'use strict';
const private_message = require('../../../handlers/messages/private.js');
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
    private_message(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`gameId, username, targetUsername, and message are required.`);
  });
})

describe('Private Message Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {
      "body": {
        "gameId": 10000,
        "username": "Testy",
        "targetUsername": "TestyMcTester",
        "message": "Test Message",
      }
    };
  });
  it("Should Error on invalid game id", () => {
    private_message(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`Game not found.`);
  });

  it("Target Player isn't in game.", () => {
    let testGame = new Game("TestyGame");
    req["body"]["gameId"] = testGame.id;
    private_message(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith('Cannot read property \'broadcast\' of undefined')
  })

  it("Sends Message", () => {
    let gameId = new Game("TestyGame").id;
    let testGame = Game.find(gameId)
    testGame.addPlayer(req.body.targetUsername);
    req["body"]["gameId"] = testGame.id;
    private_message(req, res);
    expect(res.json).toHaveBeenCalledWith('Sent')
  })
});
