const Router = require('express').Router;
const indexRouter = new Router();

indexRouter.route('/selectSuspect').put(require('../handlers/players/selectSuspect'));

module.exports = indexRouter;
