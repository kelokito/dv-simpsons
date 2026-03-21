import altair as alt
import pandas as pd
import streamlit as st
from scipy.stats import kendalltau


JUSTIFICATION_TEXT = """
"""



# 1. Cache the data loading separately so it's fast!
@st.cache_data
def load_data(path="../data/simpsons_episodes_cleaned.csv"):
    return pd.read_csv(path)

def render_q3_justification():
    st.divider()
    st.markdown("### Justification")
    st.write(JUSTIFICATION_TEXT)

# 2. This function builds the whole Q3 section
def render_q3_view():
    # Load the cached data
    df = load_data()

    st.markdown("### Ratings vs. Viewership Correlation")
    st.write("How do the ratings and viewership relate to each other? Let's look at their relationship.")

    # ---------------------------------------------------------
    # CHART 1: Scatter Plot with Trendline
    # ---------------------------------------------------------
    st.markdown("#### 1. Overall Correlation (Scatter Plot)")
    
    # Base scatter plot


    correlation_kendall, _ = kendalltau(df['us_viewers_in_millions'], df['imdb_rating'])
    correlation_kendall = correlation_kendall.round(2)

    correlation_pearson = df['us_viewers_in_millions'].corr(df['imdb_rating'])
    correlation_pearson = correlation_pearson.round(2)

    


    scatter = alt.Chart(df).mark_circle(size=60, opacity=0.5).encode(
        x=alt.X('imdb_rating:Q', title='IMDb Rating', scale=alt.Scale(zero=False)),
        y=alt.Y('us_viewers_in_millions:Q', title='US Viewers (Millions)'),
        tooltip=['title', 'season', 'imdb_rating', 'us_viewers_in_millions']
    )


    corr_labels = [
        f"Kendall Tau: {correlation_kendall}",
        f"Pearson: {correlation_pearson}",
    ]

    corr_legend_df = pd.DataFrame({
        'metric': corr_labels,
        'imdb_rating': [df['imdb_rating'].min(), df['imdb_rating'].min()],
        'us_viewers_in_millions': [df['us_viewers_in_millions'].max(), df['us_viewers_in_millions'].max()],
    })

    # Invisible marks used only to render an in-plot legend with correlation values.
    corr_legend = alt.Chart(corr_legend_df).mark_text().encode(
        x='imdb_rating:Q',
        y='us_viewers_in_millions:Q',
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
                symbolType='stroke',
                symbolStrokeColor='black',
                symbolStrokeWidth=2
         ),
        ),
    )




    
    # Add a regression line (trendline) to show the correlation path clearly
    trendline = scatter.transform_regression('imdb_rating', 'us_viewers_in_millions').mark_line(color='red', strokeWidth=3)
    
    chart1 = (scatter + trendline + corr_legend).properties(height=400)
    st.altair_chart(chart1, use_container_width=True)

    st.write("We can observe an overall postivie trend in the scatter plot, but is it alos noticeable that there is a lot of variability in the data, meaning that for a given ratiing, the number of viewers can vary widely. ")
    st.write("To quantify this relationship, we calculated 2 correlation coefficients shown in the plot. We calculated both Pearson's correlation, which measures linear correlation, and Kendall's Tau, which is a non-parametric " \
    "measure of rank correlation. This second measure can be usefull since we know from our EDA and visualizations that some of the assumptions of Pearson's correlation (like normality, linearity and constant variance) do not hold. Both show values that indicate a moderate positive correlation between ratings and viewership. This allows us to plot both variables in a double-axis chart, " \
    "not do demonstrate any correlation but to display the relatiionship between the variables in different seasons and see if this relationship holds across time.")

    



    # ---------------------------------------------------------
    # CHART 2: Dual-Axis Line Chart over Time
    # ---------------------------------------------------------
    st.markdown("#### 2. Trends Over Time (Dual-Axis Line Chart)")

    # For a clean line chart, it's usually best to aggregate by season first 
    # so it doesn't look like a chaotic scribble of 600+ episodes.
    season_df = df.groupby('season').agg({
        'us_viewers_in_millions': 'mean',
        'imdb_rating': 'mean'
    }).reset_index()

    # Base chart for the X-axis (Season)
    base = alt.Chart(season_df).encode(
        x=alt.X('season:O', title='Season', axis = alt.Axis(labelAngle=0))
    )

    # First line: Viewers (Blue)
    line_viewers = base.mark_line(color='#1f77b4', strokeWidth=3).encode(
        y=alt.Y('us_viewers_in_millions:Q', 
                title='Average Viewers (Millions)', 
                axis=alt.Axis(titleColor='#1f77b4'))
    )
    point_viewers = base.mark_point(size=80, filled=True, stroke='white', strokeWidth=1.5, color='#1f77b4').encode(
        y=alt.Y('us_viewers_in_millions:Q'),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('us_viewers_in_millions:Q', title='Avg Viewers (Millions)', format='.2f')
        ]
    )


    # Second line: Ratings (Orange)
    line_ratings = base.mark_line(color='#ff7f0e', strokeWidth=3).encode(
        y=alt.Y('imdb_rating:Q', 
                title='Average IMDb Rating', 
                axis=alt.Axis(titleColor='#ff7f0e'), 
                scale=alt.Scale(zero=False))
                
    )
    point_ratings = base.mark_point(size=80, filled=True, stroke='white', strokeWidth=1.5, color='#ff7f0e').encode(
        y=alt.Y('imdb_rating:Q',title =''),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('imdb_rating:Q', title='Avg IMDb Rating', format='.2f')
        ]
    )

    # Legend layer generated from the same season_df (no extra DataFrame needed).
    legend = alt.Chart(season_df).transform_fold(
        ['us_viewers_in_millions', 'imdb_rating'],
        as_=['metric', 'value']
    ).transform_calculate(
        series="datum.metric == 'us_viewers_in_millions' ? 'Average Viewers' : 'Average Ratings'"
    ).mark_point(size=1, opacity=0,filled =True ).encode(
        x=alt.X('season:O'),
        y=alt.Y('us_viewers_in_millions:Q',title=''),
        color=alt.Color(
            'series:N',
            title='',
            scale=alt.Scale(domain=['Average Viewers', 'Average Ratings'], range=['#1f77b4', '#ff7f0e']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        )
    )

    # Combine them and resolve the Y-axis so they stay independent
    viewers_layer = alt.layer(line_viewers, point_viewers,legend)
    ratings_layer = alt.layer(line_ratings, point_ratings)
    chart2 = alt.layer(viewers_layer, ratings_layer).resolve_scale(y='independent').properties(height=400)
    
    st.altair_chart(chart2, use_container_width=True)
    st.write("We can see that the linear elationship is specially strong for later seasons, where both ratings and viewership decline together approximately after season 15. From seasons 1-8 we see that the average ratings grow while the viewership declines, and in seasons 11-14 we see the opposite, with ratings declining while viewership grows. This is an interesting finding, as it shows that the correlation between ratings and viewership is not consistent across all seasons, and that there are periods where they even move in opposite directions. This could be due to a variety of factors, such as changes in the show's quality, shifts in audience preferences, or external events affecting viewership.")

    st.markdown("#### 3. Each espisode")
    st.write("not going to use, just testing, justifiquem que l'average es sufucient ja que ja tenim l'scatter + els coefs")

    # For a clean line chart, it's usually best to aggregate by season first 
    # so it doesn't look like a chaotic scribble of 600+ episodes.
    

    # Base chart for the X-axis (Season)
    base = alt.Chart(df).encode(
        x=alt.X('number_in_series:O', title='Season')
    )

    # First line: Viewers (Blue)
    line_viewers = base.mark_line(color='#1f77b4', strokeWidth=3).encode(
        y=alt.Y('us_viewers_in_millions:Q', 
                title='Viewers (Millions)', 
                axis=alt.Axis(titleColor='#1f77b4'))
    )
    point_viewers = base.mark_point(size=80, filled=True, stroke='white', strokeWidth=1.5, color='#1f77b4').encode(
        y=alt.Y('us_viewers_in_millions:Q'),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('us_viewers_in_millions:Q', title='Viewers (Millions)', format='.2f')
        ]
    )


    # Second line: Ratings (Orange)
    line_ratings = base.mark_line(color='#ff7f0e', strokeWidth=3).encode(
        y=alt.Y('imdb_rating:Q', 
                title='IMDb Rating', 
                axis=alt.Axis(titleColor='#ff7f0e'), 
                scale=alt.Scale(zero=False))
                
    )
    point_ratings = base.mark_point(size=80, filled=True, stroke='white', strokeWidth=1.5, color='#ff7f0e').encode(
        y=alt.Y('imdb_rating:Q',title =''),
        tooltip=[
            alt.Tooltip('season:O', title='Season'),
            alt.Tooltip('imdb_rating:Q', title='IMDb Rating', format='.2f')
        ]
    )

    # Legend layer generated from the same season_df (no extra DataFrame needed).
    legend = alt.Chart(df).transform_fold(
        ['us_viewers_in_millions', 'imdb_rating'],
        as_=['metric', 'value']
    ).transform_calculate(
        series="datum.metric == 'us_viewers_in_millions' ? 'Viewers' : 'Ratings'"
    ).mark_point(size=1, opacity=0,filled =True ).encode(
        x=alt.X('season:O'),
        y=alt.Y('us_viewers_in_millions:Q',title=''),
        color=alt.Color(
            'series:N',
            title='',
            scale=alt.Scale(domain=['Viewers', 'Ratings'], range=['#1f77b4', '#ff7f0e']),
            legend=alt.Legend(orient='top-right', strokeColor='black', fillColor='white', cornerRadius=5, padding=10)
        )
    )

    # Combine them and resolve the Y-axis so they stay independent
    viewers_layer = alt.layer(line_viewers, point_viewers,legend)
    ratings_layer = alt.layer(line_ratings, point_ratings)
    chart2 = alt.layer(viewers_layer, ratings_layer).resolve_scale(y='independent').properties(height=400)
    
    st.altair_chart(chart2, use_container_width=True)
    st.write("We can see that the linear elationship is specially strong for later seasons, where both ratings and viewership decline together approximately after season 15. From seasons 1-8 we see that the average ratings grow while the viewership declines, and in seasons 11-14 we see the opposite, with ratings declining while viewership grows. This is an interesting finding, as it shows that the correlation between ratings and viewership is not consistent across all seasons, and that there are periods where they even move in opposite directions. This could be due to a variety of factors, such as changes in the show's quality, shifts in audience preferences, or external events affecting viewership.")


    

    # ---------------------------------------------------------
    # JUSTIFICATION
    # ---------------------------------------------------------
