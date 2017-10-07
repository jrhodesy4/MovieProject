import requests
"""
****************************************************
YOU MIGHT HAVE TO PIP INSTALL REQUESTS IF YOU DO NOT ALREADY HAVE IT
****************************************************

api key = 286abf6056d0a1338f772d1b7202e728
"""
def get_discover(): #this gets the popular movies at from the TMDB api
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1'
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


def search_database(search):
    multi_search = 'https://api.themoviedb.org/3/search/multi?api_key=286abf6056d0a1338f772d1b7202e728&language=en-US&query=' + str(search) + '&page=1&include_adult=false'


    json_data = requests.get(multi_search).json()

    try:
        errrors = json_data['errors'];
        final_list = []
        return final_list
    except:
        results = json_data['results']

        newlist = sorted(results, key=lambda k: k['popularity'], reverse=True)
        final_list = []

        for result in newlist:

            if result['media_type'] == "movie":
                data = {
                    'name': result['original_title'],
                    "type": result['media_type'],
                    "pop": result['popularity'],
                    "picture": result['poster_path']
                }
                final_list.append(data)
            if result['media_type'] == "tv":
                data = {
                    'name': result['original_name'],
                    "type": result['media_type'],
                    "pop": result['popularity'],
                    "picture": result['poster_path'],
                }
                final_list.append(data)
            if result['media_type'] == "person":
                data = {
                    'name': result['name'],
                    "type": result['media_type'],
                    "pop": result['popularity'],
                    "picture": result['profile_path']
                }
                final_list.append(data)

        return final_list
