import altair as alt
import pandas as pd
import streamlit as st


JUSTIFICATION_TEXT = """
we have understand this question as if there is a pattern intraseason if there is a pattern in number of viewers across the seasons.
in order to answer the question we have decided to use a line chart with the number of viewers in the y-axis and the number of episode normalized in the x-axis.
We have defined as "number_of_episode_normalized" the number of episode divided by the total number of episodes in the season, 
so that we can compare the pattern across seasons with different number of episodes."
We have defined finally a line based on quantiles of 5 () in order to make the pattern more clear and the trend more visible
In order to make the pattern more clear we have added a line of best fit for each season, so that we can see if there is a general trend 
in the number of viewers across the seasons.

"""
# 1. Cache the data loading separately so it's fast!
@st.cache_data
def load_data(path="../data/simpsons_episodes_cleaned.csv"):
    return pd.read_csv(path)

def render_q5_justification():
    # Initialize the section with a divider and a header, then add the justification text
    st.divider()
    st.markdown("### Justification")
    st.markdown(JUSTIFICATION_TEXT)

# 2. Preprocess the data to create the normalized and quantile columns
def preprocess_data(df):
    # Create the normalized episode progression (values from ~0.0 to 1.0)
    df['number_of_episode_normalized'] = df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')
    
    # Split the season into 20 phases (0 to 19)
    df['number_of_episode_normalized_quantiles'] = pd.qcut(df['number_of_episode_normalized'], q=10, labels=False)

    df['number_of_viewers_percentage'] = df.groupby('season')['us_viewers_in_millions'].transform(lambda x: x / x.sum() * 100)
    return df

def render_q5_view(path="../data/simpsons_episodes_cleaned.csv"):
    # Load and preprocess the data
    df = load_data(path)
    df = preprocess_data(df)

    st.write("This chart shows the number of viewers for each episode across all seasons, normalized by the total number of episodes in each season. The red line of best fit (grouped by 5 quantiles) helps us identify the general trend in viewership as a season progresses.")

    # --- CONFIGURE CHARTS ---
    
    # Chart 1: Scatter plot of all episodes using the continuous normalized variable
    scatter = alt.Chart(df[df['number_of_viewers_percentage'] < 6]).mark_circle(opacity=0.4, size=40, color='#1f77b4').encode(
        x=alt.X('number_of_episode_normalized:Q', title='Season Progression (Normalized 0 to 1)'),
        y=alt.Y('number_of_viewers_percentage:Q', title='Viewers as % of Season Total'),
        tooltip=['season', 'number_in_season', 'number_of_viewers_percentage','us_viewers_in_millions','number_of_episode_normalized']
    )

    # Chart 2: The quantile trendline you requested!
    # We group by your new quantile variable and calculate the mean for both X and Y
    trend_line = alt.Chart(df).mark_line(color='red', strokeWidth=4, point=True).encode(
        x=alt.X('mean(number_of_episode_normalized):Q'), 
        y=alt.Y('mean(number_of_viewers_percentage):Q',scale=alt.Scale(domain=(3, 6))),
        tooltip=[
            alt.Tooltip('number_of_episode_normalized_quantiles:O', title='Season Phase (Quantile)'),
            alt.Tooltip('mean(number_of_viewers_percentage):Q', title='Average percentage of viewers', format='.2f')
        ]
    )

    # Combine the scatter plot and the quantile trendline
    final_chart_percentage = (trend_line + scatter).properties(
        width=700, 
        height=400,
        title="Intraseasonal Viewership Pattern (percentage of season total)")


    scatter = alt.Chart(df).mark_circle(opacity=0.4, size=40, color='#1f77b4').encode(
        x=alt.X('number_of_episode_normalized:Q', title='Season Progression (Normalized 0 to 1)'),
        y=alt.Y('us_viewers_in_millions:Q', title='Viewers as % of Season Total'),
        tooltip=['season', 'number_in_season', 'number_of_viewers_percentage','us_viewers_in_millions']
    )

    # Chart 2: The quantile trendline you requested!
    # We group by your new quantile variable and calculate the mean for both X and Y
    trend_line = alt.Chart(df).mark_line(color='red', strokeWidth=4, point=True).encode(
        x=alt.X('mean(number_of_episode_normalized):Q'), 
        y=alt.Y('mean(us_viewers_in_millions):Q'),
        tooltip=[
            alt.Tooltip('number_of_episode_normalized_quantiles:O', title='Season Phase (Quantile)'),
            alt.Tooltip('mean(us_viewers_in_millions):Q', title='Average viewers (millions)', format='.2f')
        ]
    )

    # Combine the scatter plot and the quantile trendline
    final_chart_absolute = (scatter + trend_line).properties(
        width=700, 
        height=400,
        title="Intraseasonal Viewership Pattern (absolute viewers in millions)"
    )


    # Render it in Streamlit
    st.altair_chart(final_chart_percentage)
    st.altair_chart(final_chart_absolute)

    # Render the text block below the chart
    render_q5_justification()

import altair as alt
import pandas as pd
import streamlit as st

def show_q5_view(path="../data/simpsons_episodes_cleaned.csv"):
    # Load and preprocess the data
    df = load_data(path)
    df = preprocess_data(df)

    # --- CONFIGURE CHART 1: PERCENTAGE ---
    
    scatter_pct = alt.Chart(df[df['number_of_viewers_percentage'] < 6]).mark_circle(opacity=0.4, size=40, color='#9edae5').encode(
        x=alt.X('number_of_episode_normalized:Q', title='Season Progression (Normalized 0 to 1)'),
        y=alt.Y('number_of_viewers_percentage:Q', title='Viewers as % of Season Total'),
        tooltip=['season', 'number_in_season', 'number_of_viewers_percentage', 'us_viewers_in_millions', 'number_of_episode_normalized']
    )

    trend_line_pct = alt.Chart(df).mark_line(color='#1f77b4', strokeWidth=4, point=True).encode(
        x=alt.X('mean(number_of_episode_normalized):Q'), 
        y=alt.Y('mean(number_of_viewers_percentage):Q', scale=alt.Scale(domain=(3, 6))),
        tooltip=[
            alt.Tooltip('number_of_episode_normalized_quantiles:O', title='Season Phase (Quantile)'),
            alt.Tooltip('mean(number_of_viewers_percentage):Q', title='Average percentage of viewers', format='.2f')
        ]
    )

    final_chart_percentage = (trend_line_pct + scatter_pct).properties(
        width=1100, 
        height=400,
        title="Intraseasonal Viewership Pattern (percentage of season total)"
    )

    # Render it in Streamlit
    st.altair_chart(final_chart_percentage, use_container_width=True)
