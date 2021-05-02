'use strict';
const start = require('../../../handlers/games/start.js');
const {Game} = require("../../../models/game");

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    start(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId is required.`);
  });
})

describe('Game Start Test', () => {
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

  it("Should Error on invalid game id", () => {
    start(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("Returns not enough players", () => {
    let testGame = new Game("TestyGame");
    req["body"]["gameId"] = testGame.id;
    start(req, res);
    expect(res.json).toHaveBeenCalledWith('Not enough players.');
  });

  it("Starts Game", () => {
    let testGame = new Game("TestyGame");
    req["body"]["gameId"] = testGame.id;
    ['Testy', 'TestyMcTester', 'King Tester'].forEach((username) => {
      testGame.addPlayer(username)
    })
    start(req, res);
    expect(res.json).toHaveBeenCalledWith(testGame);
  });
});
