import streamlit as st

# 1. Import your section-rendering functions
from final_views.q1_ratings_evolution import render_q1_view, show_q1_view
from final_views.q2_viewers_evolution import render_q2_view, show_q2_view
from final_views.q3_correlation import render_q3_view, show_q3_view
from final_views.q4_weekday_viewers import render_q4_view
from final_views.q5_seasonal_pattern import render_q5_view
from final_views.q6_weekday_testing import render_q6_view

# 2. Set the layout to wide
st.set_page_config(
    page_title="The Simpsons Analytics Dashboard",
    layout="wide" 
)

# --- THE MAGIC TRICK: INJECT CUSTOM CSS ---
# I increased the max-width to 1400px here so the 2-column 
# grid doesn't squeeze your charts too much!
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
#st.markdown("Explore the data behind the show's viewership and ratings at a glance.")
st.divider()

# 3. Dictionary holding the FUNCTION references
questions = {
    "Ratings over time": {
        "question": "How have the ratings evolved over time?",
        "render_func": show_q1_view
    },
    "Viewers over time": {
        "question": "How have the viewers evolved over time?",
        "render_func": show_q2_view
    },
    "Viewers by Weekday": {
        "question": "Are viewers related to the weekday aired?",
        "render_func": render_q4_view
    },
    "Ratings vs Viewers": {
        "question": "Is there a correlation between ratings and viewers?",
        "render_func": show_q3_view
    },
    
    "Seasonal Pattern": {
        "question": "Do the seasons’ viewers present a pattern?",
        "render_func": render_q5_view
    },
     "Weekday Testing": {
        "question": "Weekday Testing", # Update this string if needed!
        "render_func": render_q6_view
    }
}

# 4. Create a 2-column grid layout
col1, col2 = st.columns(2)

# 5. Loop through the questions and place them in the columns
for i, (key, data) in enumerate(questions.items()):
    
    # Even index (0, 2, 4) goes to col1. Odd index (1, 3, 5) goes to col2.
    target_col = col1 if i % 2 == 0 else col2
    
    with target_col:
        #st.subheader(data["question"])
        
        # Call the function to draw the chart!
        data["render_func"]()
        
        # Add a little breathing room beneath each graphic
        st.write("<br><br>", unsafe_allow_html=True) 

st.divider()
st.caption("Dashboard created by Biel Manté and Adrià Espinoza")