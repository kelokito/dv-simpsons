import altair as alt
import pandas as pd
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import sys
sys.path.append('../')
from preprocessing import load_data

    
def preprocess_data():
    df = load_data(path="../data/simpsons_episodes_cleaned.csv")
    df['season_05'] = df['season'] + 0.5
    df['season_dec'] = df['season'] + (df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')) 
    return df
    


def make_plot_q2():

    df = preprocess_data()

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
            alt.Tooltip('mean_viewers:Q', title='Average US Viewers (Millions)', format='.2f')
        ]
    )

    point = alt.Chart(df).transform_calculate(
        series="'Individual episode'"
    ).mark_circle(size=50, opacity=0.75).encode(
        x=alt.X('season_dec:Q', title='Season', scale=alt.Scale(domain=[1, 28])),
        y=alt.Y('us_viewers_in_millions:Q'),
        color=alt.Color(
            'series:N',
            title='',
            scale=alt.Scale(domain=['Individual episode', 'Season average'], range=['#9edae5', '#1f77b4']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        ),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('number_in_season:O', title='Episode Number'),
             alt.Tooltip('title:N', title='Episode Title'),
            alt.Tooltip('us_viewers_in_millions:Q', title='US Viewers (Millions)', format='.2f')
        ]
    )
    
    chart = (line + point + avg_point).properties(width=1400, height=500,title='Evolution of US Viewership Over Seasons')
    return chart

def show_q2_view():
    chart = make_plot_q2()
    st.altair_chart(chart)

