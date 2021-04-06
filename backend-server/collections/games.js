const { turnPhases } = require("../models/turn");
const { suspects } = require("./suspects");
const { Player } = require("../models/player");
const { Game } = require("../models/game");

const games = []
exports.games = games;

exports.addGame = (attributes) => {
  let game = new Game(newId(), attributes.name, attributes.password)
  games.push(game);
  return game;
}

exports.joinGame = ({ gameId, username }) => {
  let game = findGame(gameId)
  if (!game) throw new Error("Game not found.")
  if (game.players.length > 6) throw new Error('Lobby is full.');
  if (game.status !== 'waiting') throw new Error('Game has already started.');
  if (game.players.some((player) => player.username === username)) throw new Error('Username already in game.');

  game.players.push(new Player(username))
  return game;
}

exports.startGame = ({ gameId }) => {
  let game = findGame(gameId)
  if (!game) throw new Error("Game not found.")

  game.start()
  return game;
}

exports.setSuspect = ({ gameId, username, suspect }) => {
  let game = findGame(gameId)
  if (!game) throw new Error("Game not found.")
  if (game.status !== 'waiting') throw new Error('Game has already started.')
  if (!suspects.map(suspect => suspect.name).includes(suspect)) throw new Error('Not a valid suspect.')
  if (game.players.some(player => player.suspect === suspect)) throw new Error('Suspect already taken.')

  let player = game.players.find(player => player.username === username)
  if (!player) throw new Error("Player not found.")

  player.suspect = suspect
  return player;
}

exports.movePlayer = ({ gameId, username, location }) => {
  let game = findGame(gameId)
  if (!game) throw new Error("Game not found.")
  if (game.status !== 'playing') throw new Error("Game is not in progress.")
  if (game.turn.currentPlayer.username !== username) throw new Error("Not your turn.")
  if (game.turn.phase !== turnPhases.MOVEMENT) throw new Error("Already moved or made a suggestion.")
  if (!game.turn.currentPlayer.location.canMoveTo(location))
    throw new Error(`You can not move there. Possible movements are: ${game.turn.currentPlayer.location.possibleMovements}`)

  game.turn.movePlayer(location)
  return game.turn.currentPlayer;
}

exports.makeAccusation = ({ gameId, username, accusation }) => {
  let game = findGame(gameId)
  let guessingPlayer = game.turn.currentPlayer
  if (!game) throw new Error("Game not found.")
  if (game.status !== 'playing') throw new Error("Game is not in progress.")
  if (game.turn.currentPlayer.username !== username) throw new Error("Not your turn.")

  if (checkSolution(accusation, game.solution)) {
    game.status = 'Finished'
    game.winner = game.turn.currentPlayer
    return `${guessingPlayer.username} has won!`
  }

  guessingPlayer.failed = true
  if (game.players.some(player => player.failed === false)) {
    game.turn.nextPlayer()
    return `${guessingPlayer.username} made a bad guess and has failed`
  }

  game.status = 'Finished'
  return 'Everyone has failed, the game ends with no winner.'
}

// Private

const checkSolution = (accusation, solution) => {
  return (
    solution.suspect === accusation.suspect &&
    solution.weapon === accusation.weapon &&
    solution.room === accusation.room
  )
}

const newId = () => {
  let max = Math.max(...games.map(game => game.id));
  if (max === -Infinity) max = 0
  return ++max
}

const findGame = (gameId) => {
  return games.find((game) => game["id"] === gameId)
}
