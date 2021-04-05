const io = require("socket.io-client");
const socket = io('ws://localhost:3000',
  {
    query: {
      gameId: '1',
      uuid: 'asdasdasasdasdasda'
    }
  });

// client-side
socket.on("connect", () => {
  console.log("Connected!")
});

socket.on("disconnect", () => {
  console.log("Disconnected!")
});

socket.onAny((event, ..._args) => {
  console.log(`${event}`);
});
