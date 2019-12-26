const express = require('express');
const server = express();
const path = require('path');
const router = require('./routes/routes');

const PORT = process.env.PORT || 4000; 

server.use('/', router);
server.set('views', path.join(__dirname, 'views'));
server.set('view engine', 'ejs');
server.engine('html', require('ejs').renderFile);

server.listen(PORT, () => {
    console.log(`Listening on port ${PORT}.`)
});
