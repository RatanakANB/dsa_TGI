import os
import sys
import pandas as pd
import numpy as np
import datetime

import streamlit as st
import plotly.express as px

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING (CROSS-PLATFORM & NO EMOJIS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="RPL Dashboard - Interactive Analytics",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean aesthetics and Khmer typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Kantumruy Pro', 'Inter', sans-serif;
    }
    
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        font-size: 1.05rem;
        color: #6c757d;
        margin-bottom: 1.5rem;
    }
    
    .stTable {
        border-radius: 8px;
        overflow: hidden;
    }

    .block-container {
        width: 100%;
        max-width: 1400px;
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING & PREPROCESSING (CROSS-PLATFORM & DYNAMIC DATE FETCHING)
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_preprocess_data():
    csv_path = os.path.join(os.path.dirname(__file__), "RPL_Dashboard_V.1.csv") if __file__ else "RPL_Dashboard_V.1.csv"
    if not os.path.exists(csv_path):
        csv_path = "RPL_Dashboard_V.1.csv"
        
    df = pd.read_csv(csv_path)
    
    # Parse Date_Committee_Meeting cross-platform
    df['CM_Date'] = pd.to_datetime(df['Date_Committee_Meeting'], format='%d-%b-%y', errors='coerce')
    
    # Extract date attributes
    df['CM_Year'] = df['CM_Date'].dt.year
    df['CM_Quarter'] = 'Qtr' + df['CM_Date'].dt.quarter.astype(str)
    df['CM_Month_Name'] = df['CM_Date'].dt.strftime('%b')
    df['CM_Date_Only'] = df['CM_Date'].dt.date
    
    # Format date string as M/D/YYYY (e.g. 11/16/2020, 1/26/2022)
    df['CM_Date_Str'] = df['CM_Date'].dt.month.astype(str) + '/' + df['CM_Date'].dt.day.astype(str) + '/' + df['CM_Date'].dt.year.astype(str)
    
    # Drop DI, DE, EN target columns, and explicit unwanted columns (keeping Date_Committee_Meeting)
    explicit_drops = ['Serial_Code', 'Path', 'Pics', 'CardNo']
    cm_sub_cols = ['CM_Day_KH', 'CM_Month_KH', 'CM_Year_KH']
    di_cols = [c for c in df.columns if c.startswith('DI') or 'Date_Issue' in c]
    de_cols = [c for c in df.columns if c.startswith('DE') or 'Date_Expiry' in c]
    en_cols = ['Gender_EN', 'Occupation_EN', 'NQ_EN', 'AT_EN']
    
    all_drops = list(set(explicit_drops + cm_sub_cols + di_cols + de_cols + en_cols))
    df_clean = df.drop(columns=[c for c in all_drops if c in df.columns]).copy()
    
    return df_clean

df_cleaned = load_and_preprocess_data()

# -----------------------------------------------------------------------------
# HEADER SECTION
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">RPL Dashboard - Interactive Data Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Data Insights & Visualizations Filtered by Date_Committee_Meeting</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR INTERACTIVE FILTERS (4 COMMITTEE MEETING DATE FILTERS)
# -----------------------------------------------------------------------------
st.sidebar.header("Interactive Date Filters")
st.sidebar.markdown("Filter all 5 findings by **Date_Committee_Meeting** attributes:")

# Filter 1: Committee Meeting Specific Date [Committee_Meeting(date)]
st.sidebar.subheader("1. Specific Meeting Date")
# Dynamically fetch unique sorted meeting dates from Date_Committee_Meeting
unique_date_objects = sorted(df_cleaned['CM_Date'].dropna().unique())
date_options_map = {
    f"{pd.Timestamp(d).month}/{pd.Timestamp(d).day}/{pd.Timestamp(d).year}": d
    for d in unique_date_objects
}
available_date_strings = list(date_options_map.keys())

selected_date_strings = st.sidebar.multiselect(
    "Select Meeting Date(s)",
    options=available_date_strings,
    default=available_date_strings
)

# Filter 2: Committee Meeting Year [Committee_Meeting(year)]
st.sidebar.subheader("2. Committee Meeting Year")
available_years = sorted(df_cleaned['CM_Year'].dropna().unique().astype(int))
selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=available_years,
    default=available_years
)

# Filter 3: Committee Meeting Quarter [Committee_Meeting(Quarter)]
st.sidebar.subheader("3. Committee Meeting Quarter")
available_quarters = ['Qtr1', 'Qtr2', 'Qtr3', 'Qtr4']
selected_quarters = st.sidebar.multiselect(
    "Select Quarter(s)",
    options=available_quarters,
    default=available_quarters
)

