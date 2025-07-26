# HealthKart Influencer Dashboard

## Overview
The HealthKart Influencer Dashboard is a Streamlit-based web application designed to track and analyze influencer marketing campaigns for HealthKart across platforms (Instagram, YouTube, Twitter) and brands (MuscleBlaze, HKVitals, Gritzo). It provides actionable insights into campaign performance, Return on Ad Spend (ROAS), incremental ROAS, influencer effectiveness, and payout tracking, with a user-friendly interface for data visualization and export.

## Features
- **Data Upload**: Upload CSV files for influencers, posts, tracking data, and payouts with robust error handling.
- **Interactive Filters**: Filter by platform, brand, influencer category, and date range for tailored analysis.
- **Visualizations**:
  - Bar charts for orders and revenue by brand.
  - Combined ROAS and incremental ROAS by influencer.
  - Top 5 influencers by revenue with category breakdown.
  - Engagement trends over time (reach, likes, comments).
- **Payout Tracking**: Detailed table with formatted currency values for influencer payouts.
- **Insights Summary**: Key metrics and actionable recommendations for campaign optimization.
- **Export Options**:
  - Download campaign data as CSV.
  - Export insights as LaTeX source for PDF compilation.

## Installation

### Prerequisites
- Python 3.8 or higher
- A LaTeX compiler (e.g., `latexmk`) for PDF export compilation

### Dependencies
Install the required Python packages using pip:
```bash
pip install streamlit pandas plotly latex
