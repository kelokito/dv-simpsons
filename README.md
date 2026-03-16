
# 📺 dv-simpsons: The Simpsons Analytics Dashboard

Welcome to the **dv-simpsons** project! This repository contains a data visualization dashboard built with Python, Altair, and Streamlit to explore viewership and rating trends for *The Simpsons*.

Created by Biel Manté and Adrià Espinoza.

---

## 🚀 How to Run the Project

To get the dashboard up and running, please follow these steps in order.

### Step 1: Generate the Visualizations
Before launching the dashboard, you need to generate the charts. 
1. Open and execute the Jupyter Notebook `plots.ipynb`.
2. Running this notebook will process the data and generate several interactive visualizations as `.html` files.

### Step 2: Save the HTML Files
The Streamlit app expects to find these HTML files in a specific folder. Save or move the generated `.html` files directly into the `data/figures/` directory. 

Make sure they are named correctly to match the views in the app:
* `q1_ratings_evolution.html`
* `q2_viewers_evolution.html`
* `q3_correlation.html`
* `q4_weekday_viewers.html`
* `q5_seasonal_pattern.html`

Your folder structure should look something like this:
```text
dv-simpsons/
│
├── data/
│   └── figures/
│       ├── q1_ratings_evolution.html
│       └── ... (other HTML files)
│
├── src/
│   └── app.py
│
└── plots.ipynb

```

### Step 3: Launch the Streamlit App

Once your figures are saved in the correct directory, you can start the dashboard.

1. Open your terminal or command prompt.
2. Navigate to the `src` directory:
```bash
cd src

```


3. Run the Streamlit application:
```bash
streamlit run app.py

```


4. A browser window will automatically open with the dashboard interface, allowing you to explore the data!

