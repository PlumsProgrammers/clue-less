const {Turn, turnPhases} = require('./turn');
const {Player} = require('./player');
const {shuffle} = require('../helpers/cardManagement');
const {suspectCards, weaponCards, roomCards} = require('../collections/cards');
const app = require('../app');
const {weaponList} = require('../collections/weapons');
const {suspects} = require('../collections/suspects');
const {locations} = require('../collections/locations');

const possibleLocations = locations.filter(location => location.suggestionsAllowed).map(location => location.name);
const possibleSuspects = suspects.map(suspect => suspect.name);

const Game = class Game{
  static allInstances = [];

  constructor(name, password = undefined) {
    this.id = Game.newId();
    this.name = name;
    this.password = password;
    this.status = 'waiting'; // Starts in lobby
    this.players = [];
    this.solution = {};
    this.turn = {};
    this.winner = null;

    Game.allInstances.push(this);
  }

  static newId() {
    let max = Math.max(...Game.allInstances.map(game => game.id));
    if (max === -Infinity) max = 0;
    return ++max;
  }

  static find(id) {
    let game =  Game.allInstances.find((game) => game.id === id);
    if (!game) throw new Error('Game not found.');

    return game;
  }

  socketRoom = () => `game-${this.id}`
  broadcast = (message, event = 'game') => app.get('io').to(this.socketRoom()).emit(event, message)

  start = () => {
    if (this.players.length < 3) throw new Error('Not enough players.');
    if (this.status !== 'waiting') throw new Error('Game already started.');

    this.status = 'starting'; // No Longer accepts more players
    this.broadcast('Game is starting');
    this.#autoAssignSuspects();
    this.#setupPlayerLocations();
    this.#setupCards();
    this.#setupTurn();
    this.status = 'playing';
    this.turn.notifyPlayerOfTurn();
  }

  addPlayer = (username, password = null) => {
    if (this.password != null && this.password !== password) throw new Error('Incorrect Password for Game.');
    if (this.status !== 'waiting') throw new Error('Game has already started.');
    if (this.players.length > 6) throw new Error('Lobby is full.');
    if (this.players.some((player) => player.username === username)) throw new Error('Username already in game.');

    let player = new Player(username);
    this.players.push(player);
    this.broadcast(`${username} has joined the game!`);
    return player;
  }

  setSuspect = (username, suspect) => {
    if (this.status !== 'waiting') throw new Error('Game has already started.');
    if (!suspects.map(suspect => suspect.name).includes(suspect)) throw new Error('Not a valid suspect.');
    if (this.players.some(player => player.suspect === suspect)) throw new Error('Suspect already taken.');

    let player = this.players.find(player => player.username === username);
    if (!player) throw new Error("Player not found.");

    player.suspect = suspect;
    this.broadcast(`${username} has selected ${suspect}!`);
    return player;
  }

  movePlayer(username, location) {
    if (this.status !== 'playing') throw new Error('Game is not in progress.');
    if (this.turn.currentPlayer.username !== username) throw new Error('Not your turn.');
    if (this.turn.phase !== turnPhases.MOVEMENT) throw new Error('Already moved or made a suggestion.');
    if (!this.turn.currentPlayer.location.canMoveTo(location))
      throw new Error(`You can not move there. Possible movements are: ${this.turn.currentPlayer.location.possibleMovements}`);

    this.turn.movePlayer(location);
    this.broadcast(`${username} has moved into the ${location}.`);
    return this.turn.currentPlayer;
  }

  makeSuggestion(username, suggestion) {
    let suggestingPlayer = this.turn.currentPlayer;
    if (this.status !== 'playing') throw new Error('Game is not in progress.');
    if (suggestingPlayer.username !== username) throw new Error('Not your turn.');
    if (!possibleLocations.includes(suggestion.room)) throw new Error('Not a valid location.');
    if (!possibleSuspects.includes(suggestion.suspect)) throw new Error('Not a valid suspect.');
    if (!weaponList.includes(suggestion.weapon)) throw new Error('Not a valid weapon.');
    if (suggestion.room !== suggestingPlayer.location.name) throw new Error('Must suggest the room you are in.');
    if (![turnPhases.MOVEMENT, turnPhases.SUGGESTION].includes(this.turn.phase)) throw new Error('Already made a suggestion.');

    this.broadcast(`${suggestingPlayer.username} is making a suggestion of: ${JSON.stringify(suggestion)}`);
    this.turn.suggest(suggestion);
  }

  suggestionResponse(username, card = null) {
    if (this.status !== 'playing') throw new Error('Game is not in progress.');
    if (this.turn.suggestTo.username !== username) throw new Error('Not your turn to respond.');
    if (card == null) {
      if (this.turn.suggestTo.cards.map((card) => card.name).some(card => Object.values(this.turn.currentSuggestion).includes(card)))
        throw new Error('You must show a card, since you can disprove the suggestion.');
    } else {
      if (!this.turn.suggestTo.cards.map((card) => card.name).includes(card)) throw new Error('You can\'t show a card you don\'t have.');
      if (!Object.values(this.turn.currentSuggestion).includes(card)) throw new Error('That card doesn\'t disprove the suggestion.');
    }

    this.turn.suggestionResponse(card);
  }

  makeAccusation(username, accusation) {
    let guessingPlayer = this.turn.currentPlayer;
    if (this.status !== 'playing') throw new Error('Game is not in progress.');
    if (guessingPlayer.username !== username) throw new Error('Not your turn.');

    this.broadcast(`${guessingPlayer.username} is making an accusation of: ${JSON.stringify(accusation)}`);
    if (this.#checkSolution(accusation)) {
      this.status = 'Finished';
      this.winner = guessingPlayer;
      this.broadcast(`${guessingPlayer.username} has won!`);
      return true;
    }

    guessingPlayer.failed = true;
    if (this.players.some(player => player.failed === false)) {
      this.turn.endTurn();
      this.broadcast(`${guessingPlayer.username} made a bad accusation and has failed`);
      return false;
    }

    this.status = 'Finished';
    this.broadcast('Everyone has failed, the game ends with no winner.');
  }

  endTurn(username) {
    if (this.status !== 'playing') throw new Error('Game is not in progress.');
    if (this.turn.currentPlayer.username !== username) throw new Error('Not your turn.');

    this.turn.endTurn(username);
  }

  // Private

  #autoAssignSuspects() {
    let selectedSuspects = this.players.map(player => player.suspect);
    let availableSuspects = suspects.map(suspect => suspect.name).filter(name => !selectedSuspects.includes(name));
    availableSuspects = shuffle(availableSuspects);
    this.players.filter(player => player.suspect === '').forEach(player => player.suspect = availableSuspects.pop());
  }

  #setupPlayerLocations() {
    this.players.forEach((player) => {
      let suspect = suspects.find(suspect => suspect.name === player.suspect);
      player.location = suspect.startingLocation;
    });
  }

  #setupCards() {
    let suspects = shuffle(suspectCards);
    let weapons = shuffle(weaponCards);
    let rooms = shuffle(roomCards);
    this.solution['suspect'] = suspects.pop().name;
    this.solution['weapon'] = weapons.pop().name;
    this.solution['room'] = rooms.pop().name;
    let deck = shuffle(suspects.concat(weapons, rooms));
    this.#dealCards(deck);
  }

  #dealCards(deck) {
    let i = 0;
    while(deck.length) this.players[i++ % this.players.length].addCard(deck.pop());
  }

  #setupTurn() { this.turn = new Turn(this.players, this.broadcast); }

  #checkSolution(accusation) {
    return (
      this.solution.suspect === accusation.suspect &&
      this.solution.weapon === accusation.weapon &&
      this.solution.room === accusation.room
    );
  }
};
exports.Game = Game;
