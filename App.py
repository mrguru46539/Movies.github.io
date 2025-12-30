import streamlit as st
import requests

API_KEY = "YOUR_TMDB_API_KEY"

def get_movie_data(movie_name):
    # 1. Search for Movie ID
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    res = requests.get(search_url).json()
    if not res['results']: return None
    
    movie_id = res['results'][0]['id']
    
    # 2. Get OTT Links (Watch Providers)
    ott_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
    providers = requests.get(ott_url).json()
    
    # 3. Get Reviews
    review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}"
    reviews = requests.get(review_url).json()
    
    return res['results'][0], providers.get('results', {}).get('IN', {}), reviews['results']

st.title("🎬 CineStream Scout")
movie_query = st.text_input("Enter a movie name:", "Inception")

if movie_query:
    data, ott, reviews = get_movie_data(movie_query)
    if data:
        st.header(data['title'])
        st.image(f"https://image.tmdb.org/t/p/w500{data['poster_path']}")
        st.write(f"**Rating:** {data['vote_average']} ⭐")
        
        # Display OTT Platforms
        st.subheader("📺 Where to Watch (India)")
        if ott and 'flatrate' in ott:
            for platform in ott['flatrate']:
                st.write(f"- {platform['provider_name']}")
        else:
            st.write("Not available on major streaming platforms.")

        # Display Reviews
        st.subheader("💬 Top Reviews")
        for r in reviews[:2]: # Show first 2 reviews
            st.info(f"**{r['author']}**: {r['content'][:200]}...")
