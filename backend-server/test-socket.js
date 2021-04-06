const io = require("socket.io-client");
require('dotenv').config();
const uuid = process.env.uuid;
const socket = io('ws://localhost:3000',
  {
    query: {
      gameId: '1',
      uuid: uuid
    }
  });

// client-side
socket.on("connect", () => {
  console.log("Connected!")
});

socket.on("disconnect", () => {
  console.log("Disconnected!")
});

socket.onAny((event, ...args) => {
  switch (event) {
    case 'game':
      console.log(`${args[0]}`);
      break;
    case 'message':
      `message: ${console.log(args[0])}`
      break;
    case 'private':
      `private message: ${console.log(args[0])}`
      break;
    default: console.log(event, args.join(''))
  }
});
