'use strict';
const post = require('../../../handlers/games/post.js');

describe('Invalid parameters', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {"body": ""};
  });

  it("errors with message", () => {
    post(req, res);
    expect(res.status).toHaveBeenCalledWith(400)
    expect(res.json).toHaveBeenCalledWith(`name is required.`);
  });
})

describe('New Game Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = { "body": { "name": "TestyGame" } };
  });

  it("Should Error on invalid game id", () => {
    post(req, res);
    expect(res.status).toHaveBeenCalledWith(201)
    expect(res.json).toHaveBeenCalled();
  });
});
