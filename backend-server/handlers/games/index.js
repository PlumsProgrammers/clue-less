const {games} = require("../../collections/games");

module.exports = (req, res) => res.json(games);
