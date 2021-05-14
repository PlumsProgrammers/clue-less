'use strict';
const about = require('../../../handlers/index/about.js');

describe('Get About Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {};
  });
  it("should use the conversations collection", () => {
    about(req, res);
    expect(res.json).toHaveBeenCalledWith(`"It's like ClueTM, just less!"
    A simplified version of the classic board game, developed for 
    EN.605.601 Foundations of Software Engineering 
    at Johns Hopkins University.`);
  });
});
