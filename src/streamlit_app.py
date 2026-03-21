import streamlit as st

# 1. Import your section-rendering functions
from final_views.q1_ratings_evolution import render_q1_view
from final_views.q2_viewers_evolution import render_q2_view
from final_views.q3_correlation import render_q3_view
from final_views.q4_weekday_viewers import render_q4_view
from final_views.q5_seasonal_pattern import render_q5_view

# 2. Set the layout to wide
st.set_page_config(
    page_title="The Simpsons Analytics Dashboard",
    layout="wide" 
)

# --- THE MAGIC TRICK: INJECT CUSTOM CSS ---
# This sets the maximum width of the app to 1100 pixels and centers it.
# You can change '1100px' to whatever size feels best for your charts!
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ------------------------------------------

st.title("The Simpsons Analytics Dashboard")
st.markdown("Explore the data behind the show's viewership and ratings by clicking through the questions below.")

# 3. Update the dictionary to hold the FUNCTION references
questions = {
    "Ratings over time": {
        "question": "How have the ratings evolved over time?",
        "render_func": render_q1_view
    },
    "Viewers over time": {
        "question": "How have the viewers evolved over time?",
        "render_func": render_q2_view
    },
    "Ratings vs Viewers": {
        "question": "Is there a correlation between the ratings and the viewers?",
        "render_func": render_q3_view
    },
    "Viewers by Weekday": {
        "question": "Are the number of viewers for the episodes related to the weekday they were aired?",
        "render_func": render_q4_view
    },
    "Seasonal Pattern": {
        "question": "Do the seasons’ number of viewers present any relevant pattern?",
        "render_func": render_q5_view
    }
}

# 4. Create tabs for each question
tab_titles = list(questions.keys())
tabs = st.tabs(tab_titles)

# 5. Loop through the tabs to populate them
for i, (tab_key, data) in enumerate(questions.items()):
    with tabs[i]:
        st.subheader(data["question"])
        
        # NOTE: Because we set a max-width with CSS, you don't really need the 
        # spacer columns anymore! I removed them so the code is cleaner, 
        # but the charts won't stretch to the edge of your screen.
        data["render_func"]() 

st.divider()
st.caption("Dashboard created by Biel Manté and Adrià Espinoza")