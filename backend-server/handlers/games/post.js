const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {addGame} = require("../../collections/games");
const _ = require('lodash');

const requiredParams = ['name']
const optionalParams = ['password']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    res.status(201)
    res.json(addGame(_.pick(req.body, requiredParams.concat(optionalParams))));
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
