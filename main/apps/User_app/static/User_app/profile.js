$(document).ready(function(){
  $(function() {
    $("#places").autocomplete({
      source: "/api/get_places",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 2,
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;
    window.location = "/user/" + selectedObj.id;
  }






  function showDiv() {
    document.getElementById('profileDiv').style.display = "block";
  }
  function showPic() {
    document.getElementById('picDiv').style.display = "block";
  }



});
