'use strict';
const suggestionResponse = require('../../../handlers/gameplay/suggestionResponse.js');
const {runningGame} = require('./runningGame');

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    suggestionResponse(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId and username are required.`);
  });
})

describe('Player Suggestion Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {
      "body": {
        "gameId": 10000,
        "username": "Testy"
      }
    };
  });

  it("errors on invalid game id", () => {
    suggestionResponse(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("Doesnt have card", () => {
    let testGame = runningGame('TestyGame')
    testGame.movePlayer(testGame.turn.currentPlayer.username, testGame.turn.currentPlayer.location.possibleMovements[0])
    testGame.makeSuggestion(testGame.turn.currentPlayer.username, {
      "suspect": testGame.solution.suspect,
      "weapon": testGame.solution.weapon,
      "room": testGame.turn.currentPlayer.location.name,
    });
    req["body"]["gameId"] = testGame.id;
    req["body"]["username"] = testGame.turn.suggestTo.username;
    // Removing cards from there hand.
    testGame.turn.suggestTo.cards.splice(0, testGame.turn.suggestTo.cards.length)
    suggestionResponse(req, res);
    expect(res.json).toHaveBeenCalledWith('Response Accepted');
  });
});
