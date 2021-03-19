const {suspects} = require("./suspects");
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
    if (game.players.length > 6) throw new Error('Lobby is full.');
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

exports.setSuspect = ({gameId, uuid,  suspect}) => {
  let game = findGame(gameId)
  if (game) {
    if (game.status !== 'waiting') throw new Error('Game has already started.')
    if (!suspects.includes(suspect)) throw new Error('Not a valid suspect.')
    if (game.players.some(player => player.suspect === suspect)) throw new Error('Suspect already taken.')

    let player = game.players.find(player => player.uuid === uuid)
    if (player) {
      player.suspect = suspect
      return player;
    }
  }
}

// Private

const newId = () => {
  let max = Math.max();
  if (max === -Infinity) max = 0
  return ++max
}

const findGame = (gameId) => {
  return games.find((game) => game["id"] === gameId)
}
