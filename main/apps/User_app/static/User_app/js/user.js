$(document).ready(function(){
  var typingTimer;                //timer identifier
  var doneTypingInterval = 1000;  //time in ms, 5 second for example
  var $input = $('#places');

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
  function doneTyping() {
    var input = $('#places').val();
    if (input == ''){
      $('#searching-results').css({
        'display': 'none'
      });
    }
    else {
      console.log("doneTyping");
      $.ajax({
        url: "/searchusers",
        method: "get",
        data: $('#places').serialize(),
        success: function(serverResponse) {
          jsonRetrieved(serverResponse);
        }
      })

    }
  }
  $('.content-wrapper').click(function(){
    $('#searching-results').html('')
    $('#places').val('')
  })


  $('.search-user-form').submit(function(e){
       e.preventDefault();
  })
  function jsonRetrieved(json){
    $('#searching-results').html('')
    console.log("jsonretrieved");
    console.log(json);
    if (json.length == 0) {
      $("#searching-results").append('<h2 class = "no-results-found" >No Results Found</h2>');
    }
    else {
      for (var i = 0; i < json.length; i++){
        var id = json[i].profile_id
        var user_name = (json[i].first_name + ' ' + json[i].last_name)
        var proPic = json[i].pic_name
        var kind = json[i].kind
        var current_user = json[i].logged_user

        if (id == current_user) {
          if (proPic.length == 2){
            $("#searching-results").append('<a class="searching-tag" href="/profile"><div class="result-searching centaur"><div class="imgDiv"><div class="imgDiv-holder"><p>'+ proPic +'</p></div></div> <div class="title-card"><h3 class="search-result-title">' + user_name + '</h3> </div></div></a>');
          }
          else {
            $("#searching-results").append('<a class="searching-tag" href="/profile"><div class="result-searching centaur"><div class="imgDiv"><img class ="search-result-icon" src="'+ proPic +'"></div> <div class="title-card"><h3 class="search-result-title">' + user_name + '</h3><p>' + kind + '</p></div></div></a>');

          }
        }
        else {
          if (proPic.length == 2){
            $("#searching-results").append('<a class="searching-tag" href="/user/' + id + '"><div class="result-searching centaur"><div class="imgDiv"><div class="imgDiv-holder"><p>'+ proPic +'</p></div></div> <div class="title-card"><h3 class="search-result-title">' + user_name + '</h3><p>' + kind + '</p></div></div></a>');


          }
          else {
            $("#searching-results").append('<a class="searching-tag" href="/user/' + id + '"><div class="result-searching centaur"><div class="imgDiv"><img class ="search-result-icon" src="'+ proPic +'"></div> <div class="title-card"><h3 class="search-result-title">' + user_name + '</h3><p>' + kind + '</p></div></div></a>');

          }

        }
      }
    }
  }


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

  // $(function() {
  //   $("#places").autocomplete({
  //     source: "/api/get_places",
  //     select: function (event, ui) { //item selected
  //       AutoCompleteSelectHandler(event, ui)
  //       console.log("suck me");
  //     },
  //     minLength: 2,
  //   });
  // });
  //
  // function AutoCompleteSelectHandler(event, ui){
  //   var selectedObj = ui.item;
  //   window.location = "/user/" + selectedObj.id;
  // }








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
