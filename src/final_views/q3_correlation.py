import altair as alt
import pandas as pd
import streamlit as st
from scipy.stats import kendalltau
import sys
sys.path.append('../')
from preprocessing import load_data


def make_plot_q3(path="../data/simpsons_episodes_cleaned.csv"):
    df = load_data(path)

    correlation_kendall, _ = kendalltau(df['us_viewers_in_millions'], df['imdb_rating'])
    correlation_kendall = correlation_kendall.round(2)

    correlation_pearson = df['us_viewers_in_millions'].corr(df['imdb_rating'])
    correlation_pearson = correlation_pearson.round(2)

    scatter = alt.Chart(df).mark_circle(size=60, opacity=0.5,color='teal').encode(
        y=alt.Y('imdb_rating:Q', title='IMDb Rating', scale=alt.Scale(domain=[3, df['imdb_rating'].max() + 1])),
        x=alt.X('us_viewers_in_millions:Q', title='US Viewers (Millions)', scale=alt.Scale(zero=False,domain=[0, df['us_viewers_in_millions'].max() + 1])),
        tooltip=['title', 'season', 'imdb_rating', 'us_viewers_in_millions'],
    )


    corr_labels = [
        f"Kendall Tau: {correlation_kendall}",
        f"Pearson: {correlation_pearson}",
    ]

    corr_legend_df = pd.DataFrame({
        'metric': corr_labels,
        'imdb_rating': [df['imdb_rating'].max(), df['imdb_rating'].max()],
        'us_viewers_in_millions': [df['us_viewers_in_millions'].max(), df['us_viewers_in_millions'].max()],
    })


    corr_legend = alt.Chart(corr_legend_df).mark_text().encode(
        y='imdb_rating:Q',
        x='us_viewers_in_millions:Q',
        color=alt.Color(
            'metric:N',
            scale=alt.Scale(domain=corr_labels, range=['black', 'black']),
            legend=alt.Legend(
                title='',
                orient='top-left',
                fillColor='white',
                strokeColor='black',
                cornerRadius=4,
                padding=6,
                symbolSize=0,
                symbolType='stroke',
                symbolStrokeColor='black',
                symbolStrokeWidth=2
         ),
        ),
    )
    
    trendline = alt.Chart(df).transform_regression(
        'us_viewers_in_millions',
        'imdb_rating',
        method='poly',
        order=2,
    ).mark_line(color='#FF8749', strokeWidth=3,tooltip=False).encode(
        x='us_viewers_in_millions:Q',
        y='imdb_rating:Q',
    )
    
    chart1 = (scatter + trendline + corr_legend).properties(height=450, title='US Viewers and IMDb Ratings Correlation')
    return chart1


def show_q3_view(path="../data/simpsons_episodes_cleaned.csv"):
    
    plot = make_plot_q3(path)
    st.altair_chart(plot, width='stretch')

    