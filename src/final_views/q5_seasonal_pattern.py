import altair as alt
import pandas as pd
import streamlit as st
import sys
sys.path.append('../')
from preprocessing import load_data




def preprocess_data(df):
    df['number_of_episode_normalized'] = (100*df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')).round(2)
    df['number_of_episode_normalized_quantiles'] = pd.qcut(df['number_of_episode_normalized'], q=10, labels=False).round(2)
    df['number_of_viewers_percentage'] = df.groupby('season')['us_viewers_in_millions'].transform(lambda x: x / x.sum() * 100).round(2)
    return df



def make_plot_q5(path="../data/simpsons_episodes_cleaned.csv"):
    df = load_data(path)
    df = preprocess_data(df)
    
    scatter_pct = alt.Chart(df[df['number_of_viewers_percentage'] < 6]).mark_circle(opacity=0.4, size=40, color='#9edae5').encode(
        x=alt.X(
            'number_of_episode_normalized:Q',
            title='Season Progression - Episode Number / Episodes in Season',
            axis=alt.Axis(labelExpr="datum.value + '%'"),
        ),
        y=alt.Y(
            'number_of_viewers_percentage:Q',
            title='Viewers % - Episode Viewers / Season Total Viewers',
            axis=alt.Axis(labelExpr="datum.value + '%'"),
        ),
        tooltip=['season', 'number_in_season', 'number_of_viewers_percentage', 'us_viewers_in_millions', 'number_of_episode_normalized']
    )

    trend_line_pct = alt.Chart(df).mark_line(color='#1f77b4', strokeWidth=4, point=True).encode(
        x=alt.X('mean(number_of_episode_normalized):Q', axis=alt.Axis(labelExpr="datum.value + '%'")), 
        y=alt.Y(
            'mean(number_of_viewers_percentage):Q',
            scale=alt.Scale(domain=(2, 6.5)),
            axis=alt.Axis(labelExpr="datum.value + '%'"),
        ),
        tooltip=[
            alt.Tooltip('number_of_episode_normalized_quantiles:O', title='Season Phase (Quantile)'),
            alt.Tooltip('mean(number_of_viewers_percentage):Q', title='Average percentage of viewers', format='.2f')
        ]
    )

    chart = (trend_line_pct + scatter_pct).properties(
        width=1100, 
        height=465,
        title="Viewership Pattern within Seasons"
    )
    return chart

def show_q5_view():
    chart = make_plot_q5()
    st.altair_chart(chart)