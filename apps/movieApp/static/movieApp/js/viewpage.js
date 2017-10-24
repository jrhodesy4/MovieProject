
var is_review_open = "closed"

function reviewFormController(){
  if (is_review_open == "closed"){
    // $(".info-section-middle").css({display: 'inline-block'});
    $(".info-section-middle").fadeIn(1000);
    $('.opaque').fadeIn(500);
    is_review_open = "open"
  }else {
    $(".info-section-middle").css({display: 'none'});
    $('.opaque').css('display', 'none');
    is_review_open = "closed"
  }
}

var is_extra_open = "closed"

function extraController(){
  if (is_extra_open == "closed"){
    $(".extra-info-section").fadeIn(1000);

    $('.opaque').fadeIn(500);
    is_extra_open = "open"
  }else {
    $(".extra-info-section").css({display: 'none'});

    $('.opaque').css('display', 'none');
    is_extra_open = "closed"
  }
}
var is_trailer_open = "closed"

function trailerController(state){
  // if state == 'hide', hide. Else: show video
   var div = document.getElementById("trailer-sec");
   var iframe = div.getElementsByTagName("iframe")[0].contentWindow;
   div.style.display = state == 'hide' ? 'none' : '';
   func = state == 'hide' ? 'pauseVideo' : 'playVideo';
   iframe.postMessage('{"event":"command","func":"' + func + '","args":""}', '*');
  if (is_trailer_open == "closed"){
    $(".trailer-section").fadeIn(1000);
    $('.opaque').fadeIn(500);
    is_trailer_open = "open"
  }else {
    $(".trailer-section").css({display: 'none'});
    $('.opaque').css('display', 'none');
    is_trailer_open = "closed"
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
  if (json.length == 0) {
    $(".episode-list").append('<h2>No Results Found</h2>');


  }
  else {
    var img_url = "https://image.tmdb.org/t/p/w500" + json[0].poster_path
    var id = json[0].id
    var show = json[1]
    var name = json[0].name
    var poster = json[0].poster_path
    var overview = ''
    var episodes = json[0].episodes
    // var episodeId = episodes.episode_number
    var episodeId = episodes.map(function(a) {return a.episode_number;});
    var season = json[0].season_number
    var episodeName = episodes.map(function(a) {return a.name;});
    if (json[0].overview) {
      overview = json[0].overview

    }
    else {
      overview = "No synopsis available."
    }
    // $(".episode-list").append('<a href="/movie/' + id + '"><div class="result-search center"><img class ="search-result-icon" src="'+ img_url +'""> <h3 class="search-result-title">' + json[i].name + '<h3></div></a>');
    $(".episode-list").append('<img src="https://image.tmdb.org/t/p/w500' + poster + '"> <div class="season-overview"><h2>' + name + '</h2><p><b>Synopsis:</b> ' + overview + '</p></div><div class="episodes">');
    // for (var i = 0; i < json.episodes.length; i++){
      for (episode in episodeName) {
        $(".episodes").append('<a href="/episode/' + show + '/' + season + '/' + episodeId[episode] + '"><div class="episode"><p class="episode-number">' + episodeId[episode] + "</p><p class='episode-name'>" + episodeName[episode] + '</p></div></a>' );

      }
    // }
    $(".episode-list").append('</div>')
  }
}


var watchlist_status = false
function watchlist_controller(id, type){
  if (watchlist_status == false) {
    watchlist_status = true;
    addtowatchlist(id, type);
  }else {
  }
}

function addtowatchlist(id, type) {

  data = {'id': id, 'type': type};
  $.ajax({
    url: "/add/watchlist/",
    method: "get",
    data: data,
    success: function(serverResponse) {
      addedtoWatchlist();

    }
  })

}

function addedtoWatchlist(){
  $("#watchlist-button").css({"background-color": '#FC466B'});
}


function ReviewAddedSuccess(data){
  var score =  data['score']
  var color = "red"
  if(score > 60 ){
    color = "yellow";
  }
  if (score > 80) {
    color = "green";
  }


  $('.review-icon').html('<p class="review-score-number">' + score + "</p>");
  $('.review-icon').addClass(color);
  reviewFormController();
}


$(document).ready(function(){

  $('#review-form').submit(function(e){ //this is the function for submiting a review
    e.preventDefault()
    var info = $(this).serialize()
    console.log(info)
    $.ajax({
      url: $(this).attr('action'),
      type: 'POST',
      data: $(this).serialize(),
      success: function(serverResponse) {
        ReviewAddedSuccess(serverResponse);
      }
    })//end ajax


  })//end of submit

});
