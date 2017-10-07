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
    $('#close-search-button').fadeIn("slow", function() {
    });
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

  // $("#search-button").click(function() {
  //   openSearch();
  // });
  $('.search-form').submit(function(e){
       e.preventDefault()
     })

   $('#search-button').click(function(){
     openSearch();
  });


});//end of document listen


function openSearch() {
  $("#navbar-menu").fadeOut("slow", function() {
    // $('.search-bar').fadeIn("slow", function() {
    // });
    // $('.search-block').fadeIn("slow", function() {
    // });

  });
  searchAppear();

  // if ($('.search-bar').is(':hidden')) {
  //
  //   $('.search-bar').show('slide',{direction:'left'},1000);
  //   $('.search-block').show('slide',{direction:'left'},1000);
  // } else {
  //   $('.search-bar').hide('slide',{direction:'right'},1000);
  //   $('.search-block').hide('slide',{direction:'right'},1000);
  //
  // };
};

function closeSearch(){
  $("#navbar-menu").fadeIn("slow", function() {
  });
  searchAppear();


  // $(".search-bar").fadeOut("slow", function() {
  //   $("#navbar-menu").fadeIn("slow", function() {
  //   });
  // });
  // $(".search-block").fadeOut("slow", function() {
  // });
};
function searchAppear() {
  var hidden = $('.search-wrapper');
  if (hidden.hasClass('visible')){
    hidden.animate({"right":"-1000px"}, "slow").removeClass('visible');
  } else {
    hidden.animate({"right":"50px"}, "slow").addClass('visible');
  }

}

function jsonTaken(json){
  $('#search-results').html('')
  console.log(json);
  if (json.length == 0) {
    $("#search-results").append('<h2>No Results Found</h2>');


  }
  else {

  for (var i = 0; i < json.length; i++){
    var img_url = "https://image.tmdb.org/t/p/w500" + json[i].picture
    var id = json[i].id
    console.log(id);
    console.log(img_url);
    $("#search-results").append('<a href="/movie/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div></a>');
  }
}
}






//end
