const {paramsRequiredMessage, parameterCheck} = require("../../helpers/parameters");
const {Game} = require("../../models/game");

const requiredParams = ['gameId', 'username', 'location']
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      let game = Game.find(req.body.gameId)
      res.json(game.movePlayer(req.body.username, req.body.location));
    } catch(e) {
      res.status(400)
      res.json(e.message)
    }
  } else {
    res.status(400)
    res.json(paramsRequiredMessage(requiredParams))
  }
}
