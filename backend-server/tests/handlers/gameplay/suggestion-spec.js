'use strict';
const suggestion = require('../../../handlers/gameplay/suggestion.js');
const {runningGame} = require('./runningGame');

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    suggestion(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId, username, and suggestion are required.`);
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
        "username": "Testy",
        "suggestion": {
          "suspect": "Miss Scarlet",
          "weapon": "Candlestick",
          "room": "Kitchen"
        }
      }
    };
  });

  it("errors on invalid game id", () => {
    suggestion(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("valid suggestion", () => {
    let testGame = runningGame('TestyGame')
    testGame.movePlayer(testGame.turn.currentPlayer.username, testGame.turn.currentPlayer.location.possibleMovements[0])
    req["body"]["gameId"] = testGame.id;
    req["body"]["username"] = testGame.turn.currentPlayer.username;
    req["body"]["suggestion"] = {
      "suspect": testGame.solution.suspect,
      "weapon": testGame.solution.weapon,
      "room": testGame.turn.currentPlayer.location.name,
    };
    suggestion(req, res);
    expect(res.json).toHaveBeenCalledWith('Suggestion Accepted');
  });
});
