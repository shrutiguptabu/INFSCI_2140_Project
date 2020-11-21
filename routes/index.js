var express = require('express');
var router = express.Router();
var spawn = require("child_process").spawn;

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index',{
    welcome: "Hi !"
  });
});

module.exports = router;
