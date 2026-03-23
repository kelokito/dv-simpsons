import altair as alt
import pandas as pd
import streamlit as st

JUSTIFICATION_TEXT = """
We have decided to just compare the number of viewers in two days of the week: 
Sunday and Thursday, as they are the most common days for airing episodes. 
The other three only have 1 or 2 days of airing and in order to make a comparison we need a minimum number of episodes for each day.
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

    df['season_dec'] = df['season'] + -0.5 + (df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')) 

    # 2. CRITICAL CALCULATION STEP: Sort by date so yi-1 is actually the previous episode
    df = df.sort_values('original_air_date')

    # 3. Calculate yi - yi-1 (The difference in viewers from the previous episode)
    # Note: If you want the difference from the previous episode OF THE SAME DAY, 
    # you should use: df.groupby('day_aired')['us_viewers_in_millions'].diff()
    df['viewers_diff'] = df['us_viewers_in_millions'].diff()

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
    st.altair_chart(final_chart_1, width='stretch')

    # ---------------------------------------------------------
    # CHART 2: Timeline with Season Limits and Trendlines
    # ---------------------------------------------------------
    st.markdown("#### Viewership Timeline and Shift in Tendency")
    st.write("Below is a timeline of all Sunday and Thursday episodes. We have added tendency lines for **Seasons 2-5**, **Seasons 6-9**, and an overall trend for **Seasons 2-9** to compare slopes and visualize the viewership decline.")

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

    # Tendency Line 1: Seasons 2 to 5 (Red)
    trend_s2_s5 = alt.Chart(df).transform_filter(
        (alt.datum.season >= 2) & (alt.datum.season <= 5)
    ).transform_regression(
        'original_air_date', 'us_viewers_in_millions'
    ).mark_line(color='red', strokeWidth=4).encode(
        x=alt.X('original_air_date:T'),
        y=alt.Y('us_viewers_in_millions:Q')
    )

    # Tendency Line 2: Seasons 6 to 9 (Dark Red)
    trend_s6_s9 = alt.Chart(df).transform_filter(
        (alt.datum.season >= 6) & (alt.datum.season <= 9)
    ).transform_regression(
        'original_air_date', 'us_viewers_in_millions'
    ).mark_line(color='darkred', strokeWidth=4).encode(
        x=alt.X('original_air_date:T'),
        y=alt.Y('us_viewers_in_millions:Q')
    )

    # NEW OVERALL Tendency Line 3: Seasons 2 to 9 (Blue Dashed)
    # NEW OVERALL Tendency Line 3: Seasons 2 to 9 (Blue Dashed)
    trend_s2_s9 = alt.Chart(df).transform_filter(
        (alt.datum.season >= 2) & (alt.datum.season <= 9)
    ).transform_regression(
        'original_air_date', 'us_viewers_in_millions'
    ).mark_line(color='blue', strokeWidth=3, strokeDash=[5, 5]).encode(
        # THE BUG IS HERE ⬇️
        x=alt.X('original_air_date:T'), 
        y=alt.Y('us_viewers_in_millions:Q')
    )

    # Combine all elements into Chart 2
    final_chart_2 = (line_chart + limit_bounds + season_labels + trend_s2_s5 + trend_s6_s9 + trend_s2_s9).properties(
        height=450,
        title='US Viewers Over Time (with Trends for S2-S5, S6-S9, and Overall S2-S9)'
    )
    
    # Render the timeline chart
    st.altair_chart(final_chart_2, width='stretch')

    # ---------------------------------------------------------
    # CALCULATE METRICS FOR CONCLUSION
    # ---------------------------------------------------------
    # Calculate average viewers for Sunday and Thursday
    sunday_avg = df[df['day_aired'] == 'Sunday']['us_viewers_in_millions'].mean()
    thursday_avg = df[df['day_aired'] == 'Thursday']['us_viewers_in_millions'].mean()
    
    # Calculate the ratio
    day_multiplier = sunday_avg / thursday_avg
    
    # Render the conclusion block
    st.divider()
    st.markdown("### Conclusions")
    
    st.write("By plotting the tendency line from **Season 2 to Season 9** (dashed blue line) alongside the era-specific trends, we can observe the following:")
    
    st.info("While both the Season 2–5 era and the Season 6–9 era display negative slopes, the tendency line from Season 6 to 9 is visibly steeper. This indicates a sharper decline in viewership during that later era compared to the earlier seasons.")
    
    st.success(f"Furthermore, across our dataset, an episode aired on **Sunday** averages **{sunday_avg:.2f} million** viewers, whereas an episode aired on **Thursday** averages **{thursday_avg:.2f} million**. Therefore, it is roughly **{day_multiplier:.2f}x better** (or an increase of about {(day_multiplier - 1) * 100:.1f}%) to air an episode on Sunday rather than Thursday.")

    # Render justification at the very bottom
    render_q4_justification()

def show_q4_view(path="../data/simpsons_episodes_cleaned.csv"):
    # 1. Load and preprocess the cached data
    df = load_data(path)
    df = preprocess_data(df)


    # 4. Generate the Density Area Chart
    area = alt.Chart(df[abs(df['viewers_diff']) < 10]).transform_density(
        'viewers_diff',
        as_=['viewers_diff', 'density'],
        groupby=['day_aired']
    ).mark_area(opacity=0.7).encode(
        x=alt.X('viewers_diff:Q', 
                title='Number of Viewers Change (yi - yi-1)', 
                axis=alt.Axis(format=',.0f'), 
                scale=alt.Scale(domain=(-10, 10))),
        y=alt.Y('density:Q', 
                title='Density', 
                scale=alt.Scale(domain=(0, 0.5))),
        color=alt.Color(
            'day_aired:N',
            title='Day Aired',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#de2157', '#21DEA8']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        )
    ).properties(
        title='Density of Viewership Changes (Removing the Tendency) by Weekday',
        height=450
    )

    # 5. Render to Streamlit (Use container width so it aligns nicely with your other charts)
    st.altair_chart(area, use_container_width=True)