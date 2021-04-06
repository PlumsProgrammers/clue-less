const Router = require('express').Router;
const indexRouter = new Router();

indexRouter.route('/move').put(require('../handlers/gameplay/move'));
indexRouter.route('/suggestion').put(require('../handlers/gameplay/suggestion'));
indexRouter.route('/suggestion_response').put(require('../handlers/gameplay/suggestionResponse'));
indexRouter.route('/accusation').put(require('../handlers/gameplay/accusation'));
indexRouter.route('/end_turn').put(require('../handlers/gameplay/endTurn'));

module.exports = indexRouter;
