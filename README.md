# IMDB movies analysis for the year 2024

# Project Overview
This project focuses on extracting and analyzing movie data from IMDb for the year 2024. The task involves:

1. Scraping movie details such as names, genres, ratings, voting counts, and durations from IMDb using Selenium.

2. Organizing data by genre and saving them as individual CSV files.

3. Merging the CSV files into a single dataset and storing it in an SQL database.

4. Providing interactive visualizations and filtering functionality using Streamlit to explore key trends in the dataset.

# Features
1. Data Scraping: Extract movie details dynamically from IMDb.

2. Data Storage: Organize and store data in an SQL database (TiDB).

3. Interactive Filtering: Filter movies based on genre, rating, duration, and voting count.

4. Visualizations: Generate interactive charts including histograms, bar charts, scatter plots, and heatmaps to analyze trends.

# Technologies Used
1. Python (Pandas, Selenium, SQLAlchemy, Streamlit, Plotly, Matplotlib, Seaborn)

2. SQL (TiDB for database storage)

3. Streamlit (For interactive web-based analysis)

# Business Use Case
1. Top 10 Movies by Rating and Voting Counts: Identify movies with the highest ratings and significant voting engagement.
2. Genre Distribution: Plot the count of movies for each genre in a bar chart.
3. Average Duration by Genre: Show the average movie duration per genre in a horizontal bar chart.
4. Voting Trends by Genre: Visualize average voting counts across different genres.
5. Rating Distribution: Display a histogram of movie ratings.
6. Genre-Based Rating Leaders: Highlight the top-rated movie for each genre in a table.
7. Most Popular Genres by Voting: Identify genres with the highest total voting counts in a pie chart.
8. Duration Extremes: Use a table or card display to show the shortest and longest movies.
9. Ratings by Genre: Use a heatmap to compare average ratings across genres.
10. Correlation Analysis: Analyze the relationship between ratings and voting counts using a scatter plot.

