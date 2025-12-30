def get_movie_data(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    res = response.json()

    # Check if 'results' is actually in the response
    if 'results' not in res:
        st.error(f"API Error: {res.get('status_message', 'Unknown Error')}")
        return None, None, None

    if not res['results']:
        st.warning("No movies found with that name.")
        return None, None, None
    
    movie_id = res['results'][0]['id']
    
    # Get OTT Links (Watch Providers)
    ott_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    ott_res = requests.get(ott_url).json()
    
    # Get Reviews
    review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}"
    rev_res = requests.get(review_url).json()
    
    return res['results'][0], ott_res.get('results', {}).get('IN', {}), rev_res.get('results', [])
