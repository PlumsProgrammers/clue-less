const app = require('./app')
require('dotenv').config();
const port = process.env.PORT;

// Middleware to parse requests
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

// Routes
app.use('/', require('./routes/index.js'));
app.use('/games/', require('./routes/games.js'));
app.use('/gameplay/', require('./routes/gameplay.js'));
app.use('/messages/', require('./routes/messages.js'));
app.use('/players/', require('./routes/players.js'));

const server = require('http').createServer(app)
module.exports = server.listen(port, () => console.log(`Listening on port ${port}`));
