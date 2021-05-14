const Router = require('express').Router;
const indexRouter = new Router();

indexRouter.route('/game').post(require('../handlers/messages/game'));
indexRouter.route('/private').post(require('../handlers/messages/private'));

module.exports = indexRouter;
