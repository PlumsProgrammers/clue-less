const Router = require('express').Router;
const indexRouter = new Router();

indexRouter.route('/').get(require('../handlers/games/index'));
indexRouter.route('/').post(require('../handlers/games/post'));
indexRouter.route('/join').post(require('../handlers/games/join'));
indexRouter.route('/start').put(require('../handlers/games/start'));

module.exports = indexRouter;
