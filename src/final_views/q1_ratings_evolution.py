import altair as alt
import pandas as pd
import streamlit as st


### MODIFY THIS TEXT TO EXPLAIN IN OUR OWN WORDS WHY WE CHOSE A HEATMAP FOR THIS QUESTION
JUSTIFICATION_TEXT = """"A heatmap is ideal for this question because it allows us to visualize the ratings of all episodes across seasons in a compact and intuitive way. " \
    "The color gradient quickly highlights patterns, such as which seasons had higher or lower ratings,"
    " and the text overlay provides precise values without needing to hover over points, making it easy to spot trends at a glance."""


# 1. Cache the data loading separately so it's fast!
@st.cache_data
def load_data(path="../data/simpsons_episodes_cleaned.csv"):
    print("Loading data from disk...")  # This will only print once, thanks to caching!
    print(f"Data loaded from: {path}")
    return pd.read_csv(path)


def render_q1_justification():
    # Initialize the section with a divider and a header, then add the justification text
    st.divider()
    
    st.markdown("### Justification")

    st.write(JUSTIFICATION_TEXT)


def show_q1_view(path="../data/simpsons_episodes_cleaned.csv"):

    # Load the cached data
    df = load_data(path)

    # --- CONFIGURE CHART 1 ---
    heatmap = alt.Chart(df).mark_rect(tooltip = False).encode(
        x = alt.X('season:N', axis=alt.Axis(orient='top', labelAngle=0),title = 'Season'),
        y = alt.Y('number_in_season:N', title = 'Episode Number'),
        color = alt.Color('imdb_rating:Q',
            scale = alt.Scale(range=['red', 'yellow', 'green']),title = 'IMDb Rating'),
        
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
    st.altair_chart(chart1)



# 2. This function now builds the whole section
def render_q1_view(path="../data/simpsons_episodes_cleaned.csv"):
    

    # --- ADD YOUR TEXT HERE ---

    st.write("This heatmap shows the IMDB ratings for each episode across all seasons. We can observe how the 'Golden Era' stands out in the early seasons...")

    show_q1_view(path)

    render_q1_justification()
