const {paramsRequiredMessage, parameterCheck} = require('../../helpers/parameters');
const {Game} = require('../../models/game');

const requiredParams = ['username', 'gameId'];
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      const game = Game.find(req.body.gameId);
      game.addPlayer(req.body.username);
      res.json(game);
    } catch (e) {
      res.status(400);
      res.json(e.message);
    }
  } else {
    res.status(400);
    res.json(paramsRequiredMessage(requiredParams));
  }
};
