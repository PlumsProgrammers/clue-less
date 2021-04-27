const {paramsRequiredMessage, parameterCheck} = require('../../helpers/parameters');
const {Game} = require('../../models/game');

const requiredParams = ['gameId', 'username', 'targetUsername', 'message'];
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      const game = Game.find(req.body.gameId);
      const targetPlayer = game.players.find((player) => {
        player.username = req.body.targetUsername;
      });
      targetPlayer.broadcast(
          `${req.body.username}: ${req.body.message}`,
          'private',
      );
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
