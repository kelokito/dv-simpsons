import altair as alt
import pandas as pd
import streamlit as st

# 1. Cache the data loading separately so it's fast!
@st.cache_data
def load_data(path="../data/simpsons_episodes_cleaned.csv"):
    print("Loading data from disk...")  # This will only print once, thanks to caching!
    print(f"Data loaded from: {path}")
    return pd.read_csv(path)

# 2. Preprocess the data to create a 'season_dec' column for better x-axis positioning
def preprocess_data(df):
    # We create a 'season_dec' column that adds a small offset to the season number based on the episode's position within the season.
    df['season_dec'] = df['season'] + -0.5 + (df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')) 
    return df
    

def render_q2_justification():
    
    st.divider()
    # --- ADD A SECOND CHART (Optional Example) ---
    st.markdown("### Justification")



# 2. This function now builds the whole section
def render_q2_view():
    # Load the cached data
    df = load_data()
    df = preprocess_data(df)

    # --- ADD YOUR TEXT HERE ---
    st.markdown("### The Evolution of Viewers")
    st.write("This line chart shows the number of viewers for each episode across all seasons. We can see how the viewership has evolved over time, with peaks in the early seasons and a general decline in later seasons...")

    # FIX 1: Changed df2 to df to match the loaded variable above
    df['season_05'] = df['season'] + 0.5

    df['season_dec'] = df['season'] + (df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')) 



    # FIX 2: Indented all the Altair code so it sits inside the function
    line = alt.Chart(df).transform_aggregate(
        mean_viewers='mean(us_viewers_in_millions)',
        season='mean(season)',
        groupby=['season_05']
    ).transform_calculate(
        series="'Season average'"
    ).mark_line(strokeWidth=3,tooltip=False).encode(
        x=alt.X('season_05:Q', title='Season', axis=alt.Axis(tickCount=26), scale=alt.Scale(domain=[1, 28])),
        y=alt.Y('mean_viewers:Q', title='US Viewers (Millions)'),
        tooltip=[
            alt.Tooltip('season:Q', title='Season', format='.0f'),
            alt.Tooltip('mean_viewers:Q', title='US Viewers (Millions)', format='.2f')
        ]
    ).properties(
        title='Average US Viewers by Season'
    )
    
    avg_point = alt.Chart(df).transform_aggregate(
        mean_viewers='mean(us_viewers_in_millions)',
        season='mean(season)',
        groupby=['season_05']
    ).mark_point(size=90, filled=True, stroke='white', strokeWidth=1.5).encode(
        x=alt.X('season_05:Q', title='Season', axis=alt.Axis(tickCount=26), scale=alt.Scale(domain=[1, 28])),
        y=alt.Y('mean_viewers:Q', title='US Viewers (Millions)'),
        color=alt.value('#1f77b4'),
        tooltip=[
            alt.Tooltip('season:Q', title='Season', format='.0f'),
            alt.Tooltip('mean_viewers:Q', title='US Viewers (Millions)', format='.2f')
        ]
    )

    point = alt.Chart(df).transform_calculate(
        series="'Individual episode'"
    ).mark_circle(size=50, opacity=0.5).encode(
        # Note: Make sure 'season_dec' is a real column in your CSV!
        x=alt.X('season_dec:Q', title='Season', scale=alt.Scale(domain=[1, 28])),
        y=alt.Y('us_viewers_in_millions:Q'),
        color=alt.Color(
            'series:N',
            title='',
            scale=alt.Scale(domain=['Individual episode', 'Season average'], range=['orange', '#1f77b4']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        ),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('number_in_season:O', title='Episode Number'),
             alt.Tooltip('title:N', title='Episode Title'),
            alt.Tooltip('us_viewers_in_millions:Q', title='US Viewers (Millions)', format='.2f')
        ]
    )



    

    # FIX 3: Apply properties and render the chart in Streamlit
    chart = (line + point + avg_point).properties(width=800, height=500)
    st.altair_chart(chart, use_container_width=True)