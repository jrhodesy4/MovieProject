
  $(document).ready(function(){
    $("#hoverli").hover(
      function () {
        $('#actions_menu').slideDown('fast');
      },
      function () {
        $('#actions_menu').slideUp('fast');
      }
    );
  });

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
  $(function() {
    $("#movies").autocomplete({
      source: "/api/search_movies",
      select: function (event, ui) { //item selected
        AutoCompleteSelectHandler(event, ui)
      },
      minLength: 2,
    });
  });

  function AutoCompleteSelectHandler(event, ui)
  {
    var selectedObj = ui.item;
    window.location = "/movie/" + selectedObj.id;
  }


}); //this is the end
