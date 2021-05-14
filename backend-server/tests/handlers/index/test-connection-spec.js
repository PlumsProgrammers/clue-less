'use strict';
const test_connection = require('../../../handlers/index/test_connection.js');

describe('Test Connection Test', () => {
  let res;
  let req;
  beforeEach(() => {
    res = jasmine.createSpyObj("res", ["json", "status", "send"]);
    req = {};
  });
  it("should return valid connection", () => {
    test_connection(req, res);
    expect(res.json).toHaveBeenCalledWith(`Connected Successfully`);
  });
});
