const express = require('express');
const routes = require('./routes');

//starting express using constant app
const app = express();

//use json on requests body
app.use(express.json());
//use routes
app.use(routes);

app.listen(3333);