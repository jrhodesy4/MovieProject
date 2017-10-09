$(document).ready(function(){
  var review = $('.reviewFeed')
  var follower = document.getElementById('#followerFeed')
  var following = document.getElementById('#followingFeed')
  $("#list-1").click(function(){
    console.log('list-1');
    $('.reviewFeed').css('display', 'none')
    $('.followerFeed').slideDown("slow", function() {
    });
    $('.followingFeed').css('display', 'none')

  })
  $("#list-2").click(function(){
    console.log('list-2');
    $('.reviewFeed').css('display', 'none')
    $('.followerFeed').css('display', 'none')
    $('.followingFeed').slideDown("slow", function() {
    });


  })
  $("#list-3").click(function(){
    console.log('list-3');

    $('.reviewFeed').slideDown("slow", function() {
    });
    $('.followerFeed').css('display', 'none')
    $('.followingFeed').css('display', 'none')

  })








  // var acc = document.getElementsByClassName("accordion");
  // var i;
  //
  // for (i = 0; i < acc.length; i++) {
  //   acc[i].onclick = function() {
  //     console.log("hello there");
  //     this.classList.toggle("active");
  //     var panel = this.nextElementSibling;
  //     if (panel.style.maxHeight){
  //       panel.style.maxHeight = null;
  //     } else {
  //       panel.style.maxHeight = panel.scrollHeight + "px";
  //     }
  //   }
  // }

});
