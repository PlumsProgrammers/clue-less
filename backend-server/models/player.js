const { v4 } = require('uuid');

exports.Player = class {
  constructor(username) {
    this.username = username
    this.uuid = v4();
    this.cards = []
    this.suspect = ''
    this.location = ''
  }
}
