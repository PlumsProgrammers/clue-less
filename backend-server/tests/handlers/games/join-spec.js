'use strict';
const join = require('../../../handlers/games/join.js');
const {Game} = require("../../../models/game");

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    join(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`username and gameId are required.`);
  });
})

describe('Game Join Test', () => {
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
    join(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("Returns all games", () => {
    let testGame = new Game("TestyGame");
    req["body"]["gameId"] = testGame.id;
    join(req, res);
    expect(res.json).toHaveBeenCalledWith(testGame);
  });
});
