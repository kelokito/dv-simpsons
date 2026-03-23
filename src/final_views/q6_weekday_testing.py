import altair as alt
import pandas as pd
import streamlit as st
import numpy as np


JUSTIFICATION_TEXT = """
Testing weekdays

"""
# 1. Cache the data loading separately so it's fast!
@st.cache_data
def load_data(path="../data/simpsons_episodes_cleaned.csv"):
    return pd.read_csv(path)

def render_q6_justification():
    # Initialize the section with a divider and a header, then add the justification text
    st.divider()
    st.markdown("### Justification")
    st.markdown(JUSTIFICATION_TEXT)

# 2. Preprocess the data to create the normalized and quantile columns

def render_q6_view(path="../data/simpsons_episodes_cleaned.csv"):
    # Load and preprocess the data
    df = load_data(path)
    df = df[df['day_aired'].isin(['Sunday','Thursday'])]


    histogram = alt.Chart(df).mark_bar(opacity=0.7).encode(
        x=alt.X(
            'us_viewers_in_millions',
            title='Number of Viewers',
            bin=alt.Bin(maxbins=60),
            axis=alt.Axis(format=',.0f')
        ),
        y =alt.Y('count()', title='Number of Episodes'),
        tooltip=['day_aired', 'count()'],
        color=alt.Color('day_aired:N', 
                        scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#1f77b4', '#ff7f0e']),
                    legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10))
    )

    density = alt.Chart(df).transform_density(
        'us_viewers_in_millions',
        as_=['us_viewers_in_millions', 'density'],
        counts=True,
        groupby=['day_aired'],
        #bandwidth=1
    ).mark_line(size=2).encode(
        x=alt.X('us_viewers_in_millions', title='Number of Viewers', axis=alt.Axis(format=',.0f')),
        y=alt.Y('density:Q', title=''),
        color=alt.Color(
            'day_aired:N',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#1f77b4', '#ff7f0e']),
            legend=None
        ),
        tooltip=['day_aired:N', 'us_viewers_in_millions:Q', 'density:Q']
    )

    area = alt.Chart(df).transform_density(
        'us_viewers_in_millions',
        as_=['us_viewers_in_millions', 'density'],
        groupby=['day_aired']
    ).mark_area(opacity=0.7).encode(
        x=alt.X('us_viewers_in_millions:Q', title='Number of Viewers', axis=alt.Axis(format=',.0f')),
        y=alt.Y('density:Q', title='Estimated Episode Count'),
        color=alt.Color(
            'day_aired:N',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#1f77b4', '#ff7f0e'])
        )
    )

    chart = (histogram + density).properties(
        width=700, 
        height=400,
        title='Distribution of Viewers by Weekday'
    ).resolve_scale(
        y = 'shared'
    )

    st.altair_chart(chart, width='stretch')
    st.altair_chart(histogram, width='stretch')
    st.altair_chart(area, width='stretch')

    st.write("Less thursday espisodes but with more viewers. Let's look at the dates these were aired.")

    df = load_data(path)
    df['original_air_date'] = pd.to_datetime(df['original_air_date'])
    df = df.sort_values('original_air_date').copy()

    base_line = alt.Chart(df[df['day_aired'].isin(['Sunday', 'Thursday'])]).mark_line(color='black').encode(
        x=alt.X('original_air_date:T', title='Original Air Date'),
        y=alt.Y('us_viewers_in_millions:Q', title='US Viewers (Millions)')
    )

    highlighted_points = alt.Chart(df[df['day_aired'].isin(['Sunday', 'Thursday'])]).mark_point(size=42, filled=True).encode(
        x=alt.X('original_air_date:T', title='Original Air Date'),
        y=alt.Y('us_viewers_in_millions:Q', title='US Viewers (Millions)'),
        color=alt.Color(
            'day_aired:N',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#1f77b4', '#ff7f0e']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        ),
        tooltip=['original_air_date:T', 'number_in_season:Q', 'us_viewers_in_millions:Q', 'day_group:N', 'season:N']
    )

    line_chart = (base_line + highlighted_points).properties(
        title='US Viewers Over Time'
    )

    season_finals = df[df['is_last_episode'] == 1].copy()
    limit_bounds = alt.Chart(season_finals).mark_rule(color='black', strokeDash=[4, 4], opacity=0.6).encode(
        x=alt.X('original_air_date:T'),
        tooltip=[alt.Tooltip('season:N', title='Season')]
    )

    season_ranges = (
        df.groupby('season', as_index=False)
        .agg(
            start_date=('original_air_date', 'min'),
            end_date=('original_air_date', 'max')
        )
    )
    season_ranges['end_date'] = pd.to_datetime(season_ranges['end_date'])
    season_ranges['start_date'] = pd.to_datetime(season_ranges['start_date'])
    season_ranges['mid_date'] = season_ranges['start_date'] + (season_ranges['end_date'] - season_ranges['start_date']) / 3
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

    chart = line_chart + limit_bounds + season_labels
    chart.properties(width=1500,height=400)
    st.altair_chart(chart, width='stretch')

    st.write("The espisodes aired on thursday where aired in some fo the early seasons, where the show was more popular. This could indicate that the day of the week is not the main factor driving viewership, but rather the season and overall popularity of the show at that time." \
    "We will eliminate the tendency of the show viewerhsip and analyze the distribution again with the bias of the seasons removed.")

    df['differentiation'] = df.groupby('season')['us_viewers_in_millions'].transform(lambda x: x - x.mean())


    area = alt.Chart(df).transform_density(
        'differentiation',
        as_=['differentiation', 'density'],
        groupby=['day_aired']
    ).mark_area(opacity=0.7).encode(
        x=alt.X('differentiation:Q', title='Number of Viewers minus Season average)', axis=alt.Axis(format=',.0f')),
        y=alt.Y('density:Q', title='Density'),
        color=alt.Color(
            'day_aired:N',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#1f77b4', '#ff7f0e'])
        )
    )

    st.altair_chart(area, width='stretch')

    df['differentiation2'] = df.groupby('season')['us_viewers_in_millions'].transform(lambda x: (x - x.mean()) / x.std())

    area = alt.Chart(df).transform_density(
        'differentiation2',
        as_=['differentiation2', 'density'],
        groupby=['day_aired']
    ).mark_area(opacity=0.7).encode(
        x=alt.X('differentiation2:Q', title='Number of Viewers minus Season average and std)', axis=alt.Axis(format=',.0f')),
        y=alt.Y('density:Q', title='Density'),
        color=alt.Color(
            'day_aired:N',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#1f77b4', '#ff7f0e'])
        )
    )

    st.altair_chart(area, width='stretch')

    # do the transfromattion yi = yi - yi-1

    df['differentiation3'] = df['us_viewers_in_millions'].transform(lambda x: x.diff())

    area = alt.Chart(df).transform_density(
        'differentiation3',
        as_=['differentiation3', 'density'],
        groupby=['day_aired']
    ).mark_area(opacity=0.7).encode(
        x=alt.X('differentiation3:Q', title='Number of Viewers yi - yi-1', axis=alt.Axis(format=',.0f'),scale =alt.Scale(domain=(-10, 10))),
        y=alt.Y('density:Q', title='Density',scale =alt.Scale(domain=(0, 0.5))),
        color=alt.Color(
            'day_aired:N',
            title='Day Aired',
            scale=alt.Scale(domain=['Sunday', 'Thursday'], range=['#1f77b4', '#ff7f0e']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        )
    ).properties(
        title='Density of Viewership Changes (yi - yi-1) by Weekday',
        width=200,
        height=400
    )

    st.altair_chart(area,width=600)



    

    # Render the text block below the chart
    render_q6_justification()