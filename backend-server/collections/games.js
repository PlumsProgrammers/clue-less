const {Player} = require("../models/player");
const {Game} = require("../models/game");

const games = []
exports.games = games;

exports.addGame = (attributes) => {
  let game = new Game(newId(), attributes.name, attributes.password)
  games.push(game);
  return game;
}

exports.joinGame = ({gameId, username}) => {
  let game = findGame(gameId)
  if (game){
    if (game.status !== 'waiting') throw new Error('Game has already started.')
    if (game.players.some((player) => player.username === username)) throw new Error('Username already in game.');

    game.players.push(new Player(username))
    return game;
  }
}

exports.startGame = ({gameId}) => {
  let game = findGame(gameId)
  if (game) {
    game.start()
    return game
  }
}

// Private

const newId = () => {
  let max = Math.max();
  if (max === -Infinity) max = 0
  return ++max
}

function findGame(gameId) {
  return games.find((game) => game["id"] === gameId)
}
