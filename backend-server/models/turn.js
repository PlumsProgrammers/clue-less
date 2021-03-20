const {getLocationByName} = require("../collections/locations");
const {shuffle} = require("../helpers/cardManagement");

const turnPhases = {
  MOVEMENT: 'movement',
  SUGGESTION: 'suggestion',
  ACCUSATION: 'accusation',
}
exports.turnPhases = turnPhases

exports.Turn = class {
  constructor(players) {
    this.turnOrder = shuffle(players)
    this.currentPlayer = this.turnOrder[0]
    this.phase = turnPhases.MOVEMENT
  }

  endTurn() {
    this.nextPlayer()
    this.phase = turnPhases.MOVEMENT
  }

  nextPlayer() {
    let currentTurnIndex = this.turnOrder.indexOf(this.currentPlayer)
    currentTurnIndex = (currentTurnIndex + 1) % this.turnOrder.length
    this.currentPlayer = this.turnOrder[currentTurnIndex]
    if (this.currentPlayer.failed) this.nextPlayer()
  }

  movePlayer(location) {
    this.currentPlayer.location = getLocationByName(location)
    this.phase = turnPhases.SUGGESTION
  }
}
