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
    df['season'] = pd.Categorical(df['season'], ordered=True)

    # FIX 2: Indented all the Altair code so it sits inside the function
    line = alt.Chart(df).transform_aggregate(
        mean_viewers='mean(us_viewers_in_millions)',
        groupby=['season']
    ).mark_line().encode(
        x=alt.X('season:Q', title='Season', axis=alt.Axis(tickCount=26), scale=alt.Scale(domain=[0, 28])),
        y=alt.Y('mean_viewers:Q', title='Average US Viewers (Millions)'),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('mean_viewers:Q', title='Average US Viewers (Millions)', format='.2f')
        ]
    ).properties(
        title='Average US Viewers by Season'
    )

    point = alt.Chart(df).mark_circle(size=50, opacity=0.5, color='orange').encode(
        # Note: Make sure 'season_dec' is a real column in your CSV!
        x=alt.X('season_dec:Q', title='Season', scale=alt.Scale(domain=[1, 28])),
        y=alt.Y('us_viewers_in_millions:Q', title='US Viewers (Millions)'),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('us_viewers_in_millions:Q', title='US Viewers (Millions)', format='.2f')
        ]
    )

    # FIX 3: Apply properties and render the chart in Streamlit
    chart = (line + point).properties(width=800, height=500)
    st.altair_chart(chart, use_container_width=True)