const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {startGame} = require("../../collections/games");
const _ = require('lodash');

const requiredParams = ['gameId']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      res.json(startGame(_.pick(req.body, requiredParams)));
    } catch(e) {
      res.status(400)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
