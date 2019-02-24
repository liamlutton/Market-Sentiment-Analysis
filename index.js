var shell = require('shelljs');
var path = require('path');

var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var port = 3000;

app.use(express.static(__dirname + "/public"));

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

app.get('/dashboard', function(req, res){
  res.sendFile(__dirname + '/dashboard.html');
});

io.on('connection', function(socket){
    console.log('User entered website');
    socket.on('request-stock', function(msg){
        shell.exec('sh run_file.sh ' + msg)
        //io.emit('request-stock', msg);
  });
});

http.listen(port, function(){
  console.log('listening on *:' + port);
});
