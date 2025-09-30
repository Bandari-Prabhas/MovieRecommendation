import streamlit as st
import requests
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ------------------------
# TMDB API Configuration
# ------------------------
TMDB_API_KEY = 'a7338b0ba002aad27b5c98531dc29097'
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
TMDB_BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"
BASE_URL = "https://api.themoviedb.org/3"

# Telugu language code for TMDB
TELUGU_LANGUAGE_CODE = 'te'

# ------------------------
# Page Configuration
# ------------------------
st.set_page_config(
    page_title="🎬 CineMatch Telugu - Movie Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------------
# Enhanced CSS Styling
# ------------------------
def load_advanced_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a0000 0%, #0a0000 15%, #2d0a0a 30%, #4a0000 45%, #1a0000 60%, #0a0000 75%, #2d0a0a 90%, #1a0000 100%);
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 30%, rgba(229, 9, 20, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(139, 0, 0, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(178, 34, 34, 0.1) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
    }
    
    .stApp > * {
        position: relative;
        z-index: 1;
    }
    
    /* Carousel Styles */
    .carousel-container {
        position: relative;
        margin: 0;
        padding: 0;
        overflow: hidden;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }
    
    /* Full-width container override */
    .full-width-carousel {
        margin: 0;
        margin-left: calc(-50vw + 50%);
        margin-right: calc(-50vw + 50%);
        margin-top: -2rem;
        padding: 0;
        width: 100vw;
        max-width: 100vw;
    }
    
    /* Remove Streamlit's default padding */
    .block-container {
        padding-top: 0 !important;
    }
    
    /* Search and Filter Section */
    .search-filter-section {
        background: linear-gradient(145deg, rgba(229, 9, 20, 0.25), rgba(139, 0, 0, 0.15));
        padding: 2.5rem;
        border-radius: 25px;
        margin: 3rem 0;
        border: 2px solid rgba(229, 9, 20, 0.4);
        backdrop-filter: blur(15px);
        box-shadow: 0 15px 40px rgba(229, 9, 20, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .search-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 20px rgba(229, 9, 20, 0.6), 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    /* Movie Cards */
    .movie-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        border-radius: 20px;
        overflow: hidden;
        border: 1px solid rgba(229, 9, 20, 0.3);
        backdrop-filter: blur(15px);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        position: relative;
    }
    
    .movie-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 30px 60px rgba(229, 9, 20, 0.4);
        border-color: rgba(229, 9, 20, 0.6);
    }
    
    .movie-poster {
        width: 100%;
        height: 250px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    
    .movie-card:hover .movie-poster {
        transform: scale(1.05);
    }
    
    .movie-info {
        padding: 1.5rem;
    }
    
    .movie-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.8rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .movie-meta {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .rating-badge {
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        color: #1a1a1a;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    .meta-item {
        color: #cccccc;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .movie-overview {
        color: #e6e6e6;
        line-height: 1.6;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #e50914, #b8860b) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 25px rgba(229, 9, 20, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 35px rgba(229, 9, 20, 0.5) !important;
        background: linear-gradient(135deg, #ff1025, #d4a017) !important;
    }
    
    /* Statistics Dashboard */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(229, 9, 20, 0.3), rgba(139, 0, 0, 0.2));
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        border: 2px solid rgba(229, 9, 20, 0.5);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(229, 9, 20, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(229, 9, 20, 0.6), 0 0 30px rgba(229, 9, 20, 0.4);
        border-color: rgba(255, 69, 58, 0.8);
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(229, 9, 20, 0.8), 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #f5f5f5;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(229, 9, 20, 0.5), 1px 1px 3px rgba(0,0,0,0.7);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin: 3rem 0 2rem 0;
        text-align: center;
        text-shadow: 0 0 25px rgba(229, 9, 20, 0.7), 0 0 15px rgba(255, 69, 58, 0.5), 2px 2px 6px rgba(0,0,0,0.8);
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, transparent, #e50914, #ff4538, #e50914, transparent);
        border-radius: 2px;
        box-shadow: 0 0 15px rgba(229, 9, 20, 0.8);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ------------------------
# API Functions with Enhanced Error Handling
# ------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_from_tmdb(endpoint, params=None):
    """Fetch data from TMDB API with robust error handling"""
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    
    if params is None:
        params = {}
    params['api_key'] = TMDB_API_KEY
    params['language'] = 'en-US'

    for attempt in range(MAX_RETRIES):
        try:
            time.sleep(0.3)
            session = requests.Session()
            session.mount('https://', requests.adapters.HTTPAdapter(
                max_retries=3,
                pool_connections=10,
                pool_maxsize=10
            ))
            
            response = session.get(
                f"{BASE_URL}{endpoint}", 
                params=params, 
                timeout=20,
                headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0'
                }
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 2))
                    continue
            else:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                    continue
                    
        except (requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
                
    return None

@st.cache_data(ttl=3600, show_spinner=False)
def search_telugu_movies(query, page=1):
    """Search for Telugu movies specifically"""
    params = {
        'query': query,
        'page': page,
        'with_original_language': TELUGU_LANGUAGE_CODE
    }
    return fetch_from_tmdb('/search/movie', params)

@st.cache_data(ttl=3600, show_spinner=False)
def get_movie_details(movie_id):
    """Get detailed movie information"""
    return fetch_from_tmdb(f'/movie/{movie_id}', {'append_to_response': 'credits,videos,keywords,reviews'})

@st.cache_data(ttl=3600, show_spinner=False)
def get_popular_telugu_movies(page=1):
    """Get popular Telugu movies"""
    params = {
        'page': page,
        'with_original_language': TELUGU_LANGUAGE_CODE,
        'sort_by': 'popularity.desc'
    }
    return fetch_from_tmdb('/discover/movie', params)

@st.cache_data(ttl=3600, show_spinner=False)
def get_top_rated_telugu_movies(page=1):
    """Get top rated Telugu movies"""
    params = {
        'page': page,
        'with_original_language': TELUGU_LANGUAGE_CODE,
        'sort_by': 'vote_average.desc',
        'vote_count.gte': 100
    }
    return fetch_from_tmdb('/discover/movie', params)

@st.cache_data(ttl=3600, show_spinner=False)
def get_genres():
    """Get movie genres"""
    return fetch_from_tmdb('/genre/movie/list')

@st.cache_data(ttl=3600, show_spinner=False)
def discover_telugu_movies(genre_id=None, sort_by='popularity.desc', page=1, year=None, min_rating=None):
    """Discover Telugu movies by various filters"""
    params = {
        'sort_by': sort_by,
        'page': page,
        'with_original_language': TELUGU_LANGUAGE_CODE
    }
    if genre_id:
        params['with_genres'] = genre_id
    if year:
        params['year'] = year
    if min_rating:
        params['vote_average.gte'] = min_rating
        params['vote_count.gte'] = 50
    return fetch_from_tmdb('/discover/movie', params)

@st.cache_data(ttl=3600, show_spinner=False)
def get_trending_telugu_movies():
    """Get trending Telugu movies"""
    params = {
        'page': 1,
        'with_original_language': TELUGU_LANGUAGE_CODE,
        'sort_by': 'popularity.desc'
    }
    return fetch_from_tmdb('/discover/movie', params)

@st.cache_data(ttl=3600, show_spinner=False)
def get_upcoming_telugu_movies():
    """Get upcoming Telugu movies"""
    params = {
        'page': 1,
        'with_original_language': TELUGU_LANGUAGE_CODE,
        'primary_release_date.gte': datetime.now().strftime('%Y-%m-%d'),
        'sort_by': 'primary_release_date.asc'
    }
    return fetch_from_tmdb('/discover/movie', params)

# ------------------------
# Data Processing Functions
# ------------------------
def create_movie_dataframe(movies_list):
    """Convert movies list to pandas DataFrame"""
    if not movies_list:
        return pd.DataFrame()
    
    df = pd.DataFrame(movies_list)
    
    if 'release_date' in df.columns:
        df['release_year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year
        df['age'] = datetime.now().year - df['release_year']
    
    if 'vote_average' in df.columns and 'vote_count' in df.columns:
        min_votes = df['vote_count'].quantile(0.7)
        mean_rating = df['vote_average'].mean()
        
        df['weighted_rating'] = ((df['vote_count'] / (df['vote_count'] + min_votes)) * df['vote_average'] + 
                               (min_votes / (df['vote_count'] + min_votes)) * mean_rating)
    
    return df

def get_youtube_trailer_url(movie_id):
    """Get YouTube trailer URL for a movie"""
    try:
        movie_details = get_movie_details(movie_id)
        if movie_details and 'videos' in movie_details:
            videos = movie_details['videos'].get('results', [])
            for video in videos:
                if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                    return f"https://www.youtube.com/embed/{video['key']}?autoplay=1&mute=1&loop=1&playlist={video['key']}"
        return None
    except:
        return None

# ------------------------
# UI Components
# ------------------------
def display_telugu_hero_carousel():
    """Display hero carousel with Telugu movie trailers"""
    # Custom video URL for the OG Telugu movie
    CUSTOM_VIDEO_URL = "https://www.youtube.com/embed/_8J8LwoVH_0?autoplay=0&loop=1&playlist=_8J8LwoVH_0&controls=1&modestbranding=1&rel=0&showinfo=0"
    
    # Custom Telugu movie data for 2025
    telugu_movies = [
        {
            "title": "OG",
            "custom_video": CUSTOM_VIDEO_URL,
            "rating": 8.5,
            "year": "2025",
            "genres": "Action, Thriller, Drama",
            "overview": "A powerful Telugu action thriller featuring a gripping storyline with intense performances and high-octane action sequences."
        },
        {"id": 951491, "title": "RRR"},
        {"id": 338967, "title": "Baahubali 2"},
        {"id": 631842, "title": "Pushpa"},
        {"id": 939335, "title": "Salaar"}
    ]
    
    # Initialize carousel state
    if 'carousel_index' not in st.session_state:
        st.session_state.carousel_index = 0
    if 'carousel_movies' not in st.session_state:
        st.session_state.carousel_movies = []
        with st.spinner('Loading Telugu blockbusters...'):
            for movie_info in telugu_movies:
                if 'custom_video' in movie_info:
                    # Add custom movie directly
                    st.session_state.carousel_movies.append(movie_info)
                else:
                    # Fetch from TMDB
                    details = get_movie_details(movie_info["id"])
                    if details:
                        st.session_state.carousel_movies.append(details)
                time.sleep(0.5)
    
    if st.session_state.carousel_movies and len(st.session_state.carousel_movies) > 0:
        current_movie = st.session_state.carousel_movies[st.session_state.carousel_index]
        
        # Check if custom video
        if 'custom_video' in current_movie:
            video_url = current_movie['custom_video']
            st.markdown(f"""
            <div class="full-width-carousel">
                <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%; overflow: hidden; background: #000;">
                    <iframe 
                        src="{video_url}" 
                        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                    </iframe>
                </div>
                <div style="text-align: center; margin-top: 2.5rem; padding: 0 2rem; margin-bottom: 2rem;">
                    <h2 style="color: white; font-size: 3.5rem; font-weight: 800; text-shadow: 3px 3px 6px rgba(0,0,0,0.8); font-family: 'Poppins', sans-serif; margin-bottom: 1.5rem;">
                        {current_movie.get('title', 'Unknown')}
                    </h2>
                    <div style="display: flex; justify-content: center; gap: 2.5rem; margin-top: 1.5rem; flex-wrap: wrap;">
                        <span class="rating-badge" style="font-size: 1.1rem; padding: 0.6rem 1.2rem;">⭐ {current_movie.get('rating', 0):.1f}/10</span>
                        <span style="color: #ffcccc; font-size: 1.3rem; font-weight: 600;">📅 {current_movie.get('year', 'N/A')}</span>
                        <span style="color: #ffcccc; font-size: 1.3rem; font-weight: 600;">🎭 {current_movie.get('genres', 'N/A')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Get trailer URL from TMDB
            trailer_url = get_youtube_trailer_url(current_movie.get('id'))
            
            if trailer_url:
                # Remove controls from TMDB trailers too
                trailer_url = trailer_url.replace('?', '?controls=0&modestbranding=1&rel=0&showinfo=0&')
                st.markdown(f"""
                <div class="full-width-carousel">
                    <div style="position: relative; width: 100%; height: 0; padding-bottom: 56.25%; overflow: hidden; background: #000;">
                        <iframe 
                            src="{trailer_url}" 
                            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                            allowfullscreen>
                        </iframe>
                    </div>
                    <div style="text-align: center; margin-top: 2.5rem; padding: 0 2rem; margin-bottom: 2rem;">
                        <h2 style="color: white; font-size: 3.5rem; font-weight: 800; text-shadow: 3px 3px 6px rgba(0,0,0,0.8); font-family: 'Poppins', sans-serif; margin-bottom: 1.5rem;">
                            {current_movie.get('title', 'Unknown')}
                        </h2>
                        <div style="display: flex; justify-content: center; gap: 2.5rem; margin-top: 1.5rem; flex-wrap: wrap;">
                            <span class="rating-badge" style="font-size: 1.1rem; padding: 0.6rem 1.2rem;">⭐ {current_movie.get('vote_average', 0):.1f}/10</span>
                            <span style="color: #ffcccc; font-size: 1.3rem; font-weight: 600;">📅 {current_movie.get('release_date', 'N/A')[:4] if current_movie.get('release_date') else 'N/A'}</span>
                            <span style="color: #ffcccc; font-size: 1.3rem; font-weight: 600;">🎭 {', '.join([g['name'] for g in current_movie.get('genres', [])[:3]])}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                backdrop_url = f"{TMDB_BACKDROP_BASE}{current_movie.get('backdrop_path')}" if current_movie.get('backdrop_path') else "https://via.placeholder.com/1920x800?text=No+Trailer"
                st.markdown(f"""
                <div class="full-width-carousel">
                    <div style="background-image: url('{backdrop_url}'); height: 650px; background-size: cover; background-position: center; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(transparent, rgba(0,0,0,0.95)); padding: 4rem 3rem;">
                            <h2 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1.5rem; font-family: 'Poppins', sans-serif; color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.8);">{current_movie.get('title', 'Unknown')}</h2>
                            <div style="display: flex; gap: 2rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                                <span class="rating-badge" style="font-size: 1.1rem; padding: 0.6rem 1.2rem;">⭐ {current_movie.get('vote_average', 0):.1f}</span>
                                <span style="color: #ffcccc; font-size: 1.3rem; font-weight: 600;">📅 {current_movie.get('release_date', 'N/A')[:4]}</span>
                                <span style="color: #ffcccc; font-size: 1.3rem; font-weight: 600;">🎭 {', '.join([g['name'] for g in current_movie.get('genres', [])[:3]])}</span>
                            </div>
                            <p style="font-size: 1.2rem; max-width: 800px; color: #e6e6e6; line-height: 1.8;">{current_movie.get('overview', 'No description')[:300]}...</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Navigation
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        with col2:
            if st.button("⬅️ Previous", key="prev_trailer"):
                st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(st.session_state.carousel_movies)
                st.rerun()
        with col4:
            if st.button("Next ➡️", key="next_trailer"):
                st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(st.session_state.carousel_movies)
                st.rerun()
        
        # Indicators
        indicator_html = '<div style="display: flex; justify-content: center; gap: 1rem; margin: 2rem 0;">'
        for i in range(len(st.session_state.carousel_movies)):
            active = "background: #e50914; transform: scale(1.3);" if i == st.session_state.carousel_index else "background: rgba(255,255,255,0.4);"
            indicator_html += f'<div style="width: 12px; height: 12px; border-radius: 50%; {active} transition: all 0.3s;"></div>'
        indicator_html += '</div>'
        st.markdown(indicator_html, unsafe_allow_html=True)

def display_search_filter_section():
    """Display search and filter options"""
    st.markdown("""
    <div class="search-filter-section">
        <h2 class="search-title">🔍 Discover Telugu Movies</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        search_query = st.text_input(
            label="Search Movies",
            placeholder="Search for Telugu movies...",
            key="main_search",
            label_visibility="collapsed"
        )
    
    with col2:
        genres_data = get_genres()
        genre_options = ["All Genres"] + [g['name'] for g in genres_data.get('genres', [])] if genres_data else ["All Genres"]
        selected_genre = st.selectbox("Genre", genre_options, key="genre_select")
    
    with col3:
        year_options = ["All Years"] + list(range(datetime.now().year, 1990, -1))
        selected_year = st.selectbox("Year", year_options, key="year_select")
    
    with col4:
        sort_options = ["Popular", "Top Rated", "Latest"]
        selected_sort = st.selectbox("Sort By", sort_options, key="sort_select")
    
    return search_query, selected_genre, selected_year, selected_sort

def display_movie_card(movie):
    """Display individual movie card"""
    poster_url = f"{TMDB_IMAGE_BASE}{movie.get('poster_path')}" if movie.get('poster_path') else "https://via.placeholder.com/500x750?text=No+Poster"
    
    card_html = f"""
    <div class="movie-card">
        <img src="{poster_url}" alt="{movie.get('title', 'Movie')}" class="movie-poster">
        <div class="movie-info">
            <h3 class="movie-title">{movie.get('title', 'Unknown Title')}</h3>
            <div class="movie-meta">
                <span class="rating-badge">⭐ {movie.get('vote_average', 0):.1f}</span>
                <span class="meta-item">📅 {movie.get('release_date', 'N/A')[:4] if movie.get('release_date') else 'N/A'}</span>
                <span class="meta-item">❤️ {movie.get('vote_count', 0):,}</span>
            </div>
            <p class="movie-overview">{movie.get('overview', 'No description available.')[:180]}{'...' if len(movie.get('overview', '')) > 180 else ''}</p>
        </div>
    </div>
    """
    return card_html

def display_statistics_dashboard(df):
    """Display statistics dashboard"""
    if df.empty:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{len(df)}</div>
            <div class="stat-label">Total Movies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_rating = df['vote_average'].mean() if 'vote_average' in df.columns else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_rating:.1f}</div>
            <div class="stat-label">Avg Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        latest_year = df['release_year'].max() if 'release_year' in df.columns else datetime.now().year
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{int(latest_year) if not pd.isna(latest_year) else 'N/A'}</div>
            <div class="stat-label">Latest Year</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_votes = df['vote_count'].sum() if 'vote_count' in df.columns else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{int(total_votes):,}</div>
            <div class="stat-label">Total Votes</div>
        </div>
        """, unsafe_allow_html=True)

def display_movies_grid(search_query="", genre="All Genres", year="All Years", sort_by="Popular"):
    """Display grid of Telugu movies"""
    
    # Fetch Telugu movies based on filters
    if search_query:
        movies_data = search_telugu_movies(f"{search_query}")
    else:
        if sort_by == "Popular":
            movies_data = get_popular_telugu_movies(page=1)
        elif sort_by == "Top Rated":
            movies_data = get_top_rated_telugu_movies(page=1)
        elif sort_by == "Latest":
            movies_data = discover_telugu_movies(sort_by='release_date.desc', page=1)
        else:
            movies_data = discover_telugu_movies(sort_by='vote_average.desc', page=1)
    
    if not movies_data or 'results' not in movies_data or len(movies_data['results']) == 0:
        st.warning("⚠️ No Telugu movies found. Try different search terms.")
        return
    
    movies = movies_data['results']
    df = create_movie_dataframe(movies)
    
    # Display statistics
    display_statistics_dashboard(df)
    
    # Display movies
    st.markdown('<h2 class="section-header">🎬 Featured Telugu Movies</h2>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, movie in enumerate(movies[:12]):
        with cols[idx % 3]:
            st.markdown(display_movie_card(movie), unsafe_allow_html=True)
            
            if st.button(f"🎥 View Details", key=f"movie_{movie.get('id')}_{idx}"):
                st.session_state.selected_movie_id = movie.get('id')
                st.session_state.show_details = True
                st.rerun()
    
    # Display charts
    if not df.empty and len(df) > 5:
        st.markdown('<h2 class="section-header">📊 Data Insights</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(df, x='vote_average', nbins=20, 
                               title='Rating Distribution',
                               color_discrete_sequence=['#e50914'])
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis_title='Rating',
                yaxis_title='Count'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if 'release_year' in df.columns:
                year_counts = df['release_year'].value_counts().sort_index()
                fig2 = px.line(x=year_counts.index, y=year_counts.values,
                              title='Telugu Movies Released by Year',
                              color_discrete_sequence=['#e50914'])
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    xaxis_title='Year',
                    yaxis_title='Movies'
                )
                st.plotly_chart(fig2, use_container_width=True)

# ------------------------
# Recommendation System
# ------------------------
def display_recommendations_section():
    """Display Telugu movie recommendations based on user preferences"""
    st.markdown('<h2 class="section-header">🎯 Personalized Telugu Movie Recommendations</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="search-filter-section">
        <p style="text-align: center; color: #cccccc; font-size: 1.1rem; margin-bottom: 1.5rem;">
            Get Telugu movie recommendations based on your favorite genres and preferences
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        genres_data = get_genres()
        if genres_data:
            genre_list = [g for g in genres_data.get('genres', [])]
            selected_genres = st.multiselect(
                "Select Your Favorite Genres",
                options=[g['name'] for g in genre_list],
                default=[],
                key="rec_genres"
            )
    
    with col2:
        min_rating = st.slider("Minimum Rating", 0.0, 10.0, 7.0, 0.5, key="rec_rating")
    
    with col3:
        min_year = st.slider("From Year", 1990, datetime.now().year, 2015, key="rec_year")
    
    if st.button("🎬 Get Telugu Movie Recommendations", key="get_recommendations"):
        if selected_genres:
            # Get genre IDs
            genre_ids = [g['id'] for g in genre_list if g['name'] in selected_genres]
            genre_id_str = ','.join(map(str, genre_ids))
            
            # Fetch recommendations
            with st.spinner('Finding perfect Telugu movies for you...'):
                recommendations = discover_telugu_movies(
                    genre_id=genre_id_str,
                    min_rating=min_rating,
                    year=min_year,
                    sort_by='vote_average.desc'
                )
                
                if recommendations and 'results' in recommendations:
                    movies = recommendations['results'][:9]
                    
                    st.markdown(f"### Found {len(movies)} Telugu movies matching your preferences!")
                    
                    cols = st.columns(3)
                    for idx, movie in enumerate(movies):
                        with cols[idx % 3]:
                            st.markdown(display_movie_card(movie), unsafe_allow_html=True)
                            if st.button(f"View Details", key=f"rec_movie_{movie.get('id')}_{idx}"):
                                st.session_state.selected_movie_id = movie.get('id')
                                st.session_state.show_details = True
                                st.rerun()
                else:
                    st.warning("No Telugu movies found matching your criteria. Try adjusting the filters.")
        else:
            st.info("Please select at least one genre to get recommendations.")

# ------------------------
# Trending Section
# ------------------------
def display_trending_section():
    """Display trending Telugu movies"""
    st.markdown('<h2 class="section-header">🔥 Trending Telugu Movies</h2>', unsafe_allow_html=True)
    
    trending_data = get_trending_telugu_movies()
    
    if trending_data and 'results' in trending_data:
        movies = trending_data['results'][:6]
        
        cols = st.columns(3)
        for idx, movie in enumerate(movies):
            with cols[idx % 3]:
                st.markdown(display_movie_card(movie), unsafe_allow_html=True)
                if st.button(f"View Details", key=f"trending_{movie.get('id')}_{idx}"):
                    st.session_state.selected_movie_id = movie.get('id')
                    st.session_state.show_details = True
                    st.rerun()

# ------------------------
# Upcoming Movies Section
# ------------------------
def display_upcoming_section():
    """Display upcoming Telugu movies"""
    st.markdown('<h2 class="section-header">🎬 Coming Soon - Telugu Movies</h2>', unsafe_allow_html=True)
    
    upcoming_data = get_upcoming_telugu_movies()
    
    if upcoming_data and 'results' in upcoming_data:
        movies = upcoming_data['results'][:6]
        
        if len(movies) == 0:
            st.info("No upcoming Telugu movies found at this time.")
            return
            
        cols = st.columns(3)
        for idx, movie in enumerate(movies):
            with cols[idx % 3]:
                st.markdown(display_movie_card(movie), unsafe_allow_html=True)
                if st.button(f"View Details", key=f"upcoming_{movie.get('id')}_{idx}"):
                    st.session_state.selected_movie_id = movie.get('id')
                    st.session_state.show_details = True
                    st.rerun()
    else:
        st.info("No upcoming Telugu movies found at this time.")

# ------------------------
# Footer
# ------------------------
def display_footer():
    """Display footer section"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 2rem 0; color: #888;">
        <h3 style="color: #e50914; font-size: 2rem; margin-bottom: 1rem; font-family: 'Poppins', sans-serif;">
            🎬 CineMatch Telugu
        </h3>
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">
            Your Ultimate Telugu Movie Discovery Platform
        </p>
        <p style="font-size: 0.9rem; color: #666;">
            Powered by TMDB API | Data updated in real-time
        </p>
        <p style="font-size: 0.85rem; color: #555; margin-top: 1rem;">
            © 2025 CineMatch Telugu. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------
# Movie Details View
# ------------------------
def display_movie_details_view(movie_id):
    """Display detailed movie information"""
    movie_details = get_movie_details(movie_id)
    
    if not movie_details:
        st.error("Unable to load movie details. Please try again.")
        if st.button("← Back to Movies"):
            st.session_state.show_details = False
            st.session_state.selected_movie_id = None
            st.rerun()
        return
    
    st.markdown("---")
    st.markdown(f"<h2 class='section-header'>🎬 {movie_details.get('title')}</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        poster_url = f"{TMDB_IMAGE_BASE}{movie_details.get('poster_path')}" if movie_details.get('poster_path') else "https://via.placeholder.com/500x750"
        st.image(poster_url, use_column_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="color: #ffffff; line-height: 1.8;">
            <p style="margin-bottom: 1.5rem;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Overview:</span> <span style="color: #f5f5f5;">{movie_details.get('overview', 'N/A')}</span></p>
            <p style="margin-bottom: 1rem;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Rating:</span> <span style="color: #ffd700; font-weight: 600;">⭐ {movie_details.get('vote_average', 0):.1f}/10</span> <span style="color: #f5f5f5;">({movie_details.get('vote_count', 0):,} votes)</span></p>
            <p style="margin-bottom: 1rem;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Release Date:</span> <span style="color: #f5f5f5;">{movie_details.get('release_date', 'N/A')}</span></p>
            <p style="margin-bottom: 1rem;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Runtime:</span> <span style="color: #f5f5f5;">{movie_details.get('runtime', 0)} minutes</span></p>
        """, unsafe_allow_html=True)
        
        if 'genres' in movie_details and movie_details['genres']:
            genres_str = ', '.join([g['name'] for g in movie_details['genres']])
            st.markdown(f'<p style="margin-bottom: 1rem; color: #ffffff;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Genres:</span> <span style="color: #f5f5f5;">{genres_str}</span></p>', unsafe_allow_html=True)
        
        if 'production_companies' in movie_details and movie_details['production_companies']:
            companies = [c['name'] for c in movie_details['production_companies'][:3]]
            st.markdown(f'<p style="margin-bottom: 1rem; color: #ffffff;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Production:</span> <span style="color: #f5f5f5;">{", ".join(companies)}</span></p>', unsafe_allow_html=True)
        
        if 'budget' in movie_details and movie_details['budget'] > 0:
            st.markdown(f'<p style="margin-bottom: 1rem; color: #ffffff;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Budget:</span> <span style="color: #f5f5f5;">${movie_details["budget"]:,}</span></p>', unsafe_allow_html=True)
        
        if 'revenue' in movie_details and movie_details['revenue'] > 0:
            st.markdown(f'<p style="margin-bottom: 1rem; color: #ffffff;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Revenue:</span> <span style="color: #f5f5f5;">${movie_details["revenue"]:,}</span></p>', unsafe_allow_html=True)
        
        # Cast information
        if 'credits' in movie_details and 'cast' in movie_details['credits']:
            cast = movie_details['credits']['cast'][:6]
            if cast:
                st.markdown('<p style="font-weight: 700; color: #ffcccc; margin-bottom: 0.5rem; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Cast:</p>', unsafe_allow_html=True)
                cast_html = '<div style="color: #f5f5f5; line-height: 1.8;">'
                for actor in cast:
                    cast_html += f'<p style="margin-bottom: 0.5rem;">• {actor["name"]} as <span style="color: #ffcccc;">{actor.get("character", "N/A")}</span></p>'
                cast_html += '</div>'
                st.markdown(cast_html, unsafe_allow_html=True)
        
        # Director information
        if 'credits' in movie_details and 'crew' in movie_details['credits']:
            directors = [crew['name'] for crew in movie_details['credits']['crew'] if crew['job'] == 'Director']
            if directors:
                st.markdown(f'<p style="margin-top: 1rem; color: #ffffff;"><span style="font-weight: 700; color: #ffcccc; text-shadow: 0 0 10px rgba(229, 9, 20, 0.5);">Director:</span> <span style="color: #f5f5f5;">{", ".join(directors)}</span></p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Trailer
    trailer_url = get_youtube_trailer_url(movie_id)
    if trailer_url:
        st.markdown('<h3 style="color: #ffffff; font-weight: 700; margin-top: 2rem; text-shadow: 0 0 15px rgba(229, 9, 20, 0.6);">🎬 Watch Trailer</h3>', unsafe_allow_html=True)
        st.markdown(f"""
        <iframe 
            width="100%" 
            height="400" 
            src="{trailer_url}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen
            style="border-radius: 15px; margin-top: 1rem; box-shadow: 0 15px 40px rgba(229, 9, 20, 0.4);">
        </iframe>
        """, unsafe_allow_html=True)
    
    # Reviews section
    if 'reviews' in movie_details and movie_details['reviews'].get('results'):
        st.markdown('<h3 style="color: #ffffff; font-weight: 700; margin-top: 2rem; text-shadow: 0 0 15px rgba(229, 9, 20, 0.6);">📝 Reviews</h3>', unsafe_allow_html=True)
        reviews = movie_details['reviews']['results'][:3]
        for review in reviews:
            with st.expander(f"Review by {review.get('author', 'Anonymous')}", expanded=False):
                st.markdown(f'<p style="color: #ffd700; font-weight: 600; margin-bottom: 0.5rem;">Rating: {review.get("author_details", {}).get("rating", "N/A")}/10</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="color: #f5f5f5; line-height: 1.8;">{review.get("content", "No content")[:500]}...</p>', unsafe_allow_html=True)
    
    if st.button("← Back to Movies"):
        st.session_state.show_details = False
        st.session_state.selected_movie_id = None
        st.rerun()

# ------------------------
# Main Application Entry Point
# ------------------------
def main():
    """Main application function"""
    # Load CSS
    load_advanced_css()
    
    # Initialize session state
    if 'show_details' not in st.session_state:
        st.session_state.show_details = False
    if 'selected_movie_id' not in st.session_state:
        st.session_state.selected_movie_id = None
    
    # Check if viewing movie details
    if st.session_state.get('show_details') and st.session_state.get('selected_movie_id'):
        display_movie_details_view(st.session_state.selected_movie_id)
        return
    
    # Display main sections
    display_telugu_hero_carousel()
    
    # Search and filter
    search_query, selected_genre, selected_year, selected_sort = display_search_filter_section()
    
    # Display movies grid
    display_movies_grid(search_query, selected_genre, selected_year, selected_sort)
    
    # Display additional sections
    st.markdown("---")
    display_trending_section()
    
    st.markdown("---")
    display_upcoming_section()
    
    st.markdown("---")
    display_recommendations_section()
    
    # Footer
    display_footer()

# Run the application
if __name__ == "__main__":
    main()