def get_movie_data(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    res = response.json()

    # SAFETY CHECK: If 'results' is missing, show the actual error message from TMDb
    if 'results' not in res:
        st.error(f"TMDb API Error: {res.get('status_message', 'Invalid API Key or connection issue')}")
        return None, None, None

    if not res['results']:
        st.warning("No movies found.")
        return None, None, None
    
    movie_id = res['results'][0]['id']
    
    # Fetch Providers and Reviews safely using .get()
    ott_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    ott_res = requests.get(ott_url).json()
    
    review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}"
    rev_res = requests.get(review_url).json()
    
    return res['results'][0], ott_res.get('results', {}).get('IN', {}), rev_res.get('results', [])
