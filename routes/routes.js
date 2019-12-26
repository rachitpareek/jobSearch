const express = require('express');
const spawn = require("child_process").spawn;
const router = express.Router();

router.get('/', function(req, res, next){
    res.render('../views/index.html');
});

router.get('/data', function(req, res, next) {
    // File location is relative to server.js 
    var process = spawn('python', ["./test.py"]);

    console.log('started script'); 

    process.stdout.on('data', function(data) { 
        console.log('got data'); 
        res.json(data.toString());
        console.log('script completed'); 
    });

});

module.exports = router;