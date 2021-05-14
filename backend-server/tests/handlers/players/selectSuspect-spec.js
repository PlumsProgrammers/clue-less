'use strict';
const selectSuspect = require('../../../handlers/players/selectSuspect.js');
const {Game} = require("../../../models/game");

beforeAll(() => { require('../../test-socket') })

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    selectSuspect(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId, username, and suspect are required.`);
  });
})

describe('Select Suspect Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {
      "body": {
        "gameId": 10000,
        "username": "Testy",
        "suspect": "Miss Scarlet"
      }
    };
  });

  it("Should error on invalid game id", () => {
    selectSuspect(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("Target Player isn't in game.", () => {
    let testGame = new Game("TestyGame");
    req["body"]["gameId"] = testGame.id;
    selectSuspect(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith('Player not found.')
  })

  it("Can Set Suspect", () => {
    let gameId = new Game("TestyGame").id;
    let testGame = Game.find(gameId)
    let player = testGame.addPlayer(req.body.username);
    req["body"]["gameId"] = testGame.id;
    selectSuspect(req, res);
    expect(res.json).toHaveBeenCalledWith(player)
    expect(player.suspect).toBe(req.body.suspect)
  })
});
