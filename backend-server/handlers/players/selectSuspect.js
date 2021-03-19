const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {setSuspect} = require("../../collections/games");
const _ = require('lodash');

const requiredParams = ['gameId', 'uuid', 'suspect']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      res.json(setSuspect(_.pick(req.body, requiredParams)));
    } catch(e) {
      res.status(300)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
