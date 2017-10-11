
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
    var img_url = "https://image.tmdb.org/t/p/w500" + json[0].poster_path
    var id = json[0].id
    var show = json[1]
    var name = json[0].name
    var poster = json[0].poster_path
    var overview = json[0].overview
    var episodes = json[0].episodes
    // var episodeId = episodes.episode_number
    var episodeId = episodes.map(function(a) {return a.episode_number;});
    var season = json[0].season_number
    var episodeName = episodes.map(function(a) {return a.name;});
    console.log(show);
    console.log(id);
    console.log(name);
    console.log(episodes);
    console.log(episodeName);
    // $(".episode-list").append('<a href="/movie/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div></a>');
    $(".episode-list").append('<h2>' + name + '</h2><img src="https://image.tmdb.org/t/p/w500' + poster + '" <div class="season-overview"> <p>Synopsis:' + overview + '</p></div><div class="episodes">');
    // for (var i = 0; i < json.episodes.length; i++){
      for (episode in episodeName) {
        $(".episode-list").append('<a href="/episode/' + show + '/' + season + '/' + episodeId[episode] + '"><div class"episode"><h3>' + episodeId[episode] + '. ' + episodeName[episode] + '</h3></div></a>' );

      }
    // }
    $(".episode-list").append('</div>')
  }
}





$(document).ready(function(){




});
