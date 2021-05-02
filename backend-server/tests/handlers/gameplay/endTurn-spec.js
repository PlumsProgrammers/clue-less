'use strict';
const endTurn = require('../../../handlers/gameplay/endTurn.js');
const {runningGame} = require('./runningGame');

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    endTurn(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId and username are required.`);
  });
})

describe('Player end turn Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {
      "body": {
        "gameId": 10000,
        "username": "Testy",
      }
    };
  });

  it("errors on invalid game id", () => {
    endTurn(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("ends player's turn", () => {
    let testGame = runningGame('TestyGame')
    req["body"]["gameId"] = testGame.id;
    req["body"]["username"] = testGame.turn.currentPlayer.username;
    endTurn(req, res);
    expect(res.json).toHaveBeenCalledWith('Turn has ended');
    expect(testGame.turn.currentPlayer.username !== req.body.username).toBe(true);
  });
});
