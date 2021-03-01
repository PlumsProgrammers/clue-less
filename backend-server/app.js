const app = require('express')();
const server = require('http').createServer(app);
require('dotenv').config();

// Middleware to parse requests
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

// Routes
app.use('/', require('./routes/index.js'));

// Sockets Stuff, setup isn't up to date.
global.clients = [];
const io = require('socket.io')(server);
io.on('connection', function(socket) {
  global.clients.push(socket);

  socket.on('disconnect', function() {
    const index = global.clients.indexOf(socket);
    if (index !== -1) {
      global.clients.splice(index, 1);
    }
  });
});

const port = process.env.PORT;
server.listen(port);
console.log(`Listening on port: ${port}`);
