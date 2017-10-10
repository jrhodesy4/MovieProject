
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
function getSeasonData(id, season){
  Data = {'id': id, 'season': season}
  console.log(Data);
  $.ajax({
    url: "/seasonData",
    method: "get",
    data: Data,
    success: function(serverResponse) {
      seasonJson(serverResponse);
    }
 })

}
function seasonJson(json){
  $('.episode-list').html('')
  console.log(json);
  if (json.length == 0) {
    $(".episode-list").append('<h2>No Results Found</h2>');


  }
  else {
    var img_url = "https://image.tmdb.org/t/p/w500" + json[i].picture
    var id = json.id
    var name = json.name
    var poster = json.poster_path
    var overview = json.overview
    console.log(id);
    console.log(name);
    // $(".episode-list").append('<a href="/movie/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div></a>');
    $(".episode-list").append('<h2>' + name + '</h2><img src="https://image.tmdb.org/t/p/w500' + poster + '" <div class="season-overview"> <p>Synopsis:' + overview + '</p></div>');

  }
}





$(document).ready(function(){




});
