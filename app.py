"""
FIFA World Cup 2026 - Player Performance Analytics Dashboard
Author: Muhammad Zarq Ali

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------------------------------------
# ROBUST DATA PATH RESOLUTION
# --------------------------------------------------------------------------------
# Streamlit's working directory depends on how/where you launch it from, so we
# resolve paths relative to this script's own location instead of assuming cwd.
APP_DIR = os.path.dirname(os.path.abspath(__file__))

CANDIDATE_FILENAMES = [
    "raw_data.csv",
    "fifa_world_cup_2026_player_performance.csv",
    "cleaned_fifa_wc2026_player_performance.csv",
]
CANDIDATE_DIRS = [
    os.path.join(APP_DIR, "data"),
    APP_DIR,
]


def resolve_data_path() -> str:
    for d in CANDIDATE_DIRS:
        for fname in CANDIDATE_FILENAMES:
            path = os.path.join(d, fname)
            if os.path.exists(path):
                return path
    searched = [os.path.join(d, f) for d in CANDIDATE_DIRS for f in CANDIDATE_FILENAMES]
    raise FileNotFoundError(
        "Could not find the dataset CSV. Place your CSV file inside a 'data' "
        "folder next to app.py (e.g. data/raw_data.csv), or update "
        "CANDIDATE_FILENAMES / CANDIDATE_DIRS at the top of app.py.\n"
        "Searched:\n- " + "\n- ".join(searched)
    )

# --------------------------------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------------------------------
st.set_page_config(
    page_title="FIFA World Cup 2026 | Player Performance Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------------
# STYLING
# --------------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main { background-color: #0e1117; }
        div[data-testid="stMetric"] {
            background-color: #161b22;
            border: 1px solid #262b33;
            border-radius: 10px;
            padding: 15px 10px;
            transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
            transform-style: preserve-3d;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 12px 24px rgba(0, 200, 255, 0.18);
            border-color: #00c8ff55;
        }
        div[data-testid="stMetricLabel"] { font-size: 14px; }
        h1, h2, h3 { color: #f5f5f5; }
        .footer {
            text-align: center;
            padding: 18px 0 6px 0;
            color: #8b949e;
            font-size: 13px;
            border-top: 1px solid #262b33;
            margin-top: 30px;
        }
        .subtitle { color: #8b949e; font-size: 16px; margin-top: -10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

PRIMARY_COLOR = "#00c8ff"
ACCENT_COLOR = "#ffb703"
PLOTLY_TEMPLATE = "plotly_dark"

# --------------------------------------------------------------------------------
# WEBGL 3D HERO BANNER (Three.js — real WebGL, rendered client-side)
# --------------------------------------------------------------------------------
HERO_WEBGL_HTML = """
<div id="hero3d" style="width:100%;height:260px;position:relative;overflow:hidden;
     border-radius:14px;background:radial-gradient(circle at 30% 30%, #131b2b 0%, #0a0e17 70%);
     border:1px solid #1f2734;">
  <canvas id="heroCanvas" style="display:block;width:100%;height:100%;"></canvas>
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
       text-align:center;pointer-events:none;width:90%;">
    <div style="font-size:clamp(22px,4vw,38px);font-weight:800;color:#f2f6fb;
         letter-spacing:1px;text-shadow:0 0 18px rgba(0,200,255,0.35);">
      ⚽ FIFA WORLD CUP 2026
    </div>
    <div style="font-size:15px;color:#9fb3c8;margin-top:8px;letter-spacing:0.5px;">
      Interactive 3D Player Performance Analytics &nbsp;•&nbsp; WebGL Powered
    </div>
  </div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/three.min.js"></script>
<script>
(function () {
  var container = document.getElementById('hero3d');
  var canvas = document.getElementById('heroCanvas');
  var width = container.clientWidth;
  var height = 260;

  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
  camera.position.z = 5.2;

  var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // --- Particle sphere (fibonacci sphere distribution) ---
  var particleCount = 700;
  var geometry = new THREE.BufferGeometry();
  var positions = new Float32Array(particleCount * 3);
  for (var i = 0; i < particleCount; i++) {
    var phi = Math.acos(-1 + (2 * i) / particleCount);
    var theta = Math.sqrt(particleCount * Math.PI) * phi;
    var r = 2.3;
    positions[i * 3] = r * Math.cos(theta) * Math.sin(phi);
    positions[i * 3 + 1] = r * Math.sin(theta) * Math.sin(phi);
    positions[i * 3 + 2] = r * Math.cos(phi);
  }
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  var material = new THREE.PointsMaterial({ color: 0x00c8ff, size: 0.045, transparent: true, opacity: 0.9 });
  var points = new THREE.Points(geometry, material);
  scene.add(points);

  // --- Wireframe icosahedron ("football" facets) ---
  var icoGeo = new THREE.IcosahedronGeometry(2.3, 1);
  var icoMat = new THREE.MeshBasicMaterial({ color: 0xffb703, wireframe: true, transparent: true, opacity: 0.28 });
  var ico = new THREE.Mesh(icoGeo, icoMat);
  scene.add(ico);

  // --- Faint outer ring of orbiting dots ---
  var ringCount = 120;
  var ringGeo = new THREE.BufferGeometry();
  var ringPos = new Float32Array(ringCount * 3);
  for (var j = 0; j < ringCount; j++) {
    var a = (j / ringCount) * Math.PI * 2;
    ringPos[j * 3] = Math.cos(a) * 3.4;
    ringPos[j * 3 + 1] = Math.sin(a) * 1.2;
    ringPos[j * 3 + 2] = Math.sin(a) * 0.6;
  }
  ringGeo.setAttribute('position', new THREE.BufferAttribute(ringPos, 3));
  var ringMat = new THREE.PointsMaterial({ color: 0xffffff, size: 0.02, transparent: true, opacity: 0.35 });
  var ring = new THREE.Points(ringGeo, ringMat);
  scene.add(ring);

  function animate() {
    requestAnimationFrame(animate);
    points.rotation.y += 0.0018;
    points.rotation.x += 0.0005;
    ico.rotation.y -= 0.0011;
    ico.rotation.x += 0.0009;
    ring.rotation.z += 0.0025;
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', function () {
    var w = container.clientWidth;
    camera.aspect = w / height;
    camera.updateProjectionMatrix();
    renderer.setSize(w, height);
  });
})();
</script>
"""


# --------------------------------------------------------------------------------
# DATA LOADING & CLEANING (cached)
# --------------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading and cleaning dataset...")
def load_data():
    df = pd.read_csv(resolve_data_path())

    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Drop exact duplicates
    df = df.drop_duplicates()

    # Fix dtypes
    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    cat_cols = [
        "nationality", "team", "position", "preferred_foot", "club_name",
        "stadium", "city", "opponent_team", "tournament_stage", "match_result",
    ]
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype("category")

    exclude = set(cat_cols + ["player_id", "player_name", "match_id", "match_date"])
    for c in df.columns:
        if c not in exclude:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Handle missing values: numeric performance stats -> 0, categorical -> "Unknown"
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    obj_cols = df.select_dtypes(include=["category"]).columns
    for c in obj_cols:
        if df[c].isnull().sum() > 0:
            if "Unknown" not in df[c].cat.categories:
                df[c] = df[c].cat.add_categories(["Unknown"])
            df[c] = df[c].fillna("Unknown")

    # Cap outliers (IQR method) for a few skew-prone columns
    for c in ["market_value_eur", "top_speed_kmh", "distance_covered_km"]:
        q1, q3 = df[c].quantile(0.25), df[c].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        df[c] = df[c].clip(lower=lower, upper=upper)

    # Derived columns
    df["goal_contributions"] = df["goals"] + df["assists"]
    df["shot_conversion_rate"] = np.where(df["shots"] > 0, df["goals"] / df["shots"], 0)
    df["dribble_success_rate"] = np.where(
        df["dribbles_attempted"] > 0, df["successful_dribbles"] / df["dribbles_attempted"], 0
    )
    df["match_month"] = df["match_date"].dt.to_period("M").astype(str)

    return df


df_raw = load_data()

# --------------------------------------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------------------------------------
st.sidebar.title("⚽ Filters")
st.sidebar.markdown("Use the filters below to explore the dataset.")

teams = sorted(df_raw["team"].unique().tolist())
selected_teams = st.sidebar.multiselect("Team(s)", teams, default=[])

positions = sorted(df_raw["position"].unique().tolist())
selected_positions = st.sidebar.multiselect("Position(s)", positions, default=[])

stages = list(df_raw["tournament_stage"].cat.categories) if hasattr(df_raw["tournament_stage"], "cat") else sorted(df_raw["tournament_stage"].unique())
stage_order = ["Group Stage", "Round of 32", "Round of 16", "Quarter Finals", "Semi Finals", "Third Place Match", "Final"]
stages_present = [s for s in stage_order if s in df_raw["tournament_stage"].unique()]
selected_stages = st.sidebar.multiselect("Tournament Stage(s)", stages_present, default=[])

age_min, age_max = int(df_raw["age"].min()), int(df_raw["age"].max())
age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))

foot_options = sorted(df_raw["preferred_foot"].unique().tolist())
selected_foot = st.sidebar.multiselect("Preferred Foot", foot_options, default=[])

min_minutes = st.sidebar.slider("Minimum Minutes Played (per match row)", 0, 90, 0)

# Apply filters
df = df_raw.copy()
if selected_teams:
    df = df[df["team"].isin(selected_teams)]
if selected_positions:
    df = df[df["position"].isin(selected_positions)]
if selected_stages:
    df = df[df["tournament_stage"].isin(selected_stages)]
if selected_foot:
    df = df[df["preferred_foot"].isin(selected_foot)]
df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]
df = df[df["minutes_played"] >= min_minutes]

st.sidebar.markdown("---")
st.sidebar.metric("Rows after filtering", f"{len(df):,}")
st.sidebar.markdown("---")
st.sidebar.caption("Built by **Muhammad Zarq Ali** — AI & Data Science Trainer")

# --------------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------------
components.html(HERO_WEBGL_HTML, height=270)

st.title("⚽ FIFA World Cup 2026 — Player Performance Dashboard")
st.markdown(
    '<p class="subtitle">An interactive analytics dashboard exploring player, team, and '
    'match-level performance data from the FIFA World Cup 2026.</p>',
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("No data matches the selected filters. Please adjust the filters in the sidebar.")
    st.stop()

# --------------------------------------------------------------------------------
# TABS
# --------------------------------------------------------------------------------
tab_overview, tab_performance, tab_teams, tab_3d, tab_trends, tab_data = st.tabs(
    ["📊 Overview", "🎯 Player Performance", "🌍 Team Analysis", "🧊 3D Analytics",
     "📈 Trends & Correlation", "🗂️ Data Explorer"]
)

# =================================================================================
# TAB 1: OVERVIEW (KPIs)
# =================================================================================
with tab_overview:
    st.subheader("Key Performance Indicators")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Players", f"{df['player_id'].nunique():,}")
    c2.metric("Total Teams", f"{df['team'].nunique():,}")
    c3.metric("Total Goals", f"{int(df['goals'].sum()):,}")
    c4.metric("Total Assists", f"{int(df['assists'].sum()):,}")
    c5.metric("Avg Player Rating", f"{df['player_rating'].mean():.2f}")

    c6, c7, c8, c9, c10 = st.columns(5)
    c6.metric("Avg Market Value", f"€{df['market_value_eur'].mean()/1e6:.1f}M")
    c7.metric("Avg Pass Accuracy", f"{df['pass_accuracy'].mean()*100:.1f}%")
    c8.metric("Total Yellow Cards", f"{int(df['yellow_cards'].sum()):,}")
    c9.metric("Total Red Cards", f"{int(df['red_cards'].sum()):,}")
    c10.metric("Clean Sheets", f"{int(df['clean_sheet'].sum()):,}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Goals by Position")
        pos_goals = df.groupby("position", observed=True)["goals"].sum().reset_index().sort_values("goals", ascending=False)
        fig = px.bar(pos_goals, x="position", y="goals", color="position",
                     template=PLOTLY_TEMPLATE, text_auto=True)
        fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Match Results Distribution")
        res_counts = df.drop_duplicates("match_id")["match_result"].value_counts().reset_index()
        res_counts.columns = ["result", "count"]
        fig = px.pie(res_counts, names="result", values="count", hole=0.5,
                     template=PLOTLY_TEMPLATE,
                     color_discrete_sequence=px.colors.sequential.Teal)
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### Preferred Foot Split")
        foot_counts = df.drop_duplicates("player_id")["preferred_foot"].value_counts().reset_index()
        foot_counts.columns = ["foot", "count"]
        fig = px.pie(foot_counts, names="foot", values="count", hole=0.5,
                     template=PLOTLY_TEMPLATE, color_discrete_sequence=[PRIMARY_COLOR, ACCENT_COLOR])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("##### Age Distribution")
        fig = px.histogram(df.drop_duplicates("player_id"), x="age", nbins=20,
                            template=PLOTLY_TEMPLATE, color_discrete_sequence=[PRIMARY_COLOR])
        fig.update_layout(height=350, bargap=0.05)
        st.plotly_chart(fig, use_container_width=True)

# =================================================================================
# TAB 2: PLAYER PERFORMANCE
# =================================================================================
with tab_performance:
    st.subheader("Player-Level Performance")

    player_agg = df.groupby(["player_id", "player_name", "team", "position"], observed=True).agg(
        total_goals=("goals", "sum"),
        total_assists=("assists", "sum"),
        avg_rating=("player_rating", "mean"),
        avg_xg=("expected_goals_xg", "mean"),
        total_minutes=("minutes_played", "sum"),
        market_value=("market_value_eur", "max"),
    ).reset_index()
    player_agg["goal_contributions"] = player_agg["total_goals"] + player_agg["total_assists"]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Top 10 Goal Scorers")
        top_scorers = player_agg.sort_values("total_goals", ascending=False).head(10)
        fig = px.bar(top_scorers, x="total_goals", y="player_name", orientation="h",
                     color="total_goals", template=PLOTLY_TEMPLATE,
                     color_continuous_scale="Blues", text="total_goals")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Top 10 Assist Providers")
        top_assists = player_agg.sort_values("total_assists", ascending=False).head(10)
        fig = px.bar(top_assists, x="total_assists", y="player_name", orientation="h",
                     color="total_assists", template=PLOTLY_TEMPLATE,
                     color_continuous_scale="Oranges", text="total_assists")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### Top 10 by Average Player Rating (min 180 mins)")
        qualified = player_agg[player_agg["total_minutes"] >= 180]
        top_rated = qualified.sort_values("avg_rating", ascending=False).head(10)
        fig = px.bar(top_rated, x="avg_rating", y="player_name", orientation="h",
                     color="avg_rating", template=PLOTLY_TEMPLATE,
                     color_continuous_scale="Viridis", text=top_rated["avg_rating"].round(2))
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("##### Most Valuable Players (Market Value)")
        top_value = player_agg.drop_duplicates("player_id").sort_values("market_value", ascending=False).head(10)
        fig = px.bar(top_value, x="market_value", y="player_name", orientation="h",
                     color="market_value", template=PLOTLY_TEMPLATE,
                     color_continuous_scale="Magma", text=(top_value["market_value"]/1e6).round(1).astype(str) + "M")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Distribution of Key Numerical Metrics")
    metric_choice = st.selectbox(
        "Select a metric to view its distribution and outliers",
        ["player_rating", "goals", "assists", "shots", "pass_accuracy", "distance_covered_km",
         "top_speed_kmh", "expected_goals_xg", "market_value_eur"],
    )
    col5, col6 = st.columns(2)
    with col5:
        fig = px.histogram(df, x=metric_choice, nbins=30, template=PLOTLY_TEMPLATE,
                            color_discrete_sequence=[PRIMARY_COLOR])
        fig.update_layout(height=380, bargap=0.05, title=f"Histogram — {metric_choice}")
        st.plotly_chart(fig, use_container_width=True)
    with col6:
        fig = px.box(df, y=metric_choice, x="position", template=PLOTLY_TEMPLATE,
                     color="position")
        fig.update_layout(height=380, showlegend=False, title=f"Box Plot by Position — {metric_choice}")
        st.plotly_chart(fig, use_container_width=True)

# =================================================================================
# TAB 3: TEAM ANALYSIS
# =================================================================================
with tab_teams:
    st.subheader("Team-Level Analysis")

    team_agg = df.groupby("team", observed=True).agg(
        total_goals=("goals", "sum"),
        avg_rating=("player_rating", "mean"),
        avg_pass_accuracy=("pass_accuracy", "mean"),
        total_market_value=("market_value_eur", "sum"),
        avg_distance=("distance_covered_km", "mean"),
        yellow_cards=("yellow_cards", "sum"),
        red_cards=("red_cards", "sum"),
    ).reset_index().sort_values("total_goals", ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Top 15 Teams by Total Goals")
        fig = px.bar(team_agg.head(15), x="team", y="total_goals", color="total_goals",
                     template=PLOTLY_TEMPLATE, color_continuous_scale="Teal")
        fig.update_layout(height=420, coloraxis_showscale=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Average Player Rating by Team (Top 15)")
        top_rated_teams = team_agg.sort_values("avg_rating", ascending=False).head(15)
        fig = px.bar(top_rated_teams, x="team", y="avg_rating", color="avg_rating",
                     template=PLOTLY_TEMPLATE, color_continuous_scale="Sunset")
        fig.update_layout(height=420, coloraxis_showscale=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### Discipline: Yellow vs Red Cards (Top 15 Teams by Cards)")
        disc = team_agg.copy()
        disc["total_cards"] = disc["yellow_cards"] + disc["red_cards"]
        disc = disc.sort_values("total_cards", ascending=False).head(15)
        fig = go.Figure()
        fig.add_bar(x=disc["team"], y=disc["yellow_cards"], name="Yellow Cards", marker_color="#f4d35e")
        fig.add_bar(x=disc["team"], y=disc["red_cards"], name="Red Cards", marker_color="#e63946")
        fig.update_layout(barmode="stack", template=PLOTLY_TEMPLATE, height=420, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("##### Squad Market Value (Top 15 Teams)")
        top_value_teams = team_agg.sort_values("total_market_value", ascending=False).head(15)
        fig = px.bar(top_value_teams, x="team", y="total_market_value", color="total_market_value",
                     template=PLOTLY_TEMPLATE, color_continuous_scale="Purples")
        fig.update_layout(height=420, coloraxis_showscale=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Team Comparison Table")
    st.dataframe(
        team_agg.style.format({
            "avg_rating": "{:.2f}", "avg_pass_accuracy": "{:.1%}",
            "total_market_value": "€{:,.0f}", "avg_distance": "{:.2f} km",
        }),
        use_container_width=True,
    )

# =================================================================================
# TAB 3B: 3D ANALYTICS (WebGL — Plotly scatter_3d renders via WebGL under the hood)
# =================================================================================
with tab_3d:
    st.subheader("🧊 3D Performance Analytics (WebGL)")
    st.caption(
        "These charts render with real WebGL — click and drag to rotate, "
        "scroll to zoom, and double-click to reset the view."
    )

    active_df = df[df["minutes_played"] > 0].copy()
    active_df["goal_contributions_sized"] = active_df["goal_contributions"].clip(lower=0) + 3

    st.markdown("##### Player Space: Work-Rate vs Defense vs Rating")
    fig3d_1 = px.scatter_3d(
        active_df,
        x="distance_covered_km", y="tackles", z="player_rating",
        color="position", size="goal_contributions_sized", size_max=16,
        opacity=0.75, template=PLOTLY_TEMPLATE,
        hover_name="player_name",
        hover_data={"team": True, "goals": True, "assists": True,
                    "goal_contributions_sized": False},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig3d_1.update_layout(
        height=650,
        scene=dict(
            xaxis_title="Distance Covered (km)",
            yaxis_title="Tackles",
            zaxis_title="Player Rating",
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig3d_1, use_container_width=True)

    st.markdown("##### Team Space: Goals vs Avg Rating vs Squad Value")
    team_3d = df.groupby("team", observed=True).agg(
        total_goals=("goals", "sum"),
        avg_rating=("player_rating", "mean"),
        total_market_value=("market_value_eur", "sum"),
        avg_distance=("distance_covered_km", "mean"),
    ).reset_index()

    fig3d_2 = px.scatter_3d(
        team_3d,
        x="total_goals", y="avg_rating", z="total_market_value",
        color="team", size="avg_distance", size_max=22,
        opacity=0.85, template=PLOTLY_TEMPLATE,
        hover_name="team",
    )
    fig3d_2.update_layout(
        height=650,
        showlegend=False,
        scene=dict(
            xaxis_title="Total Goals",
            yaxis_title="Avg Player Rating",
            zaxis_title="Squad Market Value (€)",
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig3d_2, use_container_width=True)

    st.markdown("##### 3D Performance Surface: Age vs Distance Covered vs Rating")
    surface_src = active_df.groupby(
        [pd.cut(active_df["age"], bins=8), pd.cut(active_df["distance_covered_km"], bins=8)],
        observed=True,
    )["player_rating"].mean().reset_index()
    surface_src["age_mid"] = surface_src["age"].apply(lambda i: i.mid).astype(float)
    surface_src["dist_mid"] = surface_src["distance_covered_km"].apply(lambda i: i.mid).astype(float)
    pivot = surface_src.pivot_table(index="dist_mid", columns="age_mid", values="player_rating")
    pivot = pivot.interpolate(axis=0).interpolate(axis=1).bfill().ffill()

    fig3d_3 = go.Figure(
        data=[go.Surface(
            z=pivot.values, x=pivot.columns, y=pivot.index,
            colorscale="Viridis", opacity=0.92,
            colorbar=dict(title="Avg Rating"),
        )]
    )
    fig3d_3.update_layout(
        template=PLOTLY_TEMPLATE, height=600,
        scene=dict(
            xaxis_title="Age",
            yaxis_title="Distance Covered (km)",
            zaxis_title="Avg Player Rating",
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig3d_3, use_container_width=True)

# =================================================================================
# TAB 4: TRENDS & CORRELATION
# =================================================================================
with tab_trends:
    st.subheader("Trends & Correlation Analysis")

    st.markdown("##### Goals Trend Across Tournament Stages")
    stage_trend = df.groupby("tournament_stage", observed=True).agg(
        total_goals=("goals", "sum"), avg_rating=("player_rating", "mean")
    ).reindex(stages_present).reset_index()
    fig = go.Figure()
    fig.add_bar(x=stage_trend["tournament_stage"], y=stage_trend["total_goals"],
                name="Total Goals", marker_color=PRIMARY_COLOR)
    fig.add_trace(go.Scatter(x=stage_trend["tournament_stage"], y=stage_trend["avg_rating"],
                              name="Avg Rating", yaxis="y2", mode="lines+markers",
                              line=dict(color=ACCENT_COLOR, width=3)))
    fig.update_layout(
        template=PLOTLY_TEMPLATE, height=420,
        yaxis=dict(title="Total Goals"),
        yaxis2=dict(title="Avg Rating", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Goals Over Time (by Month)")
        month_trend = df.groupby("match_month", observed=True)["goals"].sum().reset_index().sort_values("match_month")
        fig = px.line(month_trend, x="match_month", y="goals", markers=True,
                      template=PLOTLY_TEMPLATE, color_discrete_sequence=[PRIMARY_COLOR])
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### Expected Goals (xG) vs Actual Goals")
        scatter_df = df[df["minutes_played"] > 0]
        fig = px.scatter(scatter_df, x="expected_goals_xg", y="goals", color="position",
                          template=PLOTLY_TEMPLATE, opacity=0.5,
                          hover_data=["player_name", "team"])
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Correlation Heatmap of Key Performance Metrics")
    corr_cols = [
        "goals", "assists", "shots", "shots_on_target", "expected_goals_xg", "expected_assists_xa",
        "key_passes", "pass_accuracy", "tackles", "interceptions", "distance_covered_km",
        "top_speed_kmh", "player_rating", "market_value_eur",
    ]
    corr_matrix = df[corr_cols].corr().round(2)
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                     color_continuous_scale="RdBu_r", template=PLOTLY_TEMPLATE, zmin=-1, zmax=1)
    fig.update_layout(height=550)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##### Distance Covered vs Player Rating")
    fig = px.scatter(df[df["minutes_played"] > 0], x="distance_covered_km", y="player_rating",
                      color="position", trendline="ols" if False else None,
                      template=PLOTLY_TEMPLATE, opacity=0.5,
                      hover_data=["player_name", "team"])
    fig.update_layout(height=420)
    st.plotly_chart(fig, use_container_width=True)

# =================================================================================
# TAB 5: DATA EXPLORER
# =================================================================================
with tab_data:
    st.subheader("Raw / Cleaned Data Explorer")
    st.markdown(f"Showing **{len(df):,}** rows (filtered) out of **{len(df_raw):,}** total rows.")

    search_name = st.text_input("Search by player name")
    display_df = df.copy()
    if search_name:
        display_df = display_df[display_df["player_name"].str.contains(search_name, case=False, na=False)]

    st.dataframe(display_df, use_container_width=True, height=450)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered / Cleaned Dataset as CSV",
        data=csv_data,
        file_name="fifa_wc2026_cleaned_filtered.csv",
        mime="text/csv",
    )

    with st.expander("📋 Dataset Info"):
        st.write(f"**Shape:** {df_raw.shape[0]:,} rows × {df_raw.shape[1]:,} columns")
        st.write(f"**Missing values:** {df_raw.isnull().sum().sum()}")
        st.write(f"**Duplicate rows:** {df_raw.duplicated().sum()}")
        st.write("**Column data types:**")
        st.dataframe(df_raw.dtypes.astype(str).rename("dtype"), use_container_width=True)

# --------------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        ⚽ FIFA World Cup 2026 — Player Performance Dashboard &nbsp;|&nbsp;
        Built with Python, Pandas & Streamlit &nbsp;|&nbsp;
        Developed by <b>Muhammad Zarq Ali</b> — AI & Data Science Trainer
    </div>
    """,
    unsafe_allow_html=True,
)
