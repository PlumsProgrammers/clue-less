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
    this.status = 'starting' // No Longer accepts more players
    this.setupCards();
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
