const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {makeAccusation} = require("../../collections/games");
const _ = require('lodash');

const requiredParams = ['gameId', 'username', 'accusation']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      res.json(makeAccusation(_.pick(req.body, requiredParams)));
    } catch(e) {
      res.status(300)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