# Filter 4: Committee Meeting Month [Committee_Meeting(Month)]
st.sidebar.subheader("4. Committee Meeting Month")
months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
available_months = [m for m in months_order if m in df_cleaned['CM_Month_Name'].unique()]
selected_months = st.sidebar.multiselect(
    "Select Month(s)",
    options=available_months,
    default=available_months
)

# Reset Filters Button
if st.sidebar.button("Reset All Filters"):
    st.rerun()

# -----------------------------------------------------------------------------
# FILTER DATA APPLICATION
# -----------------------------------------------------------------------------
mask = (
    (df_cleaned['CM_Date_Str'].isin(selected_date_strings)) &
    (df_cleaned['CM_Year'].isin(selected_years)) &
    (df_cleaned['CM_Quarter'].isin(selected_quarters)) &
    (df_cleaned['CM_Month_Name'].isin(selected_months))
)

filtered_df = df_cleaned[mask].copy()

if filtered_df.empty:
    st.warning("No records match the selected Committee Meeting date filter criteria. Please adjust your filters in the sidebar.")
    st.stop()

# -----------------------------------------------------------------------------
# TOP METRICS CARDS
# -----------------------------------------------------------------------------
total_candidates = len(filtered_df)
male_count = len(filtered_df[filtered_df['Gender_KH'] == 'ប្រុស'])
female_count = len(filtered_df[filtered_df['Gender_KH'] == 'ស្រី'])
female_pct = (female_count / total_candidates * 100) if total_candidates > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Candidates", f"{total_candidates:,}")
with col2:
    st.metric("Male (ប្រុស)", f"{male_count:,}", f"{(male_count/total_candidates*100):.1f}%")
with col3:
    st.metric("Female (ស្រី)", f"{female_count:,}", f"{female_pct:.1f}%")
with col4:
    st.metric("Selected Dates Count", f"{len(selected_date_strings)} / {len(available_date_strings)}")

st.markdown("---")

# -----------------------------------------------------------------------------
# GENERATE VISUALIZATIONS & DATA TABLES FOR ALL 5 FINDINGS
# -----------------------------------------------------------------------------

# Finding 1: Gender Distribution
gender_ct = pd.crosstab(filtered_df['Gender_KH'], columns='Candidate Count')
gender_ct['Percentage (%)'] = (gender_ct['Candidate Count'] / total_candidates * 100).round(2)
gender_ct.loc['Total'] = [total_candidates, 100.0]

gender_counts = filtered_df['Gender_KH'].value_counts().reset_index()
gender_counts.columns = ['Gender_KH', 'Count']
fig_gender = px.pie(
    gender_counts, 
    names='Gender_KH', 
    values='Count',
    hole=0.4,
    title='1. Overall Gender Share (ប្រុស vs ស្រី)',
    color='Gender_KH',
    color_discrete_map={'ប្រុស': '#1f77b4', 'ស្រី': '#e07a5f'}
)
fig_gender.update_traces(textinfo='percent+label', textfont_size=14, textfont_color='black')
fig_gender.update_layout(height=300, margin=dict(t=40, b=20, l=20, r=20))

# Finding 2: Occupation (មុខរបរ)
occ_ct = pd.crosstab(filtered_df['Occupation_KH'], filtered_df['Gender_KH'], margins=True, margins_name='Total')
for col in ['ប្រុស', 'ស្រី']:
    if col not in occ_ct.columns:
        occ_ct[col] = 0
occ_ct = occ_ct[['ប្រុស', 'ស្រី', 'Total']].sort_values(by='Total', ascending=False)

occ_chart_df = filtered_df.groupby(['Occupation_KH', 'Gender_KH']).size().reset_index(name='Count')
top_occs = occ_ct.drop('Total').head(8).index.tolist()
occ_chart_df = occ_chart_df[occ_chart_df['Occupation_KH'].isin(top_occs)]

fig_occ = px.bar(
    occ_chart_df,
    y='Occupation_KH',
    x='Count',
    color='Gender_KH',
    barmode='stack',
    orientation='h',
    title='2. Top Certified Occupations by Gender (មុខរបរ)',
    color_discrete_map={'ប្រុស': '#1f77b4', 'ស្រី': '#e07a5f'}
)
fig_occ.update_layout(yaxis={'categoryorder':'total ascending'}, height=300, yaxis_title='', xaxis_title='Candidate Count')

