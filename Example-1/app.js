
//sets up node.js server
/*const express = require("express");
const app = express();

app.get("/", function (req, res) {
    res.sendFile(__dirname + "/index.html");
});

app.listen(3001, function () {
    console.log("Server is running on localhost3000");
});*/

var express = require('express');
var app = express();

app.use(express.json());

app.post('/', function(request, response) {
  console.log(request.body);
  response.send(request.body);
});

app.listen(8080, '0.0.0.0', function () {
    console.log("Server is running on localhost 8080");
});

/*process.on('uncaughtException', function (err) {
    console.log(err);
});*/
