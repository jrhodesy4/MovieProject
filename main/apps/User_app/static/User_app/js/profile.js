$(document).ready(function(){
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


  console.log('working');
  $(function() {
    $("#places").autocomplete({
      source: "/api/get_places",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
        console.log("suck me");
      },
      minLength: 2,
    });
  });

  function AutoCompleteSelectHandler(event, ui){
    var selectedObj = ui.item;
    window.location = "/user/" + selectedObj.id;
  }
  $('ul.ui-autocomplete').css({
    color: 'red'
  });

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
      hidden = false
    }
    else if (hidden == false) {
      $('#picDiv').css('display', 'none')
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
      'z-index' : '0'
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
