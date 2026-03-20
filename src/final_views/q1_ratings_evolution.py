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


# 2. This function now builds the whole section
def render_q1_view(path="../data/simpsons_episodes_cleaned.csv"):
    # Load the cached data
    df = load_data(path)

    # --- ADD YOUR TEXT HERE ---

    st.write("This heatmap shows the IMDB ratings for each episode across all seasons. We can observe how the 'Golden Era' stands out in the early seasons...")

    # --- CONFIGURE CHART 1 ---
    heatmap = alt.Chart(df).mark_rect().encode(
        x = alt.X('season:N', axis=alt.Axis(orient='top', labelAngle=0)),
        y = alt.Y('number_in_season:N'),
        color = alt.Color('imdb_rating:Q',
            scale = alt.Scale(range=['red', 'yellow', 'green'])))

    text = alt.Chart(df).mark_text(baseline='middle').encode(
        x = alt.X('season:N'),
        y = alt.Y('number_in_season:N'),
        text = alt.Text('imdb_rating:Q', format=".1f")
    )

    chart1 = (heatmap + text).properties(width=600, height=400)
    
    # Render the first chart natively inside this function!
    st.altair_chart(chart1, use_container_width=True)

    render_q1_justification()