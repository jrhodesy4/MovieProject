$(document).ready(function(){

  $('.full-card-holder').click(function() {
      $(".score-holder", this).animate({left: '-100px'},{ complete:function() {
          $(this).parents('.full-card-holder').animate({left: '-205px'})
          $(this).parents('.full-card-holder').siblings('.review-extra-info').animate({left: '3px'})
      }})
  });//end click
  $(".review-extra-info").click(function(){
      $(this).animate({left: '-200px'})
      $(this).siblings('.full-card-holder').animate({left:'0px'}, {complete:function(){
          $(this).children(".score-holder").animate({left: '-5px'})
      }});
  });//end click

}); //end of document Ready
