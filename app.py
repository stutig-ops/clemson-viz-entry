import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Algorithm Suitability Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HEADER & ABSTRACT ---
st.title("🧩 Beyond Accuracy: Algorithm Suitability in Construction")
st.markdown("""
**Abstract:** This visualization challenges the "accuracy is everything" mindset. By analyzing 30+ empirical studies, 
we identify a trade-off between **Complexity Fit** (theoretical power) and **Data Fit** (robustness to messy data).
* **Quadrant 1 (Gold Standard):** Algorithms like *Boosting* & *Random Forest* that balance power with practicality.
* **Quadrant 4 (Deployment Gap):** Algorithms like *ANN* that are powerful but often too fragile for construction data.
""")

# --- 3. DATA LOADING (Embedded for Stability) ---
# We embed the data directly so the app doesn't break if a CSV is missing.
data_rows = [
    ('ANN', 0.82, 0.09, 0.82, 0.09, 9.7),
    ('Bayesian Networks', 0.00, 0.20, 0.00, 0.20, 0.9),
    ('Boosting/Gradient', 0.84, 0.74, 0.84, 0.74, 25.7),
    ('Decision Tree', 0.53, 0.28, 0.53, 0.28, 10.6),
    ('Ensemble', 0.80, 0.35, 0.80, 0.35, 11.5),
    ('Extremely Randomized Trees', 0.80, 0.80, 0.76, 0.82, 0.9),
    ('KNN', 0.40, 0.13, 0.40, 0.13, 5.3),
    ('Naïve-Bayesian', 0.00, 0.20, 0.02, 0.25, 1.8),
    ('Random Forest', 0.88, 0.67, 0.88, 0.67, 13.3),
    ('Regression', 0.19, 0.20, 0.19, 0.20, 12.4),
    ('SVM', 0.96, 0.20, 0.96, 0.20, 8.0)
]

df = pd.DataFrame(data_rows, columns=['category', 'True_C', 'True_D', 'Plot_C', 'Plot_D', 'Frequency'])
total_freq = df['Frequency'].sum()
df['Frequency_Pct'] = (df['Frequency'] / total_freq) * 100
df['Chart_Label'] = df.apply(lambda row: f"{row['category']}, {row['Frequency_Pct']:.1f}%", axis=1)
df['Legend_Label'] = df.apply(lambda row: f"{row['category']}, {row['Frequency_Pct']:.1f}% (C={row['True_C']:.2f}, D={row['True_D']:.2f})", axis=1)

# --- 4. SIDEBAR FILTERS ---
st.sidebar.header("Filter Options")
selected_algos = st.sidebar.multiselect(
    "Select Algorithms to Compare:",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Filter data based on selection
df_filtered = df[df['category'].isin(selected_algos)]

# --- 5. VISUALIZATION ---
# Professional Muted Pastel Palette
pastel_map = {
    'ANN': '#DBA9C7', 'Bayesian Networks': '#88C9D4', 'Boosting/Gradient': '#8FBC8F',
    'Decision Tree': '#B39EB5', 'Ensemble': '#F4C2C2', 'Extremely Randomized Trees': '#D9D98C',
    'KNN': '#A9A9A9', 'Naïve-Bayesian': '#BC8F8F', 'Random Forest': '#E9967A',
    'Regression': '#8CBED6', 'SVM': '#708090'
}

fig = px.scatter(
    df_filtered,
    x="Plot_C", y="Plot_D", size="Frequency", color="category",
    color_discrete_map=pastel_map, text="Chart_Label",
    size_max=80, template="plotly_white",
    hover_data={'Plot_C': False, 'Plot_D': False, 'True_C': ':.2f', 'True_D': ':.2f', 'Frequency': False, 'Frequency_Pct': ':.1f', 'Chart_Label': False, 'Legend_Label': False},
    labels={"Plot_C": "Complexity Fit (C)", "Plot_D": "Data Fit (D)"}
)

# Fix label alignment
fig.update_traces(textposition='middle center')

# Add Quadrant Backgrounds
c_median, d_median = 0.80, 0.20
fig.add_shape(type="rect", x0=c_median, y0=d_median, x1=1.1, y1=1.1, fillcolor="#F0F4F8", opacity=0.4, layer="below", line_width=0)
fig.add_shape(type="rect", x0=-0.1, y0=d_median, x1=c_median, y1=1.1, fillcolor="#F5F5F0", opacity=0.4, layer="below", line_width=0)
fig.add_shape(type="rect", x0=-0.1, y0=-0.1, x1=c_median, y1=d_median, fillcolor="#FAF0F0", opacity=0.4, layer="below", line_width=0)
fig.add_shape(type="rect", x0=c_median, y0=-0.1, x1=1.1, y1=d_median, fillcolor="#FDFDF0", opacity=0.4, layer="below", line_width=0)

fig.add_vline(x=c_median, line_width=1, line_dash="dash", line_color="grey")
fig.add_hline(y=d_median, line_width=1, line_dash="dash", line_color="grey")

# Add Quadrant Labels
grey_text = "rgba(100, 100, 100, 0.5)"
fig.add_annotation(x=0.4, y=0.65, text="Quadrant 2:<br>Simple & Robust", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.95, y=0.65, text="Quadrant 1:<br>Best of Both", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.4, y=0.1, text="Quadrant 3:<br>Limited Applicability", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.95, y=0.1, text="Quadrant 4:<br>Complex & Fragile", showarrow=False, font=dict(color=grey_text, size=16))

fig.update_layout(
    height=700,
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(range=[-0.1, 1.1], title_font=dict(size=18)),
    yaxis=dict(range=[-0.1, 1.1], title_font=dict(size=18)),
    showlegend=False # Hide legend to keep it clean (labels are on bubbles)
)

# Render Chart
st.plotly_chart(fig, use_container_width=True)

# --- 6. METHODOLOGY FOOTER ---
st.divider()
st.caption("""
**Methodology:** Data derived from a meta-analysis of 30 empirical studies. Scores (C, D, I, M) were calculated based on 12 algorithmic indicators.
For full reproducibility, view the [Source Code & Analysis Pipeline](https://github.com/[YOUR_GITHUB_USERNAME]/clemson_viz_entry).
""")