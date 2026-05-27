import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato Global Dashboard",
    page_icon="🍽️",
    layout="wide"
)

pio.templates.default = "plotly_white"

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>

.main {
    background-color: #050816;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #0F172A 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Hero */

.hero {
    background: linear-gradient(135deg, #FF0000 0%, #B30000 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 24px rgba(255,0,0,0.3);
}

.hero h1 {
    margin: 0;
    font-size: 40px;
    font-weight: 800;
}

.hero p {
    margin-top: 10px;
    font-size: 16px;
    opacity: 0.9;
}

/* KPI Cards */

.kpi-card {
    background: linear-gradient(135deg, #FF0000 0%, #B30000 100%);
    padding: 1.5rem;
    border-radius: 18px;
    text-align: center;
    color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
}

.kpi-label {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 10px;
}

.kpi-value {
    font-size: 34px;
    font-weight: 800;
}

.kpi-sub {
    margin-top: 8px;
    font-size: 13px;
    opacity: 0.85;
}

/* Section Headers */

.section-header {
    font-size: 24px;
    font-weight: 800;
    color: white;
    margin-bottom: 1rem;
    border-bottom: 3px solid #FF2B2B;
    display: inline-block;
    padding-bottom: 5px;
}

/* Insight Cards */

.finding {
    background: #111827;
    border-left: 5px solid #FF2B2B;
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 10px;
}

/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #111827;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    background-color: #FF0000 !important;
    color: white !important;
}

/* Hide Streamlit */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
} 
            /* KPI Card hover */
.kpi-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(255, 0, 0, 0.5);
}

