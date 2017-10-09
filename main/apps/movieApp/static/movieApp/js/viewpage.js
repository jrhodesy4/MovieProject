
var is_review_open = "closed"

function reviewFormController(){
  if (is_review_open == "closed"){
    $(".info-section-middle").css({display: 'inline-block'});
    is_review_open = "open"
  }else {
    $(".info-section-middle").css({display: 'none'});
    is_review_open = "closed"
  }
}





$(document).ready(function(){



});
