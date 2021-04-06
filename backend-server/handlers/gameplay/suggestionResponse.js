const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {Game} = require("../../models/game");

const requiredParams = ['gameId', 'username']
const optionalParams = ['card']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      let game = Game.find(req.body.gameId)
      game.suggestionReaction(req.body.username, req.body.card)
      res.json('Response Accepted')
    } catch(e) {
      res.status(400)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
