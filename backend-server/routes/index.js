const Router = require('express').Router;
const indexRouter = new Router();

indexRouter.route('/about').get(require('../handlers/index/about'));

module.exports = indexRouter;
