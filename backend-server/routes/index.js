const {suspectCards} = require("../collections/cards");
const {shuffle} = require("../helpers/cardManagement");
const Router = require('express').Router;
const indexRouter = new Router();

indexRouter.route('/').get((req, res) => {
  res.json(shuffle(suspectCards))
})
indexRouter.route('/about').get(require('../handlers/index/about'));
indexRouter.route('/test_connection').get(require('../handlers/index/test_connection'));

module.exports = indexRouter;
