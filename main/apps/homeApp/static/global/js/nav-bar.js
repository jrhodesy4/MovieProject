$(document).ready(function(){
  var typingTimer;                //timer identifier
  var doneTypingInterval = 1000;  //time in ms, 5 second for example
  var $input = $('#search-info');

  //on keyup, start the countdown
  $input.on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
  });

  //on keydown, clear the countdown
  $input.on('keydown', function () {
    clearTimeout(typingTimer);
  });

  //user is "finished typing," do something
  function doneTyping () {
    console.log("send");
    $.ajax({
      url: "/search",
      method: "get",
      data: $('#search-info').serialize(),
      success: function(serverResponse) {
        jsonTaken(serverResponse);


      }
   })
  }

  $("#search-button").click(function() {
    openSearch();
  });
  $('.search-form').submit(function(e){
       e.preventDefault()
     })

});//end of document listen


function openSearch() {
  $("#navbar-menu").fadeOut("slow", function() {
    $('.search-bar').fadeIn("slow", function() {
    });
    $('.search-block').fadeIn("slow", function() {
    });
  });
};
function closeSearch(){
  $(".search-bar").fadeOut("slow", function() {
    $("#navbar-menu").fadeIn("slow", function() {
    });
  });
  $(".search-block").fadeOut("slow", function() {
  });
}


function jsonTaken(json){
  $('#search-results').html('')
  console.log(json);
  for (var i = 0; i < json.length; i++){
    var img_url = "https://image.tmdb.org/t/p/w500" + json[i].picture
    console.log(img_url);
    $("#search-results").append('<div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div>');
  }
}






//end
