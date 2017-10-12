// const request = require('request');
const express = require('express');
var app = express();

const config = require("./config.json");
const port = config['port'];
var api = config['urls']['api'];

app.set('view engine', 'ejs');
app.use('/', express.static(__dirname + '/public'));

app.listen(port, function () { console.log(`Frontend running on port ${port}.`); });