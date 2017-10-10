import requests
"""
****************************************************
YOU MIGHT HAVE TO PIP INSTALL REQUESTS IF YOU DO NOT ALREADY HAVE IT
****************************************************

api key =
286abf6056d0a1338f772d1b7202e728
facdbd08fccf330c5cf404d4658087ae
"""
# requests =======================================
def get_discover(): #this gets the popular movies at from the TMDB api
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1'
    json_data = requests.get(url).json()
    return json_data['results']

def popular_movies():
    url = 'https://api.themoviedb.org/3/movie/popular?api_key=facdbd08fccf330c5cf404d4658087ae&language=en-US'
    json_data = requests.get(url).json()
    return json_data['results']

def popular_actors(): #this gets the popular actors at from the TMDB api
    url = 'https://api.themoviedb.org/3/person/popular?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&page=1'
    json_data = requests.get(url).json()
    return json_data['results']

def popular_tv(): # <-- this return the popular tv shows
    url = 'https://api.themoviedb.org/3/tv/popular?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&page=1'
    json_data = requests.get(url).json()
    return json_data['results']

def get_movie(id): #this gets the popular movies at from the TMDB api
    # https://api.themoviedb.org/3/movie/{movie_id}?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US

    # this gets the main info for the selected movie
    movie_url = 'https://api.themoviedb.org/3/movie/' + id + '?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US'
    movie_data = requests.get(movie_url).json()

    #  this gets the infor about the cast
    cast_url = 'https://api.themoviedb.org/3/movie/' + id + '/credits?api_key=286abf6056d0a1338f772d1b7202e728'
    cast_data = requests.get(cast_url).json()

    movie = {
        "movie_info": movie_data,
        "cast_info": cast_data
    }

    return movie

def get_show(id): # <---- this is function to to the the entire TV

    tv_url = 'https://api.themoviedb.org/3/tv/' + id + '?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US'
    tv_data = requests.get(tv_url).json()

    cast_url = 'https://api.themoviedb.org/3/tv/' + id + '/credits?api_key=286abf6056d0a1338f772d1b7202e728'
    cast_data = requests.get(cast_url).json()
    show = {
        "show_info": tv_data,
        "cast_info": cast_data
    }
    return show

def get_season(id, season): # <---- this is function to to the the entire TV season
    season = season
    print season
    season_url = 'https://api.themoviedb.org/3/tv/' + id + '/season/' + season + '?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US'
    season_data = requests.get(season_url).json()
    return season_data

def get_episode(id, season, episode): # <---- this is function to return the indivdual episode
    episode_url = 'https://api.themoviedb.org/3/tv/' + id + '/season/' + season + '/episode/' + episode + '?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US'
    episode_data = requests.get(episode_url).json()
    return episode_data

def get_person(id): # <---- this is function to return the actor

    person_url = 'https://api.themoviedb.org/3/person/' + id + '?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US'
    person_data = requests.get(person_url).json()

    credit_url = 'https://api.themoviedb.org/3/person/' + id +'/movie_credits?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US'
    credits = requests.get(credit_url).json()

    sorted_credits = sorted(credits['cast'], key=lambda k: k['popularity'], reverse=True)
    print sorted_credits
    person = {
        "details": person_data,
        "credits": sorted_credits
    }
    return person



def get_full_nowplaying():
    page = 1
    api_key = "286abf6056d0a1338f772d1b7202e728"
    api_key2 = 'facdbd08fccf330c5cf404d4658087ae'

    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=" + api_key + "&language=en-US&page=" + str(page) + "&region=Us"


    full_movies = []
    for movie in range(0, 5):

        if page % 2 == 0:
            api_key = api_key2

        info = requests.get(url).json()
    
        for i in info['results']:
            full_movies.append(i)
        page = page + 1

    return full_movies






# end
