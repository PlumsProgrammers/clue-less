'use strict';
const move = require('../../../handlers/gameplay/move.js');
const {runningGame} = require('./runningGame');

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    move(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId, username, and location are required.`);
  });
})

describe('Player move Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {
      "body": {
        "gameId": 10000,
        "username": "Testy",
        "location": "Kitchen"
      }
    };
  });

  it("errors on invalid game id", () => {
    move(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("moves player", () => {
    let testGame = runningGame('TestyGame')
    req["body"]["gameId"] = testGame.id;
    req["body"]["username"] = testGame.turn.currentPlayer.username;
    req["body"]["location"] = testGame.turn.currentPlayer.location.possibleMovements[0];
    move(req, res);
    expect(res.json).toHaveBeenCalledWith(testGame.turn.currentPlayer);
  });
});
