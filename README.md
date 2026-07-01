# ⚽ FIFA World Cup 2026 — Player Performance Analytics Dashboard

An end-to-end data analytics project: cleaning, exploratory data analysis (EDA),
and a fully interactive **Streamlit** dashboard built on a 54,600-row player
performance dataset from the FIFA World Cup 2026.

**Built by:** Muhammad Zarq Ali — AI & Data Science Trainer

---

## 📌 Project Overview

This project takes a raw, match-by-match player performance dataset (75 columns,
54,600 rows, 1,248 unique players across 48 teams and 1,050 matches) and turns it
into a polished, portfolio-ready analytics product:

1. A repeatable **data cleaning pipeline** (`clean_data.py`)
2. A complete **EDA notebook-style script** with statistics, distributions,
   correlation analysis, and business insights
3. A **multi-tab interactive Streamlit dashboard** (`app.py`) with KPI cards,
   sidebar filters, and 15+ interactive Plotly visualizations
4. A downloadable **cleaned dataset**

---

## 🗂️ Dataset Summary

| Item | Detail |
|---|---|
| Rows | 54,600 (one row per player, per match) |
| Columns | 75 original → 79 after feature engineering |
| Unique players | 1,248 |
| Teams | 48 |
| Matches | 1,050 |
| Tournament stages | Group Stage → Final (7 stages) |
| Missing values (raw) | 0 |
| Duplicate rows (raw) | 0 |
| Date range | 2026-06-11 to 2026-07-31 |

**Column groups:**
- **Identifiers:** `player_id`, `player_name`, `match_id`, `team`, `club_name`
- **Bio/attributes:** `age`, `nationality`, `height_cm`, `weight_kg`, `preferred_foot`, `position`, `market_value_eur`
- **Match context:** `match_date`, `stadium`, `city`, `opponent_team`, `tournament_stage`, `match_result`, `goals_team`, `goals_opponent`
- **Attacking stats:** `goals`, `assists`, `shots`, `shots_on_target`, `expected_goals_xg`, `expected_assists_xa`, `key_passes`, `dribbles_attempted`, `successful_dribbles`
- **Passing:** `successful_passes`, `total_passes`, `pass_accuracy`, `crosses`, `successful_crosses`
- **Defensive stats:** `tackles`, `interceptions`, `clearances`, `blocks`, `aerial_duels_won/lost`, `recoveries`
- **Discipline:** `fouls_committed`, `fouls_suffered`, `yellow_cards`, `red_cards`, `offsides`
- **Goalkeeping:** `saves`, `save_percentage`, `punches`, `clean_sheet`, `goals_conceded`, `penalty_saves`
- **Physical:** `distance_covered_km`, `sprint_distance_km`, `top_speed_kmh`, `accelerations`, `decelerations`, `stamina_score`
- **Composite scores:** `player_rating`, `performance_score`, `offensive/defensive_contribution`, `possession_impact`, `pressure_resistance`, `creativity_score`, `consistency_score`, `clutch_performance_score`
- **Tournament totals:** `total_goals_tournament`, `total_assists_tournament`, `total_minutes_tournament`, `player_of_match_awards`, `tournament_rating`

---

## 🧹 Data Cleaning Steps

1. **Column names** — stripped, lower-cased, spaces converted to underscores.
2. **Duplicates** — checked and removed (0 found in the raw file, pipeline still
   guards against future duplicate rows).
3. **Data types** — `match_date` parsed to `datetime`; categorical fields
   (`team`, `position`, `nationality`, etc.) cast to `category` for memory
   efficiency and faster dashboard filtering; all remaining stat columns
   coerced to numeric.
4. **Missing values** — none existed in the raw file, but the pipeline is
   defensive: numeric performance stats fill with `0` (a missing save/tackle
   count means "did not occur"), categorical fields fill with `"Unknown"`.
5. **Outliers** — capped using the IQR (1.5×) rule on three skew-prone columns
   (`market_value_eur`, `top_speed_kmh`, `distance_covered_km`) rather than
   deleting rows, to preserve sample size while limiting the influence of
   extreme values.
6. **Feature engineering** — added `goal_contributions` (goals + assists),
   `shot_conversion_rate`, `dribble_success_rate`, and `match_month` for
   trend analysis.

Run the cleaning pipeline standalone with:
```bash
python clean_data.py
```
This produces `data/cleaned_fifa_wc2026_player_performance.csv`.

---

## 🔍 Key EDA Insights

- **Goal output:** 3,024 total goals across 1,050 matches (~2.88 goals/match).
  Forwards contribute the majority of goals, followed by midfielders; defenders
  and goalkeepers contribute far fewer, as expected.
