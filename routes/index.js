/**
 * Created on November 21, 2020
 * @author Aishwarya Jakka
 */
var express = require('express');
var router = express.Router();
var spawn = require("child_process").spawn;

/* GET home page. */
router.get('/', function(request, response, next) {
  response.render('index',{
    welcome: "Hi !"
  });
});

/* GET THE STRING amd call Main.py */
router.post("/result", function(request, response) {
  

  const searchText = request.body.searchBar;
  //Sample product json array
  var product = [
     {
      product_uid: 1,
      product_title: "Makeup Kit"
    },
   {
      product_uid: 2,
      product_title: "Kylie fancy Kit fancy"
    },
    {
      product_uid: 3,
      product_title: "I am a barbie girl"
    }

  ]
  
   return response.render("results",{ value : searchText,products : product});
  });
 
  /* GET THE Product title amd call recommend.py */

  router.get('/:title/recommend', function(request, response, next) {
    product_title = request.params.title;
    
    var recommend = [
      {
       product_uid: 1,
       product_title: "Makeup Kit"
     },
    {
       product_uid: 2,
       product_title: "Kylie fancy Kit fancy"
     },
     {
       product_uid: 3,
       product_title: "I am a barbie girl"
     }]

   // response.json(recommend)
   return response.render("recommend",{ value : product_title ,products : recommend});

  });

module.exports = router;
