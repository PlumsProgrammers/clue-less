const {suspects} = require("../collections/suspects");
const {shuffle} = require("../helpers/cardManagement");
const {suspectCards, weaponCards, roomCards} = require("../collections/cards");
const Game = class Game{
  constructor(id, name, password = undefined) {
    this.id = id;
    this.name = name;
    this.password = password
    this.status = 'waiting'; // Starts in lobby
    this.players = [];
    this.solution = {};
    this.turn = {};
  }

  start = () => {
    if (this.players.length < 3) throw new Error('Not enough players.')

    this.status = 'starting' // No Longer accepts more players
    this.autoAssignSuspects();
    this.setupPlayerLocations();
    this.setupCards();
  }

  autoAssignSuspects = () => {
    let selectedSuspects = this.players.map(player => player.suspect);
    let availableSuspects = suspects.map(suspect => suspect.name).filter(name => !selectedSuspects.includes(name))
    availableSuspects = shuffle(availableSuspects);
    this.players.filter(player => player.suspect === '').forEach(player => player.suspect = availableSuspects.pop())
  }

  setupPlayerLocations = () => {
    this.players.forEach((player) => {
      let suspect = suspects.find(suspect => suspect.name === player.suspect)
      player.location = suspect.startingLocation
    })
  }

  setupCards = () => {
    let suspects = shuffle(suspectCards);
    let weapons = shuffle(weaponCards);
    let rooms = shuffle(roomCards);
    this.solution['suspect'] = suspects.pop()
    this.solution['weapons'] = weapons.pop()
    this.solution['room'] = rooms.pop()
    let deck = shuffle(suspects.concat(weapons, rooms));
    this.dealCards(deck)
  }

  dealCards = (deck) => {
    let i = 0
    while(deck.length) this.players[i++ % this.players.length].cards.push(deck.pop())
  }
}
exports.Game = Game;
