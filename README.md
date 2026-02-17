# Vitamin A High-Risk Screening Dashboard

## Objective
Identify individuals aged above 30 years with Risk Score > 3 who have provided consent.

## Data Engineering Steps
- Implemented facility nomenclature mapping using Codebook
- Applied filtering:
  - Consent = Yes
  - Age > 30
  - Risk Score > 3
- Generated facility-wise aggregation

## Key Insights
- Total High-Risk Individuals: 2293
- Highest Burden Facility: CHC Rajgarh (30.7%)
- Top 3 facilities contribute ~64% of total high-risk cases

## Dashboard Features
- Interactive facility filter
- KPI summary cards
- Age and Risk distribution charts
- Downloadable filtered dataset

## Deployment
This dashboard is deployed using Streamlit Community Cloud.
