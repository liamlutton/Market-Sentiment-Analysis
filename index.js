var shell = require('shelljs');

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var port = 3000;

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

// app.post('/scripts/python_test.py', function(req, res){
//   // console.log(req);
//   res.sendFile(__dirname + '/scripts/python_test.py');
// });

io.on('connection', function(socket){
    console.log('a user connecetd');
    socket.on('chat message', function(msg){
    shell.exec('sh run_file.sh ' + msg)
    io.emit('chat message', msg);
  });
});

http.listen(port, function(){
  console.log('listening on *:' + port);
});
