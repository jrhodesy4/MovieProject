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

  // function showPic() {
  //   document.getElementById('picDiv').style.display = "block";
  // }
  var hidden = true
  $("#newProf").click(function(){
    if (hidden == true) {
      $('#picDiv').css('display', 'block')
      hidden = false
    }
    else if (hidden == false) {
      $('#picDiv').css('display', 'none')
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
      $('#profileDiv').css('display', 'block')
      hidden = false
    }
    else if (hidden == false) {
      $('#profileDiv').css('display', 'none')
      hidden = true
    }
  })
  $("#editPro").click(function(){
    if (hidden == true) {
      $('#profileDiv').css('display', 'block')
      hidden = false
    }
    else if (hidden == false) {
      $('#profileDiv').css('display', 'none')
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






  function showDiv() {
    document.getElementById('profileDiv').style.display = "block";
  }
});
