$(document).ready(function(){
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






  function showDiv() {
    document.getElementById('profileDiv').style.display = "block";
  }
});
