import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ML Algorithm Selection Quadrant for Construction Industry",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. HEADER & ABSTRACT ---
st.title("ML Algorithm Selection Quadrant for Construction Industry")
st.markdown("""
**Visualization Narrative:** In a systematic literature review investigating 30 studies discussing applications of ML algorithms for construction industry 113 algorithmic implementations were grouped in 11 categories. 
A trade-off was identified and each algorithmic family was mapped to the quadrant, with the horizontal axis representing the average Complexity Fit (C) per family and the vertical axis representing the average Data Fit (D). 
X Axis: **Complexity Fit (C)** - measures the ability to capture complex, non‑linear, and high‑dimensional relationships
Y-Axis: **Data Fit (D)** - measures robustness to real-world construction data challenges - missing values, class imbalance, sample‑size variation
* **Quadrant 1:** Advanced and Sophisticated: (high C, high D) – Best of Both: Random Forest, Boosting/Gradient, and Ensemble families form a prominent cluster combining strong non‑linear modeling with comparatively better robustness to missing values, imbalance, and varying sample sizes. These families also have the largest bubbles, reflecting their high empirical maturity/adoption in the construction ML literature.
* **Quadrant 2:** Simple and Robust: (low C, high D) Regression, Naïve-Bayesian, and Decision trees represent the foundational methods that remain critical as baseline comparisons. These methods are better suited to linear relationships within variables/features and rely on clean, balanced data; they are unable to capture the inherent nonlinearity of construction data.
* **Quadrant 3:** Limited Applicability: (low C, low D) KNN models show weaker data fit despite modest complexity, suggesting applicability to a limited application.
* **Quadrant 4:** Complex and Fragile: (high C, low D) ANN scores exceptionally high in their ability to manage complex dataset interactions, with not much emphasis on handling missing data or rare event predictions. SVM, on the other hand, with kernel tricks, can handle multi-dimensional datasets that require synthetic oversampling to mitigate imbalanced classes.
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

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.header("Highlight Method")

# DROP DOWN MENU
# We use a selectbox for single-item selection
algo_options = sorted(df['category'].unique())
# Default to "Boosting/Gradient" if available, else first item
default_index = algo_options.index('Boosting/Gradient') if 'Boosting/Gradient' in algo_options else 0
selected_algo = st.sidebar.selectbox("Select an Algorithm:", algo_options, index=default_index)

# DETAILS PANEL (The Scores)
# Extract data for the selected algorithm
row = df[df['category'] == selected_algo].iloc[0]

st.sidebar.divider()
st.sidebar.subheader(f"📊 {selected_algo} Stats")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Complexity Fit (C)", f"{row['True_C']:.2f}", help="Ability to model non-linear, complex patterns.")
with col2:
    st.metric("Data Fit (D)", f"{row['True_D']:.2f}", help="Robustness to missing data, small samples, and imbalance.")

st.sidebar.caption(f"""
**Usage Frequency:** {row['Frequency_Pct']:.1f}%
""")

# --- 5. VISUALIZATION LOGIC ---

# Professional Muted Pastel Palette
pastel_map = {
    'ANN': '#DBA9C7', 'Bayesian Networks': '#88C9D4', 'Boosting/Gradient': '#8FBC8F',
    'Decision Tree': '#B39EB5', 'Ensemble': '#F4C2C2', 'Extremely Randomized Trees': '#D9D98C',
    'KNN': '#A9A9A9', 'Naïve-Bayesian': '#BC8F8F', 'Random Forest': '#E9967A',
    'Regression': '#8CBED6', 'SVM': '#708090'
}

# 1. Create the Base Chart (Draw everyone fully visible first)
fig = px.scatter(
    df,
    x="Plot_C", y="Plot_D", 
    size="Frequency", # Use standard frequency size
    color="category",
    color_discrete_map=pastel_map, 
    text="Chart_Label",
    size_max=80, template="plotly_white",
    hover_data={'Plot_C': False, 'Plot_D': False, 'True_C': ':.2f', 'True_D': ':.2f', 'Frequency': False, 'Frequency_Pct': ':.1f', 'Chart_Label': False},
    labels={"Plot_C": "Complexity Fit (C)", "Plot_D": "Data Fit (D)"}
)

# 2. Apply "Spotlight" Effect (The Fix)
# We loop through every trace (bubble group). If it matches the selection, we keep it bright.
# If it doesn't match, we turn the opacity down to 0.1 (Transparent).
for trace in fig.data:
    if selected_algo in trace.name:
        # SELECTED: Full Opacity, Bright Text
        trace.marker.opacity = 1.0
        trace.textfont.color = 'black'
    else:
        # UNSELECTED: Low Opacity, Faded Text
        trace.marker.opacity = 0.1
        trace.textfont.color = 'rgba(0,0,0,0.1)' # Make text almost invisible

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

# Add Quadrant Labels (Transparent Grey)
grey_text = "rgba(100, 100, 100, 0.4)"
fig.add_annotation(x=0.4, y=0.65, text="Quadrant 2:<br>Simple & Robust", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.95, y=0.65, text="Quadrant 1:<br>Best of Both", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.4, y=0.1, text="Quadrant 3:<br>Limited Applicability", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.95, y=0.1, text="Quadrant 4:<br>Complex & Fragile", showarrow=False, font=dict(color=grey_text, size=16))

fig.update_layout(
    height=700,
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(range=[-0.1, 1.1], title_font=dict(size=18)),
    yaxis=dict(range=[-0.1, 1.1], title_font=dict(size=18)),
    showlegend=False
)

# Render Chart
st.plotly_chart(fig, use_container_width=True)

# --- 6. METHODOLOGY FOOTER ---
st.divider()
st.caption("""
**Methodology:** Data derived from a meta-analysis of 30 empirical studies. Scores (C, D, I, M) were calculated based on 11 algorithmic indicators.
A systematic literature review following PRISMA guidelines analyzed 30 articles encompassing 113 algorithms used for construction applications. 
The development of the framework was a result of a four-stage process:
(1) synthesis and extraction of algorithmic characteristics from the findings of the SLR
(2) systematic coding of algorithms implementations based on the theoretical and empirical knowledge of performance patterns of the algorithms
(3) development of a multidimensional scoring framework
(4) quadrant-based visualization of the algorithms between model complexity, dataset characteristics and frequency of adoption

For full reproducibility, view the [Source Code & Analysis Pipeline](https://github.com/stutig-ops/clemson_viz_entry).

""")

