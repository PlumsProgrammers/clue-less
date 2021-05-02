'use strict';
const game = require('../../../handlers/messages/game.js');
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
    game(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId, username, and message are required.`);
  });
})

describe('Game Message Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {
      "body": {
        "gameId": 10000,
        "username": "Testy",
        "message": "Test Message",
      }
    };
  });
  it("Should Error on invalid game id", () => {
    game(req, res);
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("Sends Message", () => {
    let testGame = new Game("TestyGame");
    req["body"]["gameId"] = testGame.id;
    game(req, res);
    expect(res.json).toHaveBeenCalledWith('Sent')
  })
});
