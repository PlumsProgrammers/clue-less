const {getLocationByName} = require('../collections/locations');
const {shuffle} = require('../helpers/cardManagement');

const turnPhases = {
  MOVEMENT: 'movement',
  SUGGESTION: 'suggestion',
  MID_SUGGESTION: 'suggestion in progress',
  ACCUSATION: 'accusation',
};
exports.turnPhases = turnPhases;

exports.Turn = class {
  constructor(players, broadcast) {
    this.turnOrder = shuffle(players);
    this.currentPlayer = this.turnOrder[0];
    this.phase = turnPhases.MOVEMENT;
    this.currentSuggestion = {};
    this.suggestTo = null;
    this.broadcast = broadcast;
  }

  suggest(suggestion) {
    this.currentSuggestion = suggestion;
    this.suggestTo = this.#findPlayerAfterUsername(this.currentPlayer.username);
    this.phase = turnPhases.MID_SUGGESTION;
    this.broadcast(`${this.suggestTo.username} can you disprove the suggestion?`);
  }

  suggestionResponse(card) {
    if (card == null) {
      this.suggestTo = this.#findPlayerAfterUsername(this.suggestTo.username);
      if (this.currentPlayer === this.suggestTo) {
        this.suggestTo = null;
        this.currentSuggestion = {};
        this.phase = turnPhases.ACCUSATION;
      } else {
        this.broadcast(`${this.suggestTo.username} can you disprove the suggestion?`);
      }
    } else {
      this.currentPlayer.broadcast(`${this.suggestTo.username} shows you: ${card}`);
      this.broadcast(`${this.suggestTo.username} shows ${this.currentPlayer} some evidence.`);
      this.suggestTo = null;
      this.currentSuggestion = {};
    }
  }

  endTurn() {
    this.#nextPlayer();
    this.phase = turnPhases.MOVEMENT;
    this.notifyPlayerOfTurn();
  }

  movePlayer(location) {
    this.currentPlayer.location = getLocationByName(location);
    this.phase = turnPhases.SUGGESTION;
    if (this.currentPlayer.location.suggestionsAllowed) {
      this.currentPlayer.broadcast(`You are now in ${this.currentPlayer.location.name}, would you like to make a suggestion?`);
    }
  }

  notifyPlayerOfTurn() {
    this.broadcast(`${this.currentPlayer.username} it is your turn.`);
  }

  // Private
  #nextPlayer() {
    this.currentPlayer = this.#findPlayerAfterUsername(this.currentPlayer.username);
    if (this.currentPlayer.failed) {
      this.#nextPlayer();
    } else {
      this.broadcast(`It is now ${this.currentPlayer.username}'s turn.`);
    }
  }

  #findPlayerAfterUsername(username) {
    let turnIndex = this.turnOrder.map((player) => player.username).indexOf(username);
    turnIndex = (turnIndex + 1) % this.turnOrder.length;
    return this.turnOrder[turnIndex];
  }
};
