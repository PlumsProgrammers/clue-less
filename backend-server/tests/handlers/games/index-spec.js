'use strict';
const index = require('../../../handlers/games/index.js');
const {Game} = require("../../../models/game");

describe('Game Index Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {};
    Game.allInstances.splice(0, Game.allInstances.length) // Resets all games
  });
  it("Returns no games", () => {
    index(req, res);
    expect(res.json).toHaveBeenCalledWith([]);
  });

  it("Returns all games", () => {
    let game = new Game('TestGame1')
    let game2 = new Game('TestGame2')
    index(req, res);
    expect(res.json).toHaveBeenCalledWith([game, game2]);
  });
});
