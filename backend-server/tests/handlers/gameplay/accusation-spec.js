'use strict';
const accusation = require('../../../handlers/gameplay/accusation.js');
const {suspects} = require("../../../collections/suspects");
const {runningGame} = require('./runningGame');

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    accusation(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId, username, and accusation are required.`);
  });
})

describe('Player Accusation Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {
      "body": {
        "gameId": 10000,
        "username": "Testy",
        "accusation": {
          "suspect": "Miss Scarlet",
          "weapon": "Candlestick",
          "room": "Kitchen"
        }
      }
    };
  });

  it("errors on invalid game id", () => {
    accusation(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("correct guess", () => {
    let testGame = runningGame('TestyGame')
    req["body"]["gameId"] = testGame.id;
    req["body"]["username"] = testGame.turn.currentPlayer.username;
    req["body"]["accusation"] = {
      "suspect": testGame.solution.suspect,
      "weapon": testGame.solution.weapon,
      "room": testGame.solution.room,
    };
    accusation(req, res);
    expect(res.json).toHaveBeenCalledWith(true);
  });

  it("incorrect guess", () => {
    let testGame = runningGame('TestyGame')
    req["body"]["gameId"] = testGame.id;
    req["body"]["username"] = testGame.turn.currentPlayer.username;
    req["body"]["accusation"] = {
      "suspect": (suspects - testGame.solution.suspect)[0],
      "weapon": testGame.solution.weapon,
      "room": testGame.solution.room,
    };
    accusation(req, res);
    expect(res.json).toHaveBeenCalledWith(false);
  });
});
