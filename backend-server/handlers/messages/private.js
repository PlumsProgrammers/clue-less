const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {Game} = require("../../models/game");

const requiredParams = ['gameId', 'username', 'targetUsername', 'message']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      let game = Game.find(req.body.gameId)
      let targetPlayer = game.findPlayer('targetUsername')
      targetPlayer.broadcast(`${req.body.username}: ${req.body.message}`, 'private')
    } catch(e) {
      res.status(400)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
