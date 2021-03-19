const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {startGame} = require("../../collections/games");
const _ = require('lodash');

const requiredParams = ['gameId']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    res.status(200)
    res.json(startGame(_.pick(req.body, requiredParams)));
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
