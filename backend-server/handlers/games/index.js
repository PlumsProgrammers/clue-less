const {games} = require("../../models/game");
module.exports = (req, res) => res.json(games);
