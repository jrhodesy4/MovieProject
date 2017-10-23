


startSlidshow()

function startSlidshow() {
  slideshowController(1)
  setTimeout(startSlidshow, 5000);
}

var currentslide = 0;
function slideshowController(n){
  var newslide = currentslide + n;

  if (newslide > 9){
    newslide = 0
  }
  if (newslide < 0) {
    newslide = 9;
  }
  showSlide(currentslide, newslide);
}



function showSlide(old, current){
  targetslide = "#index-" + current;
  oldslide = "#index-" + old;

  $(oldslide).removeClass("active");
  $(oldslide).addClass("non-active");

  $(targetslide).removeClass("non-active");
  $(targetslide).addClass("active");


  currentslide = current;
}

var content_status = "review"
function changeContent(info) {
    if (info == content_status){
      return
    }
    if (info == "watchlist") {
      $('#reviews-header').removeClass('active-menu-item');
      $('#watchlist-header').addClass('active-menu-item');

      $('#review-content').css({"display": 'none'});
      $('#watchlist-content').css({"display": 'inline-block'});
      content_status = info;
    } else {
      $('#watchlist-header').removeClass('active-menu-item');
      $('#reviews-header').addClass('active-menu-item');

      $('#watchlist-content').css({"display": 'none'});
      $('#review-content').css({"display": 'inline-block'});
      content_status = info;
    }
}
