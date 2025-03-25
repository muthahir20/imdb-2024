import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import altair as alt
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

USERNAME = "kCCeTyfqG4q97x6.root"
PASSWORD = "O5K4JarXblpcn7gg"
HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"  
PORT = 4000  
DATABASE = "imdb"

#Create SQLAlchemy Engine
@st.cache_resource  # Caches the connection for better performance
def get_engine():
    return create_engine(f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

engine = get_engine()


#methods for fetching data from DB and return as dataframe
def fetch_top_ten_movies():
    query = "SELECT distinct title, rating, vote_count, (rating * LOG(vote_count + 1)) AS weighted_score FROM imdb.movies_2024 ORDER BY weighted_score DESC LIMIT 10"
    return pd.read_sql(query, engine)

def fetch_genre_data():
    query = "SELECT genres, COUNT(*) as movie_count FROM imdb.movies_2024 GROUP BY genres"
    return pd.read_sql(query, engine)

def fetch_avg_duration():
    query = """
        SELECT genres, AVG(TIME_TO_SEC(duration) / 60) AS avg_duration 
        FROM imdb.movies_2024
        GROUP BY genres
    """
    return pd.read_sql(query, engine)

def fetch_voting_trends():
    query = """
        SELECT genres, AVG(vote_count) AS avg_votes 
        FROM movies_2024 
        GROUP BY genres
    """
    return pd.read_sql(query, engine)

def fetch_ratings():
    query = "SELECT rating FROM imdb.movies_2024 WHERE rating IS NOT NULL"
    return pd.read_sql(query, engine)

def fetch_top_movies():
    query = """
        WITH RankedMovies AS (
            SELECT genres, title, rating,
                   RANK() OVER (PARTITION BY genres ORDER BY rating DESC) AS ranking
            FROM imdb.movies_2024
        )
        SELECT genres, title, rating FROM RankedMovies WHERE ranking = 1;
    """
    return pd.read_sql(query, engine)

def genre_by_vote():
     query = """
        SELECT genres, SUM(vote_count) AS total_votes
        FROM imdb.movies_2024
        GROUP BY genres
        ORDER BY total_votes DESC
        """
     return pd.read_sql(query,engine)

def movie_duration():
     query = """
        (SELECT title, genres, duration FROM imdb.movies_2024 where duration <> "00:00:00" ORDER BY duration ASC LIMIT 1)
        UNION
        (SELECT title, genres, duration FROM imdb.movies_2024 ORDER BY duration DESC LIMIT 1)
        """
     return pd.read_sql(query,engine)

def rating_by_gener():
    query = """
        SELECT genres, ROUND(AVG(rating), 2) AS avg_rating
        FROM imdb.movies_2024
        GROUP BY genres
        ORDER BY avg_rating DESC
       """
    return pd.read_sql(query,engine)

def hist_movie_rating():
    query = "SELECT title, rating FROM imdb.movies_2024 WHERE rating IS NOT NULL"
    return pd.read_sql(query,engine)

def rating_vs_count():
     query = """
        SELECT title, rating, vote_count, genres
        FROM imdb.movies_2024
        WHERE rating IS NOT NULL AND vote_count IS NOT NULL
        """
     return pd.read_sql(query,engine)

def filter():
    query = """
        SELECT title, rating, vote_count, TIME_TO_SEC(duration) / 60 as mins, genres
        FROM imdb.movies_2024
        WHERE rating IS NOT NULL AND vote_count IS NOT NULL
        """
    return pd.read_sql(query,engine)

#data frames
df_avg_duration = fetch_avg_duration()
df_avg_count = fetch_voting_trends()
df_hist_rating=hist_movie_rating()
df_genre_by_vote=genre_by_vote()
df_top_movies_genre=fetch_top_movies()
df_movie_duraion=movie_duration()
df_rating_by_genre=rating_by_gener()
df_rating_vs_count=rating_vs_count()
df_filter=filter()



if st.sidebar.button("About Project"):
     st.header("IMDB Movies Analysis 2024")
     justified_text="""<p style='text-align: justify;'> This project focuses on extracting and analyzing movie data from IMDb for the year 2024.
               The task involves scraping data such as movie names, genres, ratings, voting counts, and durations from 
              IMDb's 2024 movie list using Selenium. The data will then be organized genre-wise, saved as individual CSV files, 
              and combined into a single dataset stored in an SQL database. Finally, the project will provide interactive 
              visualizations and filtering functionality using Streamlit to answer key questions and allow users to customize 
              their exploration of the dataset. 
              </p>
     """
     st.markdown(justified_text, unsafe_allow_html=True)


st.sidebar.header("Business Use Cases:")

if st.sidebar.button("Top 10 Movies "):
    st.subheader("2024 Top 10 Movies")
    df_top_ten_movie = fetch_top_ten_movies()
    df_top_ten_movie=df_top_ten_movie.drop(columns=["weighted_score"])
    df_top_ten_movie=df_top_ten_movie.rename(columns={"title": "Movie Name","rating": "Rating","vote_count": "Voting Count"})
    df_top_ten_movie.index=range(1,len(df_top_ten_movie)+1)
    st.dataframe(df_top_ten_movie)  


if st.sidebar.button("Genre Distribution"):
    st.subheader("Movie counts by Genre")  
    df_genre_distribution = fetch_genre_data()
    st.bar_chart(df_genre_distribution.set_index("genres"))


if st.sidebar.button("Average Duration"):
    chart_avg_duration = alt.Chart(df_avg_duration).mark_bar().encode(
    y=alt.Y("genres:N", sort="-x"),
    x="avg_duration:Q",
    color=alt.Color("genres:N", scale=alt.Scale(scheme="category20b")),
    tooltip=["genres", "avg_duration"]
    ).properties(
    title="Average Movie Duration by Genre",
    width=600,
    height=400
    )
     
    st.altair_chart(chart_avg_duration, use_container_width=True)

if st.sidebar.button("Voting Trends by Genre"):
    chart_vote_count = alt.Chart(df_avg_count).mark_bar().encode(
    x=alt.X("genres:N", sort="-y"),
    y="avg_votes:Q",
    color=alt.Color("genres:N", scale=alt.Scale(scheme="category20b")),
    tooltip=["genres", "avg_votes"]
    ).properties(
    title="Voting Trends by Genre",
    width=600,
    height=400
    )
    
    st.altair_chart(chart_vote_count, use_container_width=True)

if st.sidebar.button("Rating Distribution"):
    hist_rating_distribution= alt.Chart(df_hist_rating).mark_bar().encode(
    x=alt.X("rating:Q", bin=alt.Bin(maxbins=20), title="Movie Ratings"),
    y=alt.Y("count()", title="Frequency"),
    tooltip=["count()"]
    ).properties(
    title=" Histogram of Movie Ratings",
    width=600
    )

    st.altair_chart(hist_rating_distribution, use_container_width=True)

if st.sidebar.button("Top movies by Genre"):
    st.header("Top-Rated Movies by Genre")
    df_top_movies_genre.index=range(1,len(df_top_movies_genre)+1)
    st.dataframe(df_top_movies_genre)

if st.sidebar.button("Most Popular Genres by Voting"):
    fig = px.pie(
        df_genre_by_vote,
        names="genres",
        values="total_votes",
        title="Most Popular Genres by Total Votes",
        color_discrete_sequence=px.colors.qualitative.Set3  # Color theme
    )

    st.plotly_chart(fig, use_container_width=True)

if st.sidebar.button("Short and Long Movie"):
    st.subheader("Shortest and Longest Duration Movies")
    df_movie_duraion.index=range(1,len(df_movie_duraion)+1)
    st.table(df_movie_duraion) 

if st.sidebar.button("Average Rating by Genres"):
    st.subheader(" Average ratings across genres")
    fig_avg_rating, ax = plt.subplots(figsize=(10, 5))
    genre_ratings = df_rating_by_genre.pivot_table(index="genres", values="avg_rating")
    
    sns.heatmap(genre_ratings, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
    ax.set_title("Heatmap of Average Ratings by Genre")

    st.pyplot(fig_avg_rating)

if st.sidebar.button("Rating Vs Count"):
     fig_rating_vs_count = px.scatter(
        df_rating_vs_count, 
        x="rating", 
        y="vote_count", 
        color="genres", 
        hover_data=["title"],
        title="Relationship Between Ratings & Voting Counts",
        labels={"rating": "IMDb Rating", "vote_count": "Number of Votes"},
        size_max=10,
        opacity=0.7
        )
     st.plotly_chart(fig_rating_vs_count)
     

if "show_filters" not in st.session_state:
    st.session_state["show_filters"] = False

    
if st.sidebar.button("Filter Movies"):
     st.session_state["show_filters"] = not st.session_state["show_filters"]

if st.session_state["show_filters"]:
    st.subheader("Filter Movies")

    col1, col2, col3 = st.columns(3)
 
        
    with col1:
            genres = df_filter["genres"].unique().tolist()
            selected_genres = st.multiselect("Select Genre(s)", genres, default=["Action"])
      
    with col2:
            min_rating = st.slider("Minimum IMDb Rating", min_value=0.0, max_value=10.0, value=8.0, step=0.1)
     
    with col3:
            min_votes = st.number_input("Minimum Vote Count", min_value=0, value=50000, step=1000)
        
    duration_filter = st.selectbox("Select Movie Duration", ["All", "< 2 hrs", "2–3 hrs", "> 3 hrs"])
       
    filtered_df = df_filter[
            (df_filter["rating"] >= min_rating) &
            (df_filter["vote_count"] >= min_votes) &
            (df_filter["genres"].isin(selected_genres))
        ]
        
    if duration_filter == "< 2 hrs":
            filtered_df = filtered_df[filtered_df["mins"] < 120]
    elif duration_filter == "2–3 hrs":
            filtered_df = filtered_df[(filtered_df["mins"] >= 120) & (filtered_df["mins"] <= 180)]
    elif duration_filter == "> 3 hrs":
            filtered_df = filtered_df[filtered_df["mins"] > 180]

    st.subheader("Filtered Movies")
    filtered_df.index=range(1,len(filtered_df)+1)
    filtered_df=filtered_df.rename(columns={"title": "Movie Name",
                                            "rating": "Rating",
                                            "vote_count": "Voting Count",
                                            "mins": "Duration (mins)",
                                            "genres": "Genres"
                                            })
    st.dataframe(filtered_df)

    