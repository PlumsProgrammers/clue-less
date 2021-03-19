const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {joinGame} = require("../../collections/games");
const _ = require('lodash');

const requiredParams = ['username', 'gameId']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      let game = joinGame(_.pick(req.body, requiredParams))
      if (game) {
        res.json(game);
      } else {
        res.status(400)
        res.json("Game not found.");
      }
    } catch(e) {
      res.status(400)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
