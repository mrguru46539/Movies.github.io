import streamlit as st
import requests

# 1. SETUP: Page Config
st.set_page_config(page_title="Movie Finder", page_icon="🎬")
st.title("🎬 Movie & Review Finder")

# 2. API KEY
API_KEY = "e2bc8333847254ab7e3dc139f393e885" 

# 3. REGION SELECTOR (New Feature!)
st.sidebar.header("Settings")
country_map = {"India": "IN", "USA": "US", "UK": "GB", "Canada": "CA", "Australia": "AU"}
selected_country = st.sidebar.selectbox("Select Streaming Region:", list(country_map.keys()))
region_code = country_map[selected_country]

# 4. FUNCTION DEFINITION (Now uses 'region_code')
def get_movie_data(movie_name, region):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
        response = requests.get(search_url)
        res = response.json()

        if 'results' not in res:
            st.error("API Error: Invalid Key or Connection")
            return None, None, None

        if not res['results']:
            st.warning("No movies found.")
            return None, None, None
        
        movie_id = res['results'][0]['id']
        
        # Fetch Providers (OTT)
        ott_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
        ott_res = requests.get(ott_url).json()
        
        # Fetch Reviews
        review_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}"
        rev_res = requests.get(review_url).json()
        
        # USE THE SELECTED REGION HERE
        return res['results'][0], ott_res.get('results', {}).get(region, {}), rev_res.get('results', [])

    except Exception as e:
        st.error(f"Error: {e}")
        return None, None, None

# 5. MAIN APP LOGIC
movie_query = st.text_input("Enter a movie name:", "Inception")

if st.button("Search") or movie_query:
    if movie_query:
        with st.spinner(f"Searching in {selected_country}..."):
            # Pass the selected region_code to the function
            data, ott, reviews = get_movie_data(movie_query, region_code)
            
            if data:
                st.header(data['title'])
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if data.get('poster_path'):
                        st.image(f"https://image.tmdb.org/t/p/w500{data['poster_path']}")
                
                with col2:
                    st.write(f"**Release Date:** {data.get('release_date', 'N/A')}")
                    st.write(f"**Rating:** {data.get('vote_average', 'N/A')} ⭐")
                    st.write(f"**Overview:** {data.get('overview', '')}")
                
                # Show OTT Links for SELECTED Region
                st.subheader(f"📺 Where to Watch ({selected_country})")
                if ott and 'flatrate' in ott:
                    for platform in ott['flatrate']:
                        st.write(f"- {platform['provider_name']}")
                else:
                    st.info(f"No streaming found in {selected_country}.")

                # Show Reviews
                st.subheader("💬 Reviews")
                if reviews:
                    for r in reviews[:3]:
                        st.markdown(f"> **{r['author']}**: {r['content'][:300]}...")
                        st.write("---")
                else:
                    st.write("No reviews available.")
