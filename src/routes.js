const express = require('express');
const controller = require('./controllers/Controller');

const routes = express.Router();

routes.get('/cancel', controller.index);

routes.post('/cancel', controller.newCancel);

module.exports = routes;