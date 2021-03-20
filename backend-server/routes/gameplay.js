const Router = require('express').Router;
const indexRouter = new Router();

indexRouter.route('/move').put(require('../handlers/gameplay/move'));
indexRouter.route('/accusation').put(require('../handlers/gameplay/accusation'));

module.exports = indexRouter;
