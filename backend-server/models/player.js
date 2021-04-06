const { v4 } = require('uuid');
const app = require('../app')

exports.Player = class {
  constructor(username) {
    this.username = username
    this.uuid = v4();
    this.cards = []
    this.suspect = ''
    this.location = ''
    this.failed = false
  }
  socketRoom = () => this.uuid
  broadcast = (message, event = 'game') => app.get('io').to(this.socketRoom()).emit(event, message)

  addCard(card) {
    this.cards.push(card);
    this.broadcast(`New Card: ${card.name}`)
  }
}