/* Executive summary card hover */
.exec-card {
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.exec-card:hover {
    transform: translateX(4px);
    border-left-color: #FF6666 !important;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():

    df = pd.read_csv("data/zomato_clean.csv")

    country_map = {
        1:'India',
        14:'Australia',
        30:'Brazil',
        37:'Canada',
        94:'Indonesia',
        148:'New Zealand',
        162:'Philippines',
        166:'Qatar',
        184:'Singapore',
        189:'South Africa',
        191:'Sri Lanka',
        208:'Turkey',
        214:'United Arab Emirates',
        215:'United Kingdom',
        216:'United States'
    }

    df['country'] = df['country_code'].map(country_map)

    return df

df = load_data()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("# 🍽️ Zomato Dashboard")
st.sidebar.markdown("### Global Restaurant Analytics")

st.sidebar.markdown("---")

countries = st.sidebar.multiselect(
    "🌍 Country",
    sorted(df['country'].dropna().unique()),
    default=sorted(df['country'].dropna().unique())
)

min_cost = int(df['approx_cost'].min())
max_cost = int(df['approx_cost'].max())

cost_range = st.sidebar.slider(
    "💰 Cost for Two",
    min_value=min_cost,
    max_value=max_cost,
    value=(min_cost, max_cost)
)

online_filter = st.sidebar.radio(
    "🛵 Online Delivery",
    ["All", "Yes", "No"]
)

# ─────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────
filtered = df[
    (df['country'].isin(countries)) &
    (df['approx_cost'] >= cost_range[0]) &
    (df['approx_cost'] <= cost_range[1])
]

if online_filter == "Yes":
    filtered = filtered[filtered['online_order'] == True]

elif online_filter == "No":
    filtered = filtered[filtered['online_order'] == False]

if filtered.empty:
    st.warning("No data available.")
    st.stop()

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">

<h1>🍽️ Zomato Global Restaurant Analytics</h1>

<p>
Explore ratings, cuisines and pricing trends across
{filtered['country'].nunique()} countries 🌍
</p>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🍽️ Restaurants</div>
        <div class="kpi-value">{len(filtered):,}</div>
        <div class="kpi-sub">Total restaurants</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">⭐ Avg Rating</div>
        <div class="kpi-value">{filtered['rate'].mean():.2f}</div>
        <div class="kpi-sub">Out of 5 stars</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">💰 Avg Cost</div>
        <div class="kpi-value">₹ {filtered['approx_cost'].mean():,.0f}</div>
        <div class="kpi-sub">For two people</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🗳️ Votes</div>
        <div class="kpi-value">{filtered['votes'].sum():,}</div>
        <div class="kpi-sub">Customer engagement</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EXECUTIVE SUMMARY
# ─────────────────────────────────────────────
st.markdown("""
<div style="background:#111827; border-radius:16px; padding:1.5rem 2rem; margin-bottom:1.5rem;">
    <div style="font-size:20px; font-weight:800; color:white; margin-bottom:1rem; border-bottom:3px solid #FF2B2B; padding-bottom:8px; display:inline-block;">
        📋 Executive Summary
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:1rem;">
        <div style="background:#1F2937; border-left:4px solid #FF2B2B; border-radius:0 10px 10px 0; padding:1rem;">
            <div style="font-size:13px; color:#9CA3AF; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Dataset Coverage</div>
            <div style="font-size:15px; color:white; font-weight:600;">15 countries · 7,394 restaurants</div>
            <div style="font-size:13px; color:#9CA3AF; margin-top:4px;">India accounts for 88% of all listings</div>
        </div>
        <div style="background:#1F2937; border-left:4px solid #FF2B2B; border-radius:0 10px 10px 0; padding:1rem;">
            <div style="font-size:13px; color:#9CA3AF; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Cost & Quality</div>
            <div style="font-size:15px; color:white; font-weight:600;">Correlation of 0.88</div>
            <div style="font-size:13px; color:#9CA3AF; margin-top:4px;">Higher spend strongly predicts better ratings</div>
        </div>
        <div style="background:#1F2937; border-left:4px solid #FF2B2B; border-radius:0 10px 10px 0; padding:1rem;">
            <div style="font-size:13px; color:#9CA3AF; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Delivery Insight</div>
            <div style="font-size:15px; color:white; font-weight:600;">Dine-in rates higher (3.47 vs 3.38)</div>
            <div style="font-size:13px; color:#9CA3AF; margin-top:4px;">Online delivery restaurants score slightly lower</div>
        </div>
        <div style="background:#1F2937; border-left:4px solid #FF2B2B; border-radius:0 10px 10px 0; padding:1rem;">
            <div style="font-size:13px; color:#9CA3AF; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.5px;">Surprising Finding</div>
            <div style="font-size:15px; color:white; font-weight:600;">No-booking places rate higher (3.59 vs 3.41)</div>
            <div style="font-size:13px; color:#9CA3AF; margin-top:4px;">Table booking doesn't guarantee better quality</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHART THEME
# ─────────────────────────────────────────────
CHART_THEME = dict(

    plot_bgcolor="white",

    paper_bgcolor="white",

    font=dict(
        family="Arial",
        size=14,
        color="black"
    ),

    title_font=dict(
        size=22,
        color="black"
    ),

    xaxis=dict(
        title_font=dict(
            size=15,
            color="black"
        ),
        tickfont=dict(
            size=13,
            color="black"
        ),
        showgrid=False
    ),

    yaxis=dict(
        title_font=dict(
            size=15,
            color="black"
        ),
        tickfont=dict(
            size=13,
            color="black"
        ),
        gridcolor="rgba(0,0,0,0.1)"
    ),

    legend=dict(
        font=dict(
            color="black"
        )
    ),

    margin=dict(
        t=60,
        l=20,
        r=20,
        b=20
    )
)

RED_SCALE = [
    "#FFD6D6",
    "#FFB3B3",
    "#FF6666",
    "#FF0000",
    "#C40000",
    "#8B0000"
]

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Overview",
    "🌍 Geography",
    "🍜 Cuisine",
    "🧠 Business",
    "🔥 Correlation",
    "🗺️ World Map"
])

# ─────────────────────────────────────────────
# OVERVIEW
# ─────────────────────────────────────────────
with tab1:

    col1, col2 = st.columns(2)

    with col1:

        country_counts = filtered['country'].value_counts().reset_index()
        country_counts.columns = ['country', 'count']

        fig1 = px.bar(
            country_counts,
            x='country',
            y='count',
            color='count',
            color_continuous_scale=RED_SCALE
        )

        fig1.update_layout(
            **CHART_THEME,
            title="Restaurants by Country",
            coloraxis_showscale=False,
            hoverlabel=dict(
                bgcolor="#1F2937",
                font_size=13,
                font_color="white",
                bordercolor="#FF2B2B"
            )
        )

        st.plotly_chart(fig1, use_container_width=True)

    with col2:

        fig2 = px.scatter(
            filtered,
            x='approx_cost',
            y='rate',
            color='country',
            opacity=0.7,
            hover_data=['name', 'city']
        )

        fig2.update_layout(
            **CHART_THEME,
            title="Cost vs Rating"
        )

        st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────
# GEOGRAPHY
# ─────────────────────────────────────────────

with tab2:

    col3, col4 = st.columns(2)

    with col3:

        avg_country_rating = (
            filtered.groupby('country')['rate']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig3 = px.bar(
            avg_country_rating,
            x='country',
            y='rate',
            color='rate',
            color_continuous_scale=RED_SCALE
        )

        fig3.update_layout(
            **CHART_THEME,
            title="Average Rating by Country",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig3, use_container_width=True)

    with col4:

        avg_country_cost = (
            filtered.groupby('country')['approx_cost']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )

        fig4 = px.bar(
            avg_country_cost,
            x='country',
            y='approx_cost',
            color='approx_cost',
            color_continuous_scale=RED_SCALE
        )

        fig4.update_layout(
            **CHART_THEME,
            title="Average Cost by Country",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# CUISINE
# ─────────────────────────────────────────────
with tab3:

    col5, col6 = st.columns(2)

    cuisines = (
        filtered['cuisines']
        .dropna()
        .str.split(',')
        .explode()
        .str.strip()
    )

    top_cuisines = cuisines.value_counts().head(10).reset_index()
    top_cuisines.columns = ['cuisine', 'count']

    with col5:

        fig5 = px.bar(
            top_cuisines,
            x='count',
            y='cuisine',
            orientation='h',
            color='count',
            color_continuous_scale=RED_SCALE
        )

        fig5.update_layout(
            **CHART_THEME,
            title="Top 10 Cuisines",
            coloraxis_showscale=False
        )

        st.plotly_chart(fig5, use_container_width=True)

    with col6:

        fig6 = px.pie(
            top_cuisines,
            names='cuisine',
            values='count',
            hole=0.5
        )

        fig6.update_layout(
            **CHART_THEME,
            title="Cuisine Share"
        )

        st.plotly_chart(fig6, use_container_width=True)

# ─────────────────────────────────────────────
# BUSINESS
# ─────────────────────────────────────────────
with tab4:

    col7, col8 = st.columns(2)

    with col7:

        delivery_data = (
            filtered.groupby('online_order')['rate']
            .mean()
            .reset_index()
        )

        delivery_data['Service'] = delivery_data['online_order'].map({
            True: 'Online Delivery',
            False: 'Dine In'
        })

        fig7 = px.bar(
            delivery_data,
            x='Service',
            y='rate',
            color='Service',
            text_auto='.2f'
        )

        fig7.update_layout(
            **CHART_THEME,
            title="Delivery vs Dine-In Ratings"
        )

        st.plotly_chart(fig7, use_container_width=True)

    with col8:

        fig8 = px.scatter(
            filtered,
            x='votes',
            y='rate',
            color='country',
            opacity=0.7
        )

        fig8.update_layout(
            **CHART_THEME,
            title="Votes vs Ratings"
        )

        st.plotly_chart(fig8, use_container_width=True)

# ─────────────────────────────────────────────
# CORRELATION
# ─────────────────────────────────────────────
with tab5:

    corr_df = filtered[
        ['rate', 'votes', 'approx_cost']
    ].corr()

    fig9 = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale=RED_SCALE
    )

    fig9.update_layout(
        **CHART_THEME,
        title="Feature Correlation Matrix"
    )

    st.plotly_chart(fig9, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    insights = [

        "🌍 India dominates the restaurant dataset.",

        f"⭐ Average restaurant rating is {filtered['rate'].mean():.2f}.",

        f"💰 Average cost for two is ₹ {filtered['approx_cost'].mean():,.0f}.",

        f"🗳️ Total customer votes exceed {filtered['votes'].sum():,}."
    ]

    for item in insights:

        st.markdown(
            f'<div class="finding">{item}</div>',
            unsafe_allow_html=True
        )
        # ─────────────────────────────────────────────
# WORLD MAP
# ─────────────────────────────────────────────
with tab6:
    country_counts = filtered['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'count']

    fig_map = px.choropleth(
        country_counts,
        locations='country',
        locationmode='country names',
        color='count',
        color_continuous_scale=RED_SCALE,
        hover_name='country',
        labels={'count': 'Restaurants'},
    )
    fig_map.update_layout(
        **CHART_THEME,
        title="Global Restaurant Distribution",
        geo=dict(
    showframe=False,
    showcoastlines=True,
    coastlinecolor="#999999",
    showland=True,
    landcolor="#E0E0E0",
    showocean=True,
    oceancolor="#C8D8E8",
    showcountries=True,
    countrycolor="#AAAAAA",
    projection_type='natural earth'
),
        height=500,
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ─────────────────────────────────────────────
# DOWNLOAD
# ─────────────────────────────────────────────
st.markdown("---")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="zomato_filtered.csv",
    mime="text/csv"
)