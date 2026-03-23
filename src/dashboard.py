import streamlit as st

# 1. Import your section-rendering functions
from final_views.q1_ratings_evolution import show_q1_view
from final_views.q2_viewers_evolution import show_q2_view
from final_views.q3_correlation import show_q3_view
from final_views.q4_weekday_viewers import show_q4_view
from final_views.q5_seasonal_pattern import show_q5_view

# 2. Set the layout to wide (THIS MUST BE THE ONLY ONE IN YOUR ENTIRE PROJECT)
st.set_page_config(page_title="The Simpsons Analytics Dashboard", layout="wide")

# 3. Inject Custom CSS
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1600px;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📺 The Simpsons Analytics Dashboard")
st.divider()

# =====================================================================
# --- CURRENT LAYOUT: Bottom Heavy ---
# =====================================================================
col1, col2 = st.columns(2, gap="large")

with col1:
    show_q1_view()  # Top Left: Ratings Evolution
    st.divider()
    show_q3_view()  # Bottom Left: Ratings vs. Viewers
    
with col2:
    show_q4_view()  # Top Right: Weekday Viewers
    st.divider()
    show_q5_view()  # Bottom Right: Seasonal Pattern

st.divider()
show_q2_view()      # Full Width at the bottom: Viewers Over Time


# =====================================================================
# --- ALTERNATIVE A: "The Hero" (Top Heavy) ---
# Great for storytelling: Hook them with the big timeline first, 
# then break down the details in the grid below.
# =====================================================================
_ = """
show_q2_view()      # Full Width at the top: Viewers Over Time
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    show_q1_view()  # Left: Ratings Heatmap
    st.divider()
    show_q3_view()  # Left: Ratings vs Viewers Scatter
    
with col2:
    show_q4_view()  # Right: Weekday Distribution
    st.divider()
    show_q5_view()  # Right: Seasonal Pattern
"""


# =====================================================================
# --- ALTERNATIVE B: "The Analyst" (Wide & Narrow Split) ---
# Groups the two wide, data-heavy charts on the left (66% of the screen)
# and stacks the three smaller analytical/pattern charts on the right (33%).
# =====================================================================
_ = """
col_wide, col_narrow = st.columns([2, 1], gap="large")

with col_wide:
    show_q2_view()  # Wide: Timeline
    st.divider()
    show_q1_view()  # Wide: Heatmap
    
with col_narrow:
    show_q3_view()  # Narrow: Correlation
    st.divider()
    show_q4_view()  # Narrow: Weekday
    st.divider()
    show_q5_view()  # Narrow: Season Pattern
"""


# =====================================================================
# --- ALTERNATIVE C: "The Three-Row Story" ---
# Gives maximum breathing room. Puts the heatmap up top, 
# splits the timeline and correlation in the middle, 
# and puts the deep-dive patterns at the bottom.
# =====================================================================
_ = """
show_q1_view()      # Row 1 Full Width: Heatmap
st.divider()

row2_col1, row2_col2 = st.columns(2, gap="large")
with row2_col1:
    show_q2_view()  # Row 2 Left: Viewers Timeline
with row2_col2:
    show_q3_view()  # Row 2 Right: Ratings vs Viewers Correlation
    
st.divider()

row3_col1, row3_col2 = st.columns(2, gap="large")
with row3_col1:
    show_q4_view()  # Row 3 Left: Weekdays
with row3_col2:
    show_q5_view()  # Row 3 Right: Seasonal Pattern
"""

st.divider()
st.caption("Dashboard created by Biel Manté and Adrià Espinoza")