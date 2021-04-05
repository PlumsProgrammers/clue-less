const server = require('../server')
const io = require('socket.io')(server)

io.on('connection', function(socket) {
  console.log(`New Socket Connection! ${socket.id} gameId: ${socket.handshake.query["gameId"]} uuid: ${socket.handshake.query["uuid"]}`)

  if (socket.handshake.query["gameId"]) socket.join(`game-${socket.handshake.query["gameId"]}`) // Game Room
  if (socket.handshake.query["uuid"]) socket.join(socket.handshake.query["uuid"]) // Player Room
});

module.exports = io;
