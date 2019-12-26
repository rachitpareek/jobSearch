const express = require('express');
const server = express();
const cors = require('cors');
// const bodyParser = require('body-parser');
const path = require('path');

// const index = require('./routes/index');
const PORT = process.env.PORT || 4000; 

// server.use(bodyParser());
// server.use(cors());
// server.use('/', index);
// server.set('views', path.join(__dirname, 'views'));
server.set('view engine', 'ejs');
server.engine('html', require('ejs').renderFile);

server.listen(PORT, () => {
    console.log(`Listening on port ${PORT}.`)
});

server.get('/', function(req, res, next){
    res.send("This is a test.");
});

