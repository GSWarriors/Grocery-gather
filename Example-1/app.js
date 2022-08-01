var express = require('express');
var app = express();
const fs = require('fs');

app.use(express.json());

app.post('/', function(request, response) {
  const data = request.body;
  const path = '/home/apunj001/Example-1/logfile.json';
  dataJson = JSON.parse(JSON.stringify(data));
  console.log(dataJson);

  fs.writeFile(path, JSON.stringify(dataJson), err => {
  	if (err) {
	  console.error(err);
	}
  });

  //writing to file

  //console.log(request.body);
  response.send(request.body);
});


app.listen(8086, '0.0.0.0', function () {
    console.log("Server is running on localhost 8080");
});