- **Foot preference:** ~74% of players are right-footed, ~26% left-footed —
  consistent with real-world football demographics.
- **Player rating drivers:** `player_rating` correlates most strongly with
  `distance_covered_km` (r ≈ 0.84) and `tackles` (r ≈ 0.50), suggesting the
  rating formula in this dataset rewards work-rate and defensive activity
  as much as, or more than, direct goal involvement (goals correlate at
  r ≈ 0.22).
- **Market value spread:** wide range (€0.5M to capped ~€200M+), heavily
  right-skewed — a small number of elite players hold disproportionate value,
  typical of real transfer markets.
- **Pass accuracy:** averages ~81%, tightly distributed (std ≈ 7%), indicating
  most players operate within a fairly narrow accuracy band regardless of
  position.
- **Discipline:** yellow cards (5,346 total) far outnumber red cards (306
  total), a realistic ~17:1 ratio.
- **Stage progression:** goal totals and average ratings shift across
  tournament stages, useful for spotting whether performance intensifies in
  knockout rounds.

---

## 📊 Business / Real-World Interpretation

- **Scouting:** the "Most Valuable Players" and "Top Rated (min 180 mins)"
  views isolate high-performing, high-value talent — a starting point for
  recruitment shortlists.
- **Team strategy:** the discipline chart flags teams accumulating cards,
  which correlates with suspension risk in later knockout rounds.
- **Fitness/medical staff:** the strong link between distance covered and
  rating highlights conditioning as a performance lever, not just technical skill.
- **Media/content:** top scorer and assist leaderboards are ready-made for
  social content or matchday graphics.

### Recommendations
1. Track `shot_conversion_rate` alongside raw goal counts to separate
   efficient finishers from high-volume shooters.
2. Monitor teams with rising card counts heading into knockout stages —
   suspension risk compounds in single-elimination formats.
3. Use `distance_covered_km` and `stamina_score` trends across stages to flag
   players at risk of fatigue-related dips in the later rounds.

---

## 🖥️ Dashboard Features

- **6 tabs:** Overview (KPIs), Player Performance, Team Analysis, **3D Analytics
  (WebGL)**, Trends & Correlation, Data Explorer
- **WebGL animated hero banner** — a real Three.js particle globe + wireframe
  football rendered client-side at the top of the dashboard
- **3D Analytics tab (WebGL via Plotly):**
  - Draggable 3D scatter: work-rate vs tackles vs player rating, colored by
    position, sized by goal contributions
  - Draggable 3D scatter: team goals vs avg rating vs squad market value
  - 3D surface plot: age vs distance covered vs average rating
  - All fully interactive — click-drag to rotate, scroll to zoom, double-click
    to reset
- **Hover-lift 3D tilt effect** on KPI cards for a more tactile, premium feel
- **Sidebar filters:** team, position, tournament stage, age range,
  preferred foot, minimum minutes played
- **KPI cards:** players, teams, goals, assists, avg rating, market value,
  pass accuracy, cards, clean sheets
- **15+ additional interactive Plotly charts:** bar, horizontal bar,
  pie/donut, histogram, box plot, scatter, line, stacked bar, correlation
  heatmap, dual-axis trend chart
- **Data Explorer tab:** searchable table + **CSV download button** for the
  filtered/cleaned dataset
- **Dark, professional theme** suited for client demos and portfolio screenshots

> **Note:** the WebGL hero banner loads Three.js from a public CDN
> (`cdnjs.cloudflare.com`). An internet connection is required for it to
> render — the rest of the dashboard works fully offline.

---

## 🚀 How to Run Locally

```bash
# 1. Clone or download this project folder
cd fifa-worldcup-2026-dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dashboard
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📁 Project Structure

```
fifa-worldcup-2026-dashboard/
├── app.py                                    # Streamlit dashboard (main entry point)
├── clean_data.py                             # Standalone data cleaning pipeline
├── requirements.txt                          # Python dependencies
├── README.md                                 # Project documentation (this file)
├── EDA_INSIGHTS_REPORT.md                    # Full written EDA + insights report
└── data/
    ├── raw_data.csv                          # Original uploaded dataset
    └── cleaned_fifa_wc2026_player_performance.csv   # Cleaned output
```

---

## 🛠️ Tech Stack

- **Python** — Pandas, NumPy for data wrangling
- **Plotly Express / Graph Objects** — interactive visualizations
- **Streamlit** — dashboard framework & deployment

---

## 👤 Author

**Muhammad Zarq Ali**
AI & Data Science Trainer | Python, Machine Learning & Analytics
Available for freelance data analytics and dashboard projects on Fiverr.

