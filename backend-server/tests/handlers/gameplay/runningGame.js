const {Game} = require('../../../models/game');

exports.runningGame = (gameName = 'TestyGame') => {
  let testGame = new Game(gameName);
  ['Testy', 'TestyMcTester', 'King Tester'].forEach((username) => {
    testGame.addPlayer(username);
  });
  testGame.start();
  return testGame;
};
