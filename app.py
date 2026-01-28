import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="ML Algorithm Selection Quadrant for Construction - Graduate Student Data Visualization Competition 2026 - Stuti Garg",
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
    ('Artifical Neural Network (ANN)', 0.82, 0.09, 0.82, 0.09, 9.7),
    ('Bayesian Networks', 0.00, 0.20, 0.00, 0.20, 0.9),
    ('Boosting/Gradient', 0.84, 0.74, 0.84, 0.74, 25.7),
    ('Decision Tree', 0.53, 0.28, 0.53, 0.28, 10.6),
    ('Ensemble', 0.80, 0.35, 0.80, 0.35, 11.5),
    ('Extremely Randomized Trees', 0.80, 0.80, 0.76, 0.82, 0.9),
    ('k-Nearest Neighbor (KNN)', 0.40, 0.13, 0.40, 0.13, 5.3),
    ('Naïve-Bayesian', 0.00, 0.20, 0.02, 0.25, 1.8),
    ('Random Forest', 0.88, 0.67, 0.88, 0.67, 13.3),
    ('Regression', 0.19, 0.20, 0.19, 0.20, 12.4),
    ('Support Vector Machine (SVM)', 0.96, 0.20, 0.96, 0.20, 8.0)
]

df = pd.DataFrame(data_rows, columns=['category', 'True_C', 'True_D', 'Plot_C', 'Plot_D', 'Frequency'])
total_freq = df['Frequency'].sum()
df['Frequency_Pct'] = (df['Frequency'] / total_freq) * 100
df['Chart_Label'] = df.apply(lambda row: f"{row['category']}, {row['Frequency_Pct']:.1f}%", axis=1)

# --- 4. SIDEBAR CONTROLS ---
st.sidebar.header("Highlight Method")

# DROP DOWN MENU
# Add "All Algorithms" to the top of the list
algo_options = ["All Algorithms"] + sorted(df['category'].unique())
selected_algo = st.sidebar.selectbox("Select View:", algo_options, index=0)

st.sidebar.divider()

# DETAILS PANEL (Conditional Logic Fixed)
if selected_algo == "All Algorithms":
    # OPTION A: Overview Mode (No 'row' variable exists here)
    st.sidebar.info("**Overview Mode**")
    st.sidebar.caption("This view shows all algorithm categories simultaneously. Hover over the bubbles to see specific performance metrics.")
    st.sidebar.markdown("""
    **Key:**
    * **X-Axis:** Complexity Fit (Power)
    * **Y-Axis:** Data Fit (Robustness)
    * **Size:** Usage Frequency
    """)
else:
    # OPTION B: Specific Method Mode
    # Extract data for the selected algorithm
    row = df[df['category'] == selected_algo].iloc[0]
    
    st.sidebar.subheader(f"📊 {selected_algo}")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Complexity (C)", f"{row['True_C']:.2f}", help="Ability to model non-linear, complex patterns.")
    with col2:
        st.metric("Data Fit (D)", f"{row['True_D']:.2f}", help="Robustness to missing data, small samples, and imbalance.")
    
    st.sidebar.caption(f"**Usage Frequency:** {row['Frequency_Pct']:.1f}% of studies")
    
    # Contextual interpretation based on quadrant
    # We use the Medians (C=0.80, D=0.20) as the cutoffs to match the chart lines
    
    if row['True_C'] > 0.80 and row['True_D'] > 0.20:
        st.sidebar.success("**Quadrant 1: Best of Both**\nHigh power and high robustness.")
    elif row['True_C'] > 0.80 and row['True_D'] <= 0.20:
        st.sidebar.warning("**Quadrant 4: Complex & Fragile**\nPowerful but sensitive to data quality.")
    elif row['True_C'] <= 0.80 and row['True_D'] >= 0.20:
        # Decision Tree (0.53, 0.28) and Naive-Bayesian (0.00, 0.20) fall here
        st.sidebar.info("**Quadrant 2: Simple & Robust**\nReliable for basic tasks.")
    else:
        st.sidebar.error("**Quadrant 3: Limited Applicability**\nLow power and low robustness.")

# --- 5. VISUALIZATION LOGIC ---

# Professional Muted Pastel Palette
pastel_map = {
    'Artifical Neural Network (ANN)': '#D68C9F',                    # Deep Dusty Rose (Darker/Redder)
    'Bayesian Networks': '#A6C6CC',      # Powder Teal
    'Boosting/Gradient': '#A3C1A3',      # Sage Green
    'Decision Tree': '#BFB5C2',          # Lilac Grey
    'Ensemble': '#E6C8C8',               # Dusty Rose
    'Extremely Randomized Trees': '#D1D1AA', # Khaki Pastel
    'k-Nearest Neighbor (KNN)': '#9FA8DA',                    # Muted Periwinkle (Now distinctly BLUE, not grey)
    'Naïve-Bayesian': '#C4AFAF',         # Mauve Taupe
    'Random Forest': '#DDB8AC',          # Peach Grey
    'Regression': '#ABC6D4',             # Slate Blue Pastel
    'Support Vector Machine (SVM)': '#78909C'                     # Blue Grey (Darker and distinct from the background)
}

