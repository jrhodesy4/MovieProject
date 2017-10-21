
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
