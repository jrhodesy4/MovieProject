$(document).ready(function(){
  $("#search-button").click(function() {
    search();
  });

});//end of document listen


function search() {
  hideNav();
};

function closeSearch(){
  $(".search-bar").fadeOut("slow", function() {
    $("#navbar-menu").fadeIn("slow", function() {
    });
  });
}

function hideNav(){
  $("#navbar-menu").fadeOut("slow", function() {
    $('.search-bar').fadeIn("slow", function() {
    });
  });
};
