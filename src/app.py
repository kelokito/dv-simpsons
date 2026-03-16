import streamlit as st
import streamlit.components.v1 as components # <-- 1. Import Streamlit components!
import os

# 1. Set up the page configuration
st.set_page_config(
    page_title="The Simpsons Analytics Dashboard",
    page_icon="📺",
    layout="centered" 
)

st.title("The Simpsons Analytics Dashboard")
st.markdown("Explore the data behind the show's viewership and ratings by clicking through the questions below.")

# 2. Define your questions and their corresponding HTML files
questions = {
    "Ratings over time": {
        "question": "How have the ratings evolved over time?",
        "file": "q1_ratings_evolution.html"
    },
    "Viewers over time": {
        "question": "How have the viewers evolved over time?",
        "file": "q2_viewers_evolution.html"
    },
    "Ratings vs Viewers": {
        "question": "Is there a correlation between the ratings and the viewers?",
        "file": "q3_correlation.html"
    },
    "Viewers by Weekday": {
        "question": "Are the number of viewers for the episodes related to the weekday they were aired?",
        "file": "q4_weekday_viewers.html"
    },
    "Seasonal Pattern": {
        "question": "Do the seasons’ number of viewers present any relevant pattern?",
        "file": "q5_seasonal_pattern.html"
    }
}

# 3. Create tabs for each question
tab_titles = list(questions.keys())
tabs = st.tabs(tab_titles)

# 4. Loop through the tabs to populate them
for i, (tab_key, data) in enumerate(questions.items()):
    with tabs[i]:
        st.subheader(data["question"])
        
        file_path = os.path.join("..", "data", "figures", data["file"])
        
        # Check if the file actually exists to prevent ugly errors on the dashboard
        if os.path.exists(file_path):
            
            # Creates 3 columns: 5% empty space, 90% for the chart, 5% empty space
            left_spacer, center_col, right_spacer = st.columns([0.5, 9, 0.5]) 
            
            with center_col:
                # Read the HTML file and render it!
                with open(file_path, "r", encoding="utf-8") as f:
                    html_data = f.read()
                
                # FIX: Added height=600 here so the chart doesn't get cut off!
                components.html(html_data, height=600, scrolling=False)
                
        else:
            st.error(f"⚠️ Could not find the chart file: `{file_path}`. Please make sure your notebook saved it correctly.")

st.divider()
st.caption("Dashboard created by Biel Manté and Adrià Espinoza")