import altair as alt
import pandas as pd
import streamlit as st
import sys
sys.path.append('../')
from preprocessing import load_data




def preprocess_data(df):
    df['number_of_episode_normalized'] = df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')
    df['number_of_episode_normalized_quantiles'] = pd.qcut(df['number_of_episode_normalized'], q=10, labels=False)
    df['number_of_viewers_percentage'] = df.groupby('season')['us_viewers_in_millions'].transform(lambda x: x / x.sum() * 100)
    return df



def make_plot_q5(path="../data/simpsons_episodes_cleaned.csv"):
    df = load_data(path)
    df = preprocess_data(df)
    
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

    chart = (trend_line_pct + scatter_pct).properties(
        width=1100, 
        height=465,
        title="Seasonal Viewership Pattern"
    )
    return chart

def show_q5_view():
    chart = make_plot_q5()
    st.altair_chart(chart)