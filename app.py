import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Vitamin A Risk Dashboard", layout="wide")

st.title("📊 Vitamin A High-Risk Screening Dashboard")
st.markdown("This dashboard shows individuals aged above 30 years with Risk Score > 3 who have provided consent.")

# Load Data
df = pd.read_excel("Assignment_Dataset.xlsx", sheet_name="Dataset")

df['q7'] = pd.to_numeric(df['q7'], errors='coerce')
df['q46'] = pd.to_numeric(df['q46'], errors='coerce')

filtered = df[
    (df['q2'] == "Yes") &
    (df['q7'] > 30) &
    (df['q46'] > 3)
].copy()

# Load Codebook
codebook = pd.read_excel("Assignment_Dataset.xlsx", sheet_name="Codebook")

facility_map = codebook[
    codebook['list_name'] == 'health_facility'
][['Options', 'label::English (en)']]

facility_dict = dict(zip(facility_map['Options'], facility_map['label::English (en)']))

filtered['facility_name'] = filtered['health_facility'].map(facility_dict)

# Sidebar Filter
st.sidebar.header("Filter Options")
facility_options = ["All"] + sorted(filtered['facility_name'].unique().tolist())
selected_facility = st.sidebar.selectbox("Select Facility", facility_options)

if selected_facility != "All":
    filtered = filtered[filtered['facility_name'] == selected_facility]

# Summary
summary = (
    filtered
    .groupby('facility_name')
    .size()
    .reset_index(name='Persons Screened')
    .sort_values(by='Persons Screened', ascending=False)
)

total = summary['Persons Screened'].sum()
summary['% Total Screened'] = (summary['Persons Screened'] / total * 100).round(2)

# KPI Cards
col1, col2 = st.columns(2)
col1.metric("Total High-Risk Individuals", total)
col2.metric("Facilities Covered", summary.shape[0])

st.markdown("---")

# Bar Chart
st.subheader("Facility-wise High Risk Distribution")
fig1, ax1 = plt.subplots()
ax1.bar(summary['facility_name'], summary['Persons Screened'])
ax1.set_xlabel("Facility")
ax1.set_ylabel("Persons Screened")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.markdown("---")

# Age Distribution
st.subheader("Age Distribution")
fig2, ax2 = plt.subplots()
ax2.hist(filtered['q7'], bins=10)
ax2.set_xlabel("Age")
ax2.set_ylabel("Count")
st.pyplot(fig2)

st.markdown("---")

# Risk Score Distribution
st.subheader("Risk Score Distribution")
fig3, ax3 = plt.subplots()
ax3.hist(filtered['q46'], bins=10)
ax3.set_xlabel("Risk Score")
ax3.set_ylabel("Count")
st.pyplot(fig3)

st.markdown("---")

# Download Button
st.subheader("Download Filtered Data")
st.download_button(
    label="Download as CSV",
    data=filtered.to_csv(index=False),
    file_name="High_Risk_Filtered_Data.csv",
    mime="text/csv"
)

st.markdown("### Detailed Summary Table")
st.dataframe(summary, use_container_width=True)