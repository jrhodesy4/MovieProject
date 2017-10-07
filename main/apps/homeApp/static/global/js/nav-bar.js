
var menuStatus = "closed";
$(function() {
    $(".menu-holder").draggable();
});

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

  $('.search-form').submit(function(e){
       e.preventDefault();
  })

   $('#search-button').click(function(){
     openSearch();
  });

  $(".menu-button-main").click(function(){
    menuController();
  })

});//end of document listen


// functions for top nav open/close =============
function openSearch() {
  $("#navbar-menu").fadeOut("slow", function() {
    // $('.search-bar').fadeIn("slow", function() {
    // });
    // $('.search-block').fadeIn("slow", function() {
    // });

  });
  // searchAppear();

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
    var type = json[i].type
    console.log(id);
    console.log(img_url);
    if (type == 'movie'){
      $("#search-results").append('<a href="/movie/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div></a>');
    }
    if (type == 'tv') {
      $("#search-results").append('<a href="/show/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div></a>');

    }
    else {
      $("#search-results").append('<a href="/people/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div></a>');
    }

  }
}
}



// here are the functions for stack-menu ===============
function menuController(){
  if (menuStatus == "closed" ){
    console.log(menuStatus);
    openStackMenu();
    menuStatus = "open";
  }
  else {
    closeStackMenu();
    console.log(menuStatus);
    menuStatus = "closed";
  }
}
function openStackMenu(){
  $("#menu-item-1").animate({opacity: '.9'});
  $("#menu-item-2").animate({opacity: '.9'});
  $("#menu-item-3").animate({opacity: '.9'});

  $("#menu-item-1").animate({left: '75px'});
  $("#menu-item-2").animate({left: '-150px'});
  $("#menu-item-3").animate({top: '-75px'});

  $('.hamburger').css({opacity: '0'});
  $('.icon-cancel').css({display: 'initial'});
  $('.logout-button').animate({opacity: '1'});


}
function closeStackMenu(){

  $("#menu-item-1").animate({left: '0px'});
  $("#menu-item-2").animate({left: '0px'});
  $("#menu-item-3").animate({top: '0px'});

  $("#menu-item-1").animate({opacity: '0'});
  $("#menu-item-2").animate({opacity: '0'});
  $("#menu-item-3").animate({opacity: '0'});

  $('.hamburger').animate({opacity: '1'});
  $('.icon-cancel').css({display: 'none'});
  $('.logout-button').animate({opacity: '0'});
}



//end
