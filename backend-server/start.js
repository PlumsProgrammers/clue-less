const app = require('./app')
require('./server')

// region Sockets
const io = require('./websockets/socket')
app.set('io', io) // Gives reference to requests
// endregion