# Finding 3: Assessment Center (AT)
at_ct = pd.crosstab(filtered_df['AT_KH'], filtered_df['Gender_KH'], margins=True, margins_name='Total')
for col in ['ប្រុស', 'ស្រី']:
    if col not in at_ct.columns:
        at_ct[col] = 0
at_ct = at_ct[['ប្រុស', 'ស្រី', 'Total']].sort_values(by='Total', ascending=False)

at_chart_df = filtered_df.groupby(['AT_KH', 'Gender_KH']).size().reset_index(name='Count')
fig_at = px.bar(
    at_chart_df,
    y='AT_KH',
    x='Count',
    color='Gender_KH',
    barmode='stack',
    orientation='h',
    title='3. Assessment Centers by Gender (មជ្ឈមណ្ឌលវាយតម្លៃសមត្ថភាព)',
    color_discrete_map={'ប្រុស': '#1f77b4', 'ស្រី': '#e07a5f'}
)
fig_at.update_layout(yaxis={'categoryorder':'total ascending'}, height=300, yaxis_title='', xaxis_title='Candidate Count')

# Finding 4: Qualification Level (NQ)
nq_ct = pd.crosstab(filtered_df['NQ_KH'], filtered_df['Gender_KH'], margins=True, margins_name='Total')
for col in ['ប្រុស', 'ស្រី']:
    if col not in nq_ct.columns:
        nq_ct[col] = 0
nq_ct = nq_ct[['ប្រុស', 'ស្រី', 'Total']].sort_values(by='Total', ascending=False)

nq_chart_df = filtered_df.groupby(['NQ_KH', 'Gender_KH']).size().reset_index(name='Count')
fig_nq = px.bar(
    nq_chart_df,
    x='NQ_KH',
    y='Count',
    color='Gender_KH',
    barmode='group',
    title='4. National Qualification Levels by Gender (កម្រិតសញ្ញាបត្រ)',
    color_discrete_map={'ប្រុស': '#1f77b4', 'ស្រី': '#e07a5f'}
)
fig_nq.update_layout(height=300, xaxis_title='', yaxis_title='Candidate Count')

# Finding 5: Sponsor (ដៃគូឧបត្ថម្ភ)
sp_ct = pd.crosstab(filtered_df['Sponsors'], filtered_df['Gender_KH'], margins=True, margins_name='Total')
for col in ['ប្រុស', 'ស្រី']:
    if col not in sp_ct.columns:
        sp_ct[col] = 0
sp_ct = sp_ct[['ប្រុស', 'ស្រី', 'Total']].sort_values(by='Total', ascending=False)

sp_chart_df = filtered_df.groupby(['Sponsors', 'Gender_KH']).size().reset_index(name='Count')
fig_sp = px.bar(
    sp_chart_df,
    x='Sponsors',
    y='Count',
    color='Gender_KH',
    barmode='stack',
    title='5. Sponsorship Distribution by Gender (ដៃគូឧបត្ថម្ភ)',
    color_discrete_map={'ប្រុស': '#1f77b4', 'ស្រី': '#e07a5f'}
)
fig_sp.update_layout(height=300, xaxis_title='', yaxis_title='Candidate Count')

# -----------------------------------------------------------------------------
# DASHBOARD TABS (INCLUDING NEW SUMMARY DASHBOARD TAB)
# -----------------------------------------------------------------------------
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dashboard Overview",
    "1. Gender Distribution", 
    "2. Occupation (មុខរបរ)", 
    "3. Assessment Center (AT)", 
    "4. Qualification Level (NQ)", 
    "5. Sponsor (ដៃគូឧបត្ថម្ភ)"
])

# -----------------------------------------------------------------------------
# TAB 0: DASHBOARD OVERVIEW (ALL 5 GRAPHS)
# -----------------------------------------------------------------------------
with tab0:
    st.subheader("Dashboard Overview - All 5 Analytics Graphs")
    st.markdown("Comprehensive visual overview of all 5 key dataset findings based on active date filters.")
    
    # Row 1: Gender Distribution & Top Occupations
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.plotly_chart(fig_gender, use_container_width=True, key="dash_fig_gender")
    with r1_col2:
        st.plotly_chart(fig_occ, use_container_width=True, key="dash_fig_occ")
        
    # Row 2: Assessment Center & National Qualifications
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.plotly_chart(fig_at, use_container_width=True, key="dash_fig_at")
    with r2_col2:
        st.plotly_chart(fig_nq, use_container_width=True, key="dash_fig_nq")
        
    # Row 3: Sponsors Distribution & Key Highlights Summary
    r3_col1, r3_col2 = st.columns([1.2, 1])
    with r3_col1:
        st.plotly_chart(fig_sp, use_container_width=True, key="dash_fig_sp")
    with r3_col2:
        st.markdown("#### Executive Summary Highlights")
        st.info(f"""
        - **Total Active Candidates:** {total_candidates:,}
        - **Male Ratio:** {male_count:,} ({(male_count/total_candidates*100):.1f}%)
        - **Female Ratio:** {female_count:,} ({female_pct:.1f}%)
        - **Top Occupation:** {occ_ct.index[0] if len(occ_ct) > 1 else 'N/A'}
        - **Top Assessment Center:** {at_ct.index[0] if len(at_ct) > 1 else 'N/A'}
        - **Top Qualification Level:** {nq_ct.index[0] if len(nq_ct) > 1 else 'N/A'}
        - **Top Sponsor:** {sp_ct.index[0] if len(sp_ct) > 1 else 'N/A'}
        """)

