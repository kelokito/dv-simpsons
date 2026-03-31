import streamlit as st

# 1. Import the section-rendering functions
from final_views.q1_ratings_evolution import show_q1_view
from final_views.q2_viewers_evolution import show_q2_view
from final_views.q3_correlation import show_q3_view
from final_views.q4_weekday_viewers import show_q4_view
from final_views.q5_seasonal_pattern import show_q5_view

# 2. Set the layout to wide to use the full 2560px screen
st.set_page_config(page_title="The Simpsons Analytics", layout="wide")

# 3. Inject Custom CSS to remove padding and maximize the width
st.markdown(
    """
    <style>
    .block-container {
        max-width: 2500px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📺 The Simpsons Analytics Dashboard")

# =====================================================================
# --- COMPREHENSIVE LAYOUT ---
# Left to right, top to bottom order: Q1, Q2, Q3, Q4, Q5
# Q1 has width=700, Q2 has width=1400. They fit perfectly side by side 
# on a 2560px screen in a ~1:2 ratio.
# =====================================================================

st.divider()

col1, col2 = st.columns([2, 2], gap="small")

with col1:
    show_q1_view()  # 1. Ratings Evolution
    
with col2:
    show_q2_view()  # 2. Viewers Evolution
    

col3, col4, col5 = st.columns([2,1,2], gap="small")

with col3:
    show_q3_view()  # 3. Correlation: Ratings vs. Viewers
    
with col4:
    show_q4_view()  # 4. Weekday Viewers
    
with col5:
    show_q5_view()  # 5. Seasonal Pattern

st.divider()
st.caption("Dashboard created by Biel Manté and Adrià Espinoza")