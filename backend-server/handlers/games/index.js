const {Game} = require("../../models/game");

module.exports = (req, res) => res.json(Game.allInstances);
