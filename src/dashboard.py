import streamlit as st

# 1. Import your section-rendering functions
from final_views.q1_ratings_evolution import render_q1_view, show_q1_view
from final_views.q2_viewers_evolution import show_q2_view
from final_views.q3_correlation import render_q3_view, show_q3_view
from final_views.q4_weekday_viewers import render_q4_view, show_q4_view
from final_views.q5_seasonal_pattern import render_q5_view, show_q5_view

# 2. Set the layout to wide
st.set_page_config(
    page_title="The Simpsons Analytics Dashboard",
    layout="wide" 
)

# --- THE MAGIC TRICK: INJECT CUSTOM CSS ---
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1600px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ------------------------------------------

st.title("The Simpsons Analytics Dashboard")
st.divider()

# 3. Dictionary holding the FUNCTION references
questions = {
    "Ratings over time": {
        "question": "How have the ratings evolved over time?",
        "render_func": show_q1_view
    },
    "Viewers by Weekday": {
        "question": "Are viewers related to the weekday aired?",
        "render_func": show_q4_view
    },
    "Ratings vs Viewers": {
        "question": "Is there a correlation between ratings and viewers?",
        "render_func": show_q3_view
    },
    "Seasonal Pattern": {
        "question": "Do the seasons’ viewers present a pattern?",
        "render_func": show_q5_view
    },    
    "Viewers over time": {
        "question": "How have the viewers evolved over time?",
        "render_func": show_q2_view
    }
}

# Convert dictionary items to a list so we can slice them easily
questions_list = list(questions.items())

# --- TOP SECTION: 2-COLUMN GRID FOR FIRST 4 QUESTIONS ---
# Added gap="large" for better spacing between the left and right charts
col1, col2 = st.columns(2, gap="large")

for i in range(4):
    key, data = questions_list[i]
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        # Call the function to draw the chart
        data["render_func"]()
        
        # Use a Streamlit divider as a clean visual separator
        st.divider()

# --- BOTTOM SECTION: FULL WIDTH FOR THE 5TH QUESTION ---
last_key, last_data = questions_list[4]

# Render the last chart across the entire width of the page
last_data["render_func"]()

st.divider()
st.caption("Dashboard created by Biel Manté and Adrià Espinoza")