const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {Game} = require("../../models/game");

const requiredParams = ['gameId', 'username', 'suggestion']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      let game = Game.find(req.body.gameId)
      game.makeSuggestion(req.body.username, req.body.suggestion)
      res.json('Suggestion Accepted')
    } catch(e) {
      res.status(400)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
