const app = require('../app');
const io = require('../websockets/socket');
app.set('io', io); // Gives reference to requests