# -----------------------------------------------------------------------------
# TAB 1: OVERALL GENDER DISTRIBUTION
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Finding 1: Overall Gender Distribution (បេក្ខជន តាមភេទ)")
    
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.markdown("#### Gender Insights & Summary Table")
        st.dataframe(gender_ct.style.format({'Candidate Count': '{:,.0f}', 'Percentage (%)': '{:.2f}%'}), use_container_width=True)
        
        st.info(f"""
        **Key Findings:**
        - **Total Active Records:** {total_candidates:,}
        - **Male (`ប្រុស`):** {male_count:,} candidates ({(male_count/total_candidates*100):.2f}%)
        - **Female (`ស្រី`):** {female_count:,} candidates ({female_pct:.2f}%)
        """)
        
    with col_right:
        st.markdown("#### Interactive Gender Visualization")
        st.plotly_chart(fig_gender, use_container_width=True, key="tab1_fig_gender")

# -----------------------------------------------------------------------------
# TAB 2: OCCUPATION (មុខរបរ)
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Finding 2: Occupation Breakdown per Gender (មុខរបរ)")
    
    col_left, col_right = st.columns([1.1, 1.3])
    
    with col_left:
        st.markdown("#### Occupation Summary Table (KH)")
        st.dataframe(occ_ct.style.format('{:,.0f}'), use_container_width=True, height=450)
        
    with col_right:
        st.markdown("#### Occupation Visualization per Gender")
        st.plotly_chart(fig_occ, use_container_width=True, key="tab2_fig_occ")

# -----------------------------------------------------------------------------
# TAB 3: ASSESSMENT CENTER (AT)
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Finding 3: Assessment Center Breakdown per Gender (មជ្ឈមណ្ឌលវាយតម្លៃសមត្ថភាព - AT)")
    
    col_left, col_right = st.columns([1.1, 1.3])
    
    with col_left:
        st.markdown("#### Assessment Center Summary Table (KH)")
        st.dataframe(at_ct.style.format('{:,.0f}'), use_container_width=True, height=450)
        
    with col_right:
        st.markdown("#### Assessment Center Visualization per Gender")
        st.plotly_chart(fig_at, use_container_width=True, key="tab3_fig_at")

# -----------------------------------------------------------------------------
# TAB 4: NATIONAL QUALIFICATION (NQ)
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Finding 4: National Qualification Breakdown per Gender (កម្រិតសញ្ញាបត្រ - NQ)")
    
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.markdown("#### Qualification Level Summary Table (KH)")
        st.dataframe(nq_ct.style.format('{:,.0f}'), use_container_width=True)
        
    with col_right:
        st.markdown("#### Qualification Level Visualization per Gender")
        st.plotly_chart(fig_nq, use_container_width=True, key="tab4_fig_nq")

# -----------------------------------------------------------------------------
# TAB 5: SPONSOR (ដៃគូឧបត្ថម្ភ)
# -----------------------------------------------------------------------------
with tab5:
    st.subheader("Finding 5: Sponsor Breakdown per Gender (ដៃគូឧបត្ថម្ភ - Sponsors)")
    
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.markdown("#### Sponsor Summary Table")
        st.dataframe(sp_ct.style.format('{:,.0f}'), use_container_width=True)
        
    with col_right:
        st.markdown("#### Sponsor Visualization per Gender")
        st.plotly_chart(fig_sp, use_container_width=True, key="tab5_fig_sp")

# Footer
st.markdown("---")
st.caption("RPL Dashboard Streamlit Application | Cross-platform | Data source: Date_Committee_Meeting | Created for TGI-DSA")

