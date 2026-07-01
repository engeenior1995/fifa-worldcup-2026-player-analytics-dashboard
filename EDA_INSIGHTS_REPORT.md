# 📊 EDA & Insights Report — FIFA World Cup 2026 Player Performance

Prepared by **Muhammad Zarq Ali**

---

## 1. Dataset Understanding

| Property | Value |
|---|---|
| Shape | 54,600 rows × 75 columns |
| Grain | One row = one player's stats in one match |
| Unique players | 1,248 |
| Unique teams | 48 |
| Unique matches | 1,050 |
| Tournament stages | Group Stage, Round of 32, Round of 16, Quarter Finals, Semi Finals, Third Place Match, Final |
| Missing values | 0 |
| Duplicate rows | 0 |
| Date range | 11 June 2026 – 31 July 2026 |

**Column type breakdown:**
- **Categorical (nominal):** `nationality`, `team`, `position`, `preferred_foot`, `club_name`, `stadium`, `city`, `opponent_team`, `tournament_stage`, `match_result`
- **Date/time:** `match_date`
- **Numerical (continuous/discrete):** the remaining 60+ columns — goals, assists, passing stats, physical metrics, and composite performance scores
- **Potential targets (for modeling):** `player_rating`, `tournament_rating`, or `goals` depending on the analytical question (rating prediction vs. goal-scoring prediction)

---

## 2. Data Cleaning Summary

The raw dataset was already well-structured (no missing values, no duplicates),
but the pipeline still applies defensive best practices:

| Step | Action | Why |
|---|---|---|
| Column names | Lower-cased, stripped, spaces → underscores | Consistent, code-friendly naming |
| Duplicates | `drop_duplicates()` | Guards against re-runs on updated data |
| Data types | `match_date` → datetime; categorical fields → `category` dtype | Enables date-based filtering/trends; speeds up dashboard filters |
| Missing values | Numeric → 0, categorical → "Unknown" | Preserves row count; 0 is semantically correct for count-based stats |
| Outliers | IQR (1.5×) capping on `market_value_eur`, `top_speed_kmh`, `distance_covered_km` | Limits the influence of extreme values without discarding data |
| Feature engineering | `goal_contributions`, `shot_conversion_rate`, `dribble_success_rate`, `match_month` | Adds analysis-ready derived metrics |

---

## 3. Summary Statistics (Selected Columns)

| Metric | Mean | Std Dev | Min | Max |
|---|---|---|---|---|
| Age | 26.3 | 4.1 | 17 | 39 |
| Goals (per match row) | 0.055 | 0.25 | 0 | 4 |
| Minutes played | 36.2 | 36.4 | 0 | 90 |
| Pass accuracy | 80.8% | 7.4% | 42% | 97% |
| Market value (EUR) | €20.1M | €27.2M | €0.53M | €200M |

---

## 4. Distribution & Outlier Findings

- **Age:** roughly normal, centered on 26, with a long-ish tail toward
  veteran players in their late 30s.
- **Market value:** heavily right-skewed — a small number of star players
  are valued far above the median, consistent with real transfer markets.
  IQR capping was applied for visualization purposes to avoid single
  outliers dominating charts.
- **Goals/assists (per match row):** highly zero-inflated, as expected —
  most players don't score in most matches; the meaningful signal is in
  the tournament-level totals (`total_goals_tournament`).
- **Pass accuracy:** tightly distributed around 81%, with goalkeepers and
  defenders trending slightly different from attacking players.

---

## 5. Categorical Breakdown

- **Preferred foot:** ~74% right-footed, ~26% left-footed.
- **Position:** Midfielders and Defenders make up the largest share of
  rows (reflecting squad composition — more outfield players than
  forwards or goalkeepers), while **Forwards score the most total goals**
  by a wide margin, followed by Midfielders.
- **Match results:** balanced roughly across Win/Draw/Loss labels at the
  match level, as expected in a tournament format.

---

## 6. Correlation Analysis

Correlation of key metrics with `player_rating`:

| Metric | Correlation with player_rating |
|---|---|
| Distance covered (km) | **0.84** |
| Tackles | 0.50 |
| Shots | 0.42 |
| Goals | 0.22 |
| Expected goals (xG) | 0.19 |
| Assists | 0.20 |
| Pass accuracy | 0.07 |

**Interpretation:** in this dataset, work-rate (distance covered) and
defensive engagement (tackles) are stronger drivers of the composite
`player_rating` than raw attacking output. This is a notable and
counter-intuitive insight worth highlighting to stakeholders — it
suggests the rating formula rewards overall contribution and effort over
pure goal-scoring, which is a useful talking point for a portfolio piece.

---

## 7. Group-By Analysis Highlights

- **Top goal scorer (tournament total):** Memphis Zerrouki — 24 goals
- **Top assist provider (tournament total):** Yassine El Yamiq — 13 assists
- **Highest market value player:** Stefan Lainer (~€51.9M)
- **Goals by position:** Forwards ≫ Midfielders > Defenders ≫ Goalkeepers
  (goalkeepers recorded 0 goals, as expected)
- **Discipline:** 5,346 total yellow cards vs. 306 total red cards (~17:1 ratio)

---

## 8. Trend Analysis

- Goal totals and average player ratings shift measurably across
  tournament stages (Group Stage → Final), useful for identifying whether
  teams/players raise their level in knockout football.
- A month-over-month view (`match_month`) tracks goal output across the
  tournament calendar (June–July 2026).

---

## 9. Business Insights & Recommendations

1. **Recruitment/Scouting:** Combine `avg_rating` (filtered to players
   with meaningful minutes) with `market_value_eur` to identify
   under-priced, high-performing players — a classic "value for money"
   scouting lens.
2. **Fitness & Conditioning:** Given the strong link between distance
   covered and rating, conditioning programs that sustain work-rate
   through the tournament could have an outsized impact on player ratings.
3. **Discipline Risk Management:** Teams accumulating yellow cards should
   be flagged ahead of knockout rounds, where one more caution can mean a
   suspension at a critical stage.
4. **Content & Fan Engagement:** Leaderboards (top scorers, assists, MVPs)
   are directly reusable for social media graphics, matchday previews, or
   fantasy football content.
5. **Efficiency Metrics:** Track `shot_conversion_rate` alongside raw shot
   volume to distinguish clinical finishers from high-volume, low-efficiency
   shooters.

---

## 10. Portfolio-Friendly Summary

> This project analyzes 54,600 player-match performance records from the
> FIFA World Cup 2026, covering 1,248 players across 48 national teams.
> After a full cleaning and feature-engineering pipeline, the analysis
> uncovers a counter-intuitive insight: **work-rate and defensive activity
> correlate more strongly with composite player ratings than raw goals or
> assists do.** The findings are delivered through a 5-tab interactive
> Streamlit dashboard with 15+ visualizations, sidebar filtering, and a
> live CSV export — built to demonstrate end-to-end data analytics and
> dashboard engineering skills for a data analyst / BI portfolio.

