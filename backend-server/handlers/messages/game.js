const {paramsRequiredMessage, parameterCheck} = require('../../helpers/parameters');
const {Game} = require('../../models/game');

const requiredParams = ['gameId', 'username', 'message'];
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      const game = Game.find(req.body.gameId);
      game.broadcast(`${req.body.username}: ${req.body.message}`, 'message');
      res.json('Sent');
    } catch (e) {
      res.status(400);
      res.json(e.message);
    }
  } else {
    res.status(400);
    res.json(paramsRequiredMessage(requiredParams));
  }
};
