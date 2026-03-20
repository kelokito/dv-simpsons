import altair as alt
import pandas as pd
import streamlit as st


JUSTIFICATION_TEXT = """
We have decided to just compare the number of viewers in two days of the week: 
Sunday and Thursday, as they are the most common days for airing episodes. 
The other three only have 1 or 2 days of airing and in order to make a comparison we need a minimum number of episodes for each day.


and also print a tendency line from avg season 2 to avg season 5 and another one from avg season 6 to avg season 9, to see if there is a change in the tendency of viewers across the seasons. 
if the tendency line from season 2 to 5 has a negative slope and the one from season 6 to 9 has a negative slope, 
    it could be comparable
"""

# 1. Cache the data loading separately so it's fast!
@st.cache_data
def load_data(path="../data/simpsons_episodes_cleaned.csv"):
    print("Loading data from disk...")  # This will only print once, thanks to caching!
    print(f"Data loaded from: {path}")
    df = pd.read_csv(path)
    return df

# 2. Preprocess the data to format dates and filter days
def preprocess_data(df):
    # Convert dates to actual datetime objects so Altair and Pandas can do math on them
    df['original_air_date'] = pd.to_datetime(df['original_air_date'])
    
    # Select only the episodes aired on Sunday and Thursday
    df = df[df['day_aired'].isin(['Sunday', 'Thursday'])]
    return df
    
def render_q4_justification():
    # Initialize the section with a divider and a header, then add the justification text
    st.divider()
    st.markdown("### Justification")
    st.write(JUSTIFICATION_TEXT)

def render_q4_view(path="../data/simpsons_episodes_cleaned.csv"):
    # Load and preprocess the cached data
    df = load_data(path)
    df = preprocess_data(df)

    st.markdown("### Viewers by Weekday")
    st.write("First, let's look at the average viewership by season, split by the two most common airing days (Sunday and Thursday).")

    # ---------------------------------------------------------
    # CHART 1: Scatter + Line (Season vs Viewers by Weekday)
    # ---------------------------------------------------------
    scatter = alt.Chart(df).mark_circle(opacity=0.4, size=60).encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('us_viewers_in_millions:Q', title='Viewers (Millions)'),
        color=alt.Color('day_aired:N', title='Day Aired'),
        tooltip=['season', 'number_in_season', 'us_viewers_in_millions', 'day_aired']
    )
    
    line = alt.Chart(df).mark_line(strokeWidth=3).encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('mean(us_viewers_in_millions):Q', title='Viewers (Millions)'),
        color=alt.Color('day_aired:N', title='Day Aired')
    )

    final_chart_1 = (scatter + line).properties(
        width=700, 
        height=400,
        title='US Viewers by Season and Weekday'
    )
    st.altair_chart(final_chart_1, use_container_width=True)

    # ---------------------------------------------------------
    # CHART 2: Timeline with Season Limits and Trendlines
    # ---------------------------------------------------------
    st.markdown("#### Viewership Timeline and Shift in Tendency")
    st.write("Below is a timeline of all Sunday and Thursday episodes. We have added tendency lines for **Seasons 2-5** and **Seasons 6-9** to compare the slopes and see if the negative viewer trend is comparable between these two distinct eras.")

    # Base line chart over time
    line_chart = alt.Chart(df).mark_line(opacity=0.6).encode(
        x=alt.X('original_air_date:T', title='Original Air Date'),
        y=alt.Y('us_viewers_in_millions:Q', title='US Viewers (Millions)'),
        color=alt.Color('day_aired:N', title='Day Aired')
    )

    # Vertical limit bounds for the last episode of the season
    season_finals = df[df['is_last_episode'] == 1].copy()
    limit_bounds = alt.Chart(season_finals).mark_rule(color='black', strokeDash=[4, 4], opacity=0.4).encode(
        x=alt.X('original_air_date:T'),
        tooltip=[alt.Tooltip('season:N', title='Season')]
    )

    # Midpoint labels for seasons
    season_ranges = (
        df.groupby('season', as_index=False)
          .agg(
              start_date=('original_air_date', 'min'),
              end_date=('original_air_date', 'max')
          )
    )
    # Calculate mid date (using /2 to put the label exactly in the middle of the season)
    season_ranges['mid_date'] = season_ranges['start_date'] + (season_ranges['end_date'] - season_ranges['start_date']) / 2
    season_ranges['label_y'] = df['us_viewers_in_millions'].max() * 1.03
    season_ranges['season_label'] = 'S' + season_ranges['season'].astype(str)

    season_labels = alt.Chart(season_ranges).mark_text(
        dy=-4,
        color='black',
        fontSize=11
    ).encode(
        x=alt.X('mid_date:T'),
        y=alt.Y('label_y:Q'),
        text=alt.Text('season_label:N', title='Season')
    )

    # Tendency Line 1: Seasons 2 to 5
    trend_s2_s5 = alt.Chart(df).transform_filter(
        (alt.datum.season >= 2) & (alt.datum.season <= 5)
    ).transform_regression(
        'original_air_date', 'us_viewers_in_millions'
    ).mark_line(color='red', strokeWidth=4).encode(
        x=alt.X('original_air_date:T'),
        y=alt.Y('us_viewers_in_millions:Q')
    )

    # Tendency Line 2: Seasons 6 to 9
    trend_s6_s9 = alt.Chart(df).transform_filter(
        (alt.datum.season >= 6) & (alt.datum.season <= 9)
    ).transform_regression(
        'original_air_date', 'us_viewers_in_millions'
    ).mark_line(color='darkred', strokeWidth=4).encode(
        x=alt.X('original_air_date:T'),
        y=alt.Y('us_viewers_in_millions:Q')
    )

    # Combine all elements into Chart 2
    final_chart_2 = (line_chart + limit_bounds + season_labels + trend_s2_s5 + trend_s6_s9).properties(
        height=450,
        title='US Viewers Over Time (with Trends for S2-S5 & S6-S9)'
    )
    
    # Render the timeline chart
    st.altair_chart(final_chart_2, use_container_width=True)

    # Render justification at the bottom
    render_q4_justification()