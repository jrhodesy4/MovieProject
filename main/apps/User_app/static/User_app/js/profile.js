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
        // var img_url = "https://image.tmdb.org/t/p/w500" + json[i].picture
        var id = json[i].profile_id
        var user_name = (json[i].first_name + ' ' + json[i].last_name)
        var proPic = json[i].pic_name
        // var current_user = $.session.get('user');
        // console.log(current_user);
        console.log(id);
        // if (id == current_user) {
        //   $("#searching-results").append('<a class="searching-tag" href="/profile"><div class="result-searching centaur"><div class="imgDiv"><div class="imgDiv-holder"><p>'+ proPic +'</p></div></div> <div class="title-card"><h3 class="search-result-title">' + user_name + '</h3> </div></div></a>');
        // }
        // else {
          if (proPic.length == 2){
            $("#searching-results").append('<a class="searching-tag" href="/user/' + id + '"><div class="result-searching centaur"><div class="imgDiv"><div class="imgDiv-holder"><p>'+ proPic +'</p></div></div> <div class="title-card"><h3 class="search-result-title">' + user_name + '</h3> </div></div></a>');


          }
          else {
            $("#searching-results").append('<a class="searching-tag" href="/user/' + id + '"><div class="result-searching centaur"><div class="imgDiv"><img class ="search-result-icon" src="'+ proPic +'"></div> <div class="title-card"><h3 class="search-result-title">' + user_name + '</h3> </div></div></a>');

          }

        // }

      }
    }
  }

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
  $(function () {
    if ($('#watchlist-button').val() == 'Watchlist (0)') {
      //Check to see if there is any text entered
      // If there is no text within the input ten disable the button
      $('.enableOnInput').prop('disabled', true);
    } else {
      //If there is text in the input, then enable the button
      $('.enableOnInput').prop('disabled', false);
    }

  });


  var watchlist_showing = false
  $("#watchlist-button").click(function(){
    if (watchlist_showing == false) {
      $('.watchlist-info').slideDown("slow", function() {
      });
      watchlist_showing = true

    }
    else {
      $('.watchlist-info').slideUp("slow", function() {
      });
      watchlist_showing = false
    }
  })

  // $(function() {
  //   $("#places").autocomplete({
  //     source: "/api/get_places",
  //     select: function (event, ui) { //item selected
  //       AutoCompleteSelectHandler(event, ui)
  //     },
  //     minLength: 2,
  //   });
  // });
  //
  // function AutoCompleteSelectHandler(event, ui){
  //   var selectedObj = ui.item;
  //   window.location = "/user/" + selectedObj.id;
  // }

  // function showPic() {
  //   document.getElementById('picDiv').style.display = "block";
  // }

  var hidden = true
  $("#newProf").click(function(){
    if (hidden == true) {
      $('#picDiv').css('display', 'block')
      $("#newProf").html("<h4>Cancel</h4>")
      hidden = false
    }
    else if (hidden == false) {
      $('#picDiv').css('display', 'none')
      $("#newProf").html("<h4>Add</h4>")
      hidden = true
    }
  })
  $("#editProf").click(function(){
    if (hidden == true) {
      $('#picDiv').css('display', 'block')
      $("#editProf").html("<h4>Undo</h4>")
      hidden = false
    }
    else if (hidden == false) {
      $('#picDiv').css('display', 'none')
      $("#editProf").html("<h4>Edit</h4>")
      hidden = true
    }
  })

  $("#newPro").click(function(){
    if (hidden == true) {
      $('.profileDiv').slideDown("slow", function() {
      });
      $("#newPro").val('Cancel')
      $("#newPro").css({
        'width' : '40%',
        'border-radius' : '20px',
        'background-color' : '#FC466B',
        'color': 'white',
        'margin-left': '-130px',
        'display' : 'inline-block',
        'position' : 'relative',
        'margin-bottom': '10px',
        'bottom' : '0'

      })
      hidden = false
    }
    else if (hidden == false) {
      $('.profileDiv').slideUp("slow", function() {
      });
      $("#newPro").val('Create Profile')
        $("#newPro").css({
          'width': '100%',
          'background-color': '#3F5EFB',
          'border-radius': '0px',
          'color': 'white',
          'height': '25px',
          'margin-top': '10px',
          'position': 'inherit',
          'margin-left': '0%',
        })
      hidden = true
    }
  })
  $("#editPro").click(function(){
    if (hidden == true) {
      $('.profileDiv').slideDown("slow", function() {
      });
      $("#editPro").val('Cancel')
      $("#editPro").css({
        'width' : '40%',
        'border-radius' : '20px',
        'background-color' : '#FC466B',
        'color': 'white',
        'margin-left': '-130px',
        'display' : 'inline-block',
        'position' : 'relative',
        'margin-bottom': '10px',
        'bottom' : '0'

      })
      $('.contact-info').css({
        'display' : 'none'
      })
      $('#edit').css({
        'display' : 'inline-block'
      })
      hidden = false
    }
    else if (hidden == false) {
      $('.profileDiv').slideUp("slow", function() {
      });
      $("#editPro").val('Edit Profile')
      $("#editPro").css({
        'width': '100%',
        'background-color': '#3F5EFB',
        'border-radius': '0px',
        'color': 'white',
        'height': '25px',
        'margin-top': '10px',
        'position': 'inherit',
        'margin-left': '0%',
      })
      $('#edit').css({
        'display' : 'none'
      })
      $('.contact-info').fadeIn('slow', function(){

      })

      hidden = true
    }
  })



  $('.profPic').hover(function() {
    $('#editProf').css({
      'z-index' : '21'
    });
    $('#proImg').css({
      'opacity' : '0.5'
    });
  }, function(){
    $('#editProf').css({
      'z-index' : '-1'
    });
    $('#proImg').css({
      'opacity' : 'inherit'
    });
  });

  $('.profile-pic-placeholder').hover(function() {
    $('#newProf').css({
      'z-index' : '101'
    });

  }, function(){
    $('#newProf').css({
      'z-index' : '19'
    });

  });






  // function showDiv() {
  //   document.getElementById('profileDiv').style.display = "block";
  // }
});
