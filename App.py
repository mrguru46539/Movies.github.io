import streamlit as st
import requests

# 1. SETUP: Page Config & Title
st.set_page_config(page_title="Movie Finder", page_icon="🎬")
st.title("🎬 Movie & Review Finder")

# 2. API KEY (Replace this with your actual key!)
API_KEY = "e2bc8333847254ab7e3dc139f393e885"  # <--- DOUBLE CHECK THIS!

# 3. FUNCTION DEFINITION
def get_movie_data(movie_name):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        response = requests.get(search_url)
        res = response.json()

        # Safety Check 1: API Error
        if 'results' not in res:
            st.error(f"TMDb Error: {res.get('status_message', 'Invalid Key or Connection')}")
            return None, None, None

        # Safety Check 2: No Results
        if not res['results']:
            st.warning("No movies found with that name.")
            return None, None, None
        
        movie_id = res['results'][0]['id']
        
        # Fetch Providers (OTT)
        ott_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
        ott_res = requests.get(ott_url).json()
        
        # Fetch Reviews
        review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}"
        rev_res = requests.get(review_url).json()
        
        return res['results'][0], ott_res.get('results', {}).get('IN', {}), rev_res.get('results', [])

    except Exception as e:
        st.error(f"Critical Error: {e}")
        return None, None, None

# 4. USER INPUT
movie_query = st.text_input("Enter a movie name:", "Inception")

# 5. BUTTON & LOGIC (The part that makes it NOT blank!)
if st.button("Search") or movie_query:
    if movie_query:
        with st.spinner("Searching..."):
            # CALL THE FUNCTION
            data, ott, reviews = get_movie_data(movie_query)
            
            # DISPLAY RESULTS
            if data:
                st.header(data['title'])
                
                # Layout: Image on Left, Info on Right
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if data.get('poster_path'):
                        st.image(f"https://image.tmdb.org/t/p/w500{data['poster_path']}")
                
                with col2:
                    st.write(f"**Release Date:** {data.get('release_date', 'N/A')}")
                    st.write(f"**Rating:** {data.get('vote_average', 'N/A')} ⭐")
                    st.write(f"**Overview:** {data.get('overview', '')}")
                
                # Show OTT Links
                st.subheader("📺 Where to Watch (India)")
                if ott and 'flatrate' in ott:
                    for platform in ott['flatrate']:
                        st.write(f"- {platform['provider_name']}")
                else:
                    st.info("No streaming information found for this region.")

                # Show Reviews
                st.subheader("💬 Reviews")
                if reviews:
                    for r in reviews[:3]:
                        st.markdown(f"> **{r['author']}**: {r['content'][:300]}...")
                        st.write("---")
                else:
                    st.write("No reviews available.")
