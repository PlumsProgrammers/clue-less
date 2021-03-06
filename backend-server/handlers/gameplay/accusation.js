const {paramsRequiredMessage, parameterCheck} = require('../../helpers/parameters');
const {Game} = require('../../models/game');

const requiredParams = ['gameId', 'username', 'accusation'];
module.exports = (req, res) => {
  if (parameterCheck(req, requiredParams)) {
    try {
      const game = Game.find(req.body.gameId);
      res.json(game.makeAccusation(req.body.username, req.body.accusation));
    } catch (e) {
      res.status(400);
      res.json(e.message);
    }
  } else {
    res.status(400);
    res.json(paramsRequiredMessage(requiredParams));
  }
};
