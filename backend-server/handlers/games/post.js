const {paramsRequiredMessage, parameterCheck} = require('../../helpers/parameters');
const _ = require('lodash');
const {Game} = require('../../models/game');

const requiredParams = ['name'];
const optionalParams = ['password'];
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    const attributes = _.pick(req.body, requiredParams.concat(optionalParams));
    res.status(201);
    res.json(new Game(attributes.name, attributes.password));
  } else {
    res.status(400);
    res.json(paramsRequiredMessage(requiredParams));
  }
};