# --- CUSTOM LABEL POSITIONS ---
custom_positions = {
    'ANN': 'top center',
    'Bayesian Networks': 'bottom center', 
    'Boosting/Gradient': 'top center',
    'Decision Tree': 'top center',
    'Ensemble': 'top center',
    'Extremely Randomized Trees': 'top left',
    'KNN': 'top center',
    'Naïve-Bayesian': 'top center',
    'Random Forest': 'bottom center',
    'Regression': 'top center',
    'SVM': 'middle left'
}

# 1. Create the Base Chart
fig = px.scatter(
    df,
    x="Plot_C", y="Plot_D", 
    size="Frequency", 
    color="category",
    color_discrete_map=pastel_map, 
    text="Chart_Label",
    size_max=80, template="plotly_white",
    hover_data={'Plot_C': False, 'Plot_D': False, 'True_C': ':.2f', 'True_D': ':.2f', 'Frequency': False, 'Frequency_Pct': ':.1f', 'Chart_Label': False},
    labels={"Plot_C": "Complexity Fit (C)", "Plot_D": "Data Fit (D)"}
)

# 2. Apply "Spotlight" Effect AND Custom Text Positions
for trace in fig.data:
    # A. Apply Custom Text Position
    # If the algorithm name is in our dictionary, use that position. Otherwise default to 'top center'.
    if trace.name in custom_positions:
        trace.textposition = custom_positions[trace.name]
    else:
        trace.textposition = 'top center'

    # B. Apply Opacity (Spotlight)
    if selected_algo == "All Algorithms":
        trace.marker.opacity = 1.0
        trace.textfont.color = 'black'
    elif trace.name == selected_algo:
        trace.marker.opacity = 1.0
        trace.textfont.color = 'black'
    else:
        trace.marker.opacity = 0.1
        trace.textfont.color = 'rgba(0,0,0,0.1)'

# Add Quadrant Backgrounds
c_median, d_median = 0.80, 0.20
fig.add_shape(type="rect", x0=c_median, y0=d_median, x1=1.1, y1=1.1, fillcolor="#F0F4F8", opacity=0.4, layer="below", line_width=0)
fig.add_shape(type="rect", x0=-0.1, y0=d_median, x1=c_median, y1=1.1, fillcolor="#F5F5F0", opacity=0.4, layer="below", line_width=0)
fig.add_shape(type="rect", x0=-0.1, y0=-0.1, x1=c_median, y1=d_median, fillcolor="#FAF0F0", opacity=0.4, layer="below", line_width=0)
fig.add_shape(type="rect", x0=c_median, y0=-0.1, x1=1.1, y1=d_median, fillcolor="#FDFDF0", opacity=0.4, layer="below", line_width=0)

fig.add_vline(x=c_median, line_width=1, line_dash="dash", line_color="grey")
fig.add_hline(y=d_median, line_width=1, line_dash="dash", line_color="grey")

# Add Quadrant Labels (Transparent Grey)
grey_text = "rgba(100, 100, 100, 0.6)"
fig.add_annotation(x=0.3, y=0.65, text="Quadrant 2:<br>Simple & Robust", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.95, y=0.65, text="Quadrant 1:<br>Best of Both", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.3, y=0.1, text="Quadrant 3:<br>Limited Applicability", showarrow=False, font=dict(color=grey_text, size=16))
fig.add_annotation(x=0.95, y=0.1, text="Quadrant 4:<br>Complex & Fragile", showarrow=False, font=dict(color=grey_text, size=16))

# --- LAYOUT UPDATE (SCIENTIFIC GRID) ---
fig.update_layout(
    height=700,
    margin=dict(l=40, r=40, t=60, b=40),
    showlegend=False,
    # X-Axis: Vertical Grids enabled
    xaxis=dict(
        range=[-0.1, 1.1], 
        title_font=dict(size=18),
        showgrid=True,        # Vertical Grid
        gridwidth=1,
        gridcolor='#E5E5E5',  # Subtle Grey
        showline=True,        # Axis Border
        linewidth=1, 
        linecolor='black',
        mirror=True           # Box Effect
    ),
    # Y-Axis: Horizontal Grids enabled
    yaxis=dict(
        range=[-0.1, 1.2], 
        title_font=dict(size=18),
        showgrid=True,        # Horizontal Grid
        gridwidth=1,
        gridcolor='#E5E5E5',
        showline=True,
        linewidth=1, 
        linecolor='black',
        mirror=True
    )
)

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

For full reproducibility, view the [Source Code & Analysis Pipeline](https://github.com/stutig-ops/clemson-viz-entry).

""")










