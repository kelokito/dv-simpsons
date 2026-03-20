import altair as alt
import pandas as pd
import streamlit as st

# 1. Cache the data loading separately so it's fast!
@st.cache_data
def load_data(path="../data/simpsons_episodes_cleaned.csv"):
    return pd.read_csv(path)

# 2. This function builds the whole Q3 section
def render_q3_view():
    # Load the cached data
    df = load_data()

    st.markdown("### Ratings vs. Viewership Correlation")
    st.write("Does a highly-rated episode guarantee a massive audience? Let's look at the relationship between IMDb ratings and US viewership.")

    # ---------------------------------------------------------
    # CHART 1: Scatter Plot with Trendline
    # ---------------------------------------------------------
    st.markdown("#### 1. Overall Correlation (Scatter Plot)")
    
    # Base scatter plot
    scatter = alt.Chart(df).mark_circle(size=60, opacity=0.5).encode(
        x=alt.X('imdb_rating:Q', title='IMDb Rating', scale=alt.Scale(zero=False)),
        y=alt.Y('us_viewers_in_millions:Q', title='US Viewers (Millions)'),
        tooltip=['title', 'season', 'imdb_rating', 'us_viewers_in_millions']
    )
    
    # Add a regression line (trendline) to show the correlation path clearly
    trendline = scatter.transform_regression('imdb_rating', 'us_viewers_in_millions').mark_line(color='red', strokeWidth=3)
    
    chart1 = (scatter + trendline).properties(height=400)
    st.altair_chart(chart1, use_container_width=True)

    # ---------------------------------------------------------
    # CHART 2: Dual-Axis Line Chart over Time
    # ---------------------------------------------------------
    st.markdown("#### 2. Trends Over Time (Dual-Axis Line Chart)")
    st.write("To see if they trended together over the years, we can plot the average ratings and viewership season by season on a dual axis.")

    # For a clean line chart, it's usually best to aggregate by season first 
    # so it doesn't look like a chaotic scribble of 600+ episodes.
    season_df = df.groupby('season').agg({
        'us_viewers_in_millions': 'mean',
        'imdb_rating': 'mean'
    }).reset_index()

    # Base chart for the X-axis (Season)
    base = alt.Chart(season_df).encode(
        x=alt.X('season:O', title='Season')
    )

    # First line: Viewers (Blue)
    line_viewers = base.mark_line(color='#1f77b4', strokeWidth=3).encode(
        y=alt.Y('us_viewers_in_millions:Q', 
                title='Average Viewers (Millions)', 
                axis=alt.Axis(titleColor='#1f77b4'))
    )

    # Second line: Ratings (Orange)
    line_ratings = base.mark_line(color='#ff7f0e', strokeWidth=3).encode(
        y=alt.Y('imdb_rating:Q', 
                title='Average IMDb Rating', 
                axis=alt.Axis(titleColor='#ff7f0e'), 
                scale=alt.Scale(zero=False)) # Don't start ratings at 0 to see the curve better
    )

    # Combine them and resolve the Y-axis so they stay independent
    chart2 = alt.layer(line_viewers, line_ratings).resolve_scale(y='independent').properties(height=400)
    
    st.altair_chart(chart2, use_container_width=True)