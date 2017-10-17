
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
  function doneTyping() {
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
     menuStatus = "search"
     openSearch();
     closeStackMenu();
  });

  // $(".menu-button-main").click(function(){
  //   menuController();
  //
  // })
  var isDragging = false;
  $(".menu-button-main")
  .mousedown(function() {
    isDragging = false;
  })
  .mousemove(function() {
    isDragging = true;
  })
  .mouseup(function() {
    var wasDragging = isDragging;
    isDragging = false;
    if (!wasDragging) {
      menuController();
    }
  });
});//end of document listen


// functions for top nav open/close =============
function openSearch() {
  $('.search-div').css({display: 'inline-block'})

};

function closeSearch(){
  $('.search-div').css({display: 'none'})
  $('.hamburger').animate({opacity: '1'});
  $('.icon-cancel').css({'fill': '#222222'});
  $('.icon-cancel').css({display: 'none'});
  $('.menu-button-main').animate({"background-color": "white"});
};


function jsonTaken(json){
  $('#search-results').html('')
  console.log(json);
  if (json.length == 0) {
    $("#search-results").append('<h2 class = "no-results-found" >No Results Found</h2>');
  }
  else {
  for (var i = 0; i < json.length; i++){
    var img_url = "https://image.tmdb.org/t/p/w500" + json[i].picture
    var id = json[i].id
    var type = json[i].type
    console.log(id);
    console.log(img_url);
    if (type == 'movie'){
      $("#search-results").append('<a class="search-tag" href="/movie/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <div class="title-holder"><h3 class="search-result-title">' + json[i].name + '</h3> </div> <h3 class="movie-type type">Movie</h3> </div> </a>');
    }
    else if (type == 'tv') {
      $("#search-results").append('<a class="search-tag" href="/show/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <div class="title-holder"><h3 class="search-result-title">' + json[i].name + '</h3> </div> <h3 class="tv-type type">Television</h3> </div> </a>');

    }
    else if (type =='person') {
      $("#search-results").append('<a class="search-tag" href="/people/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <div class="title-holder"><h3 class="search-result-title">' + json[i].name + '</h3> </div> <h3 class="person-type type">Person</h3> </div> </a>');
    }

  }
}
}




// here are the functions for stack-menu ===============
function menuController(){
  console.log(menuStatus)
  if (menuStatus == "closed" ){
    openStackMenu();
    menuStatus = "open";
  }
  else if (menuStatus == "search"){
    closeSearch();
    menuStatus = "closed";
  }
  else {
    closeStackMenu();
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

  if (menuStatus == "search"){
    $('.hamburger').animate({opacity: '0'}, 100);

    $('.icon-cancel').css({'fill': 'white'});
    $('.icon-cancel').css({display: 'initial'});
    $('.menu-button-main').animate({"background-color": "#FC466B"});
  }
}



//end
