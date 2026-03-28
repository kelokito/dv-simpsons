import altair as alt
import pandas as pd
import streamlit as st
import sys
sys.path.append('../')
from preprocessing import load_data


def make_plot_q1(path="../data/simpsons_episodes_cleaned.csv"):

    df = load_data(path)
    heatmap = alt.Chart(df).mark_rect(tooltip=False, stroke='white', strokeWidth=1).encode(
        x = alt.X('season:N', axis=alt.Axis(orient='top', labelAngle=0),title = 'Season'),
        y = alt.Y('number_in_season:N', title = 'Episode Number'),
        color = alt.Color('imdb_rating:Q',
            scale = alt.Scale(scheme='redyellowgreen'),title = 'IMDb Rating',
            legend=None)
    )
            
    text = alt.Chart(df).mark_text(baseline='middle', size=12).encode(
        x = alt.X('season:N', title='Season'),
        y = alt.Y('number_in_season:N', title='Episode Number'),
        text = alt.Text('imdb_rating:Q', format=".1f"),
        tooltip = [
            alt.Tooltip('title:N', title='Episode Title'),
            alt.Tooltip('season:N', title='Season'),
            alt.Tooltip('number_in_season:N', title='Episode Number'),
            alt.Tooltip('imdb_rating:Q', title='IMDb Rating', format='.1f')
        ]
    )

    chart1 = (heatmap + text).properties(width=700, height=450,title='IMDb Ratings by Season and Episode')
    return chart1


def show_q1_view():
    chart = make_plot_q1()
    st.altair_chart(chart)




def show_q1_view_notebook(path="../data/simpsons_episodes_cleaned.csv"):

    # Load the cached data
    df = load_data(path)

    # --- CONFIGURE CHART 1 ---
    heatmap = alt.Chart(df).mark_rect(tooltip=False, stroke='white', strokeWidth=1).encode(
        x = alt.X('season:N', axis=alt.Axis(orient='top', labelAngle=0),title = 'Season'),
        y = alt.Y('number_in_season:N', title = 'Episode Number'),
        color = alt.Color('imdb_rating:Q',
            scale = alt.Scale(scheme='redyellowgreen'),title = 'IMDb Rating',
            legend=None)
        
    )
            

    text = alt.Chart(df).mark_text(baseline='middle', size=12).encode(
        x = alt.X('season:N', title='Season'),
        y = alt.Y('number_in_season:N', title='Episode Number'),
        text = alt.Text('imdb_rating:Q', format=".1f"),
        tooltip = [
            alt.Tooltip('title:N', title='Episode Title'),
            alt.Tooltip('season:N', title='Season'),
            alt.Tooltip('number_in_season:N', title='Episode Number'),
            alt.Tooltip('imdb_rating:Q', title='IMDb Rating', format='.1f')
        ]
        
    )

    chart1 = (heatmap + text).properties(width=700, height=450,title='IMDb Ratings by Season and Episode')
    
    # Render the first chart natively inside this function!
    return chart1   





# 2. This function now builds the whole section
def render_q1_view(path="../data/simpsons_episodes_cleaned.csv"):
    

    # --- ADD YOUR TEXT HERE ---

    st.write("This heatmap shows the IMDB ratings for each episode across all seasons. We can observe how the 'Golden Era' stands out in the early seasons...")

    show_q1_view(path)

    render_q1_justification()
