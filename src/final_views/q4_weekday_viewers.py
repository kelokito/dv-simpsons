import altair as alt
import pandas as pd
import streamlit as st
import sys
sys.path.append('../')
from preprocessing import load_data


def preprocess_data(df):
    df['original_air_date'] = pd.to_datetime(df['original_air_date'])
    df = df[df['day_aired'].isin(['Sunday', 'Thursday'])]
    df['season_dec'] = df['season'] + -0.5 + (df['number_in_season'] / df.groupby('season')['number_in_season'].transform('max')) 
    df = df.sort_values('original_air_date')
    df['viewers_diff'] = df['us_viewers_in_millions'].diff()

    return df

def make_plot_q4(path="../data/simpsons_episodes_cleaned.csv"):
    df = load_data(path)
    df = preprocess_data(df)

    base = alt.Chart(df[abs(df['viewers_diff']) < 10]).transform_density(
        'viewers_diff',
        as_=['viewers_diff', 'density'],
        groupby=['day_aired']
    )    

    area = base.mark_area(opacity=0.4,tooltip=False).encode(
        x=alt.X('viewers_diff:Q', 
                title='Number of Viewers Change (yi - yi-1)', 
                axis=alt.Axis(format=',.0f'), 
                scale=alt.Scale(domain=(-10, 10))),
        y=alt.Y('density:Q', 
                stack=None,
            axis=None,
            scale=alt.Scale(domain=(0, 0.3))),
        color=alt.Color(
            'day_aired:N',
            title='Day Aired',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#800080', '#FF0080']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        )
    )

    line = base.mark_line(tooltip=False, stroke='black', strokeWidth=1.5).encode(
        x=alt.X('viewers_diff:Q', scale=alt.Scale(domain=(-10, 10))),
        y=alt.Y('density:Q', axis=None, scale=alt.Scale(domain=(0, 0.3))),
        detail='day_aired:N'   #
    )

    chart = (area + line).properties(
        title='Distribution of Detrended Weekday Viewership',
        height=450
    ) 

    return chart


def show_q4_view():
    chart = make_plot_q4()
    st.altair_chart(chart)