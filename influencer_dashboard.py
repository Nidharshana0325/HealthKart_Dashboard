import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import uuid
from datetime import datetime
import io
import base64
import latex

# Set page configuration with custom styling
st.set_page_config(page_title="HealthKart Influencer Dashboard", layout="wide", page_icon="🏋️")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {background-color: #4CAF50; color: white;}
    .stFileUploader>label {color: #333;}
    </style>
""", unsafe_allow_html=True)

# Sample data generation (for simulation)
def generate_sample_data():
    influencers = pd.DataFrame({
        'influencer_id': [str(uuid.uuid4()) for _ in range(10)],
        'name': ['FitWithAmit', 'HealthGuru', 'YogaVibes', 'MuscleMan', 'WellnessQueen', 
                'GymRat', 'FitMom', 'PowerLifter', 'NutritionNerd', 'RunWithRaj'],
        'category': ['Fitness', 'Nutrition', 'Yoga', 'Bodybuilding', 'Wellness',
                    'Fitness', 'Parenting', 'Powerlifting', 'Nutrition', 'Running'],
        'gender': ['M', 'F', 'F', 'M', 'F', 'M', 'F', 'M', 'M', 'M'],
        'follower_count': [100000, 250000, 80000, 150000, 300000, 
                          120000, 90000, 200000, 180000, 110000],
        'platform': ['Instagram', 'YouTube', 'Instagram', 'YouTube', 'Instagram',
                    'Twitter', 'Instagram', 'YouTube', 'Twitter', 'Instagram']
    })
    
    posts = pd.DataFrame({
        'influencer_id': [influencers['influencer_id'].iloc[i%10] for i in range(50)],
        'platform': [influencers['platform'].iloc[i%10] for i in range(50)],
        'date': pd.date_range(start='2025-01-01', periods=50, freq='D'),
        'url': ['https://example.com/post/' + str(i) for i in range(50)],
        'caption': ['Check out MuscleBlaze!' for _ in range(50)],
        'reach': [5000 + i*100 for i in range(50)],
        'likes': [200 + i*10 for i in range(50)],
        'comments': [10 + i*2 for i in range(50)]
    })
    
    tracking_data = pd.DataFrame({
        'source': ['Influencer' for _ in range(100)],
        'campaign': ['Spring2025' for _ in range(100)],
        'influencer_id': [influencers['influencer_id'].iloc[i%10] for i in range(100)],
        'user_id': [str(uuid.uuid4()) for _ in range(100)],
        'product': ['MuscleBlaze']*40 + ['HKVitals']*30 + ['Gritzo']*30,
        'date': pd.date_range(start='2025-01-01', periods=100, freq='H'),
        'orders': [1 for _ in range(100)],
        'revenue': [1000 + i*10 for i in range(100)]
    })
    
    payouts = pd.DataFrame({
        'influencer_id': influencers['influencer_id'],
        'basis': ['post' if i%2==0 else 'order' for i in range(10)],
        'rate': [500 if i%2==0 else 50 for i in range(10)],
        'orders': [10 + i*2 for i in range(10)],
        'total_payout': [5000 + i*100 for i in range(10)]
    })
    
    return influencers, posts, tracking_data, payouts

# Data upload functionality
def load_data(uploaded_file, data_type):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"{data_type} data uploaded successfully!")
            return df
        except Exception as e:
            st.error(f"Error uploading {data_type} data: {str(e)}")
            return None
    return None

# Initialize session state for data
if 'influencers' not in st.session_state:
    st.session_state.influencers, st.session_state.posts, st.session_state.tracking_data, st.session_state.payouts = generate_sample_data()

# Dashboard title
st.title("🏋️ HealthKart Influencer Campaign Dashboard")

# Data upload section
st.sidebar.header("Data Upload")
with st.sidebar.expander("Upload CSV Files"):
    influencers_file = st.file_uploader("Upload Influencers CSV", type=['csv'])
    posts_file = st.file_uploader("Upload Posts CSV", type=['csv'])
    tracking_file = st.file_uploader("Upload Tracking Data CSV", type=['csv'])
    payouts_file = st.file_uploader("Upload Payouts CSV", type=['csv'])

    if st.button("Load Uploaded Data"):
        if influencers_file:
            st.session_state.influencers = load_data(influencers_file, "Influencers")
        if posts_file:
            st.session_state.posts = load_data(posts_file, "Posts")
        if tracking_file:
            st.session_state.tracking_data = load_data(tracking_file, "Tracking")
        if payouts_file:
            st.session_state.payouts = load_data(payouts_file, "Payouts")

# Sidebar filters
st.sidebar.header("Filters")
platform_filter = st.sidebar.multiselect("Platform", options=['Instagram', 'YouTube', 'Twitter'], default=['Instagram', 'YouTube', 'Twitter'])
brand_filter = st.sidebar.multiselect("Brand", options=['MuscleBlaze', 'HKVitals', 'Gritzo'], default=['MuscleBlaze', 'HKVitals', 'Gritzo'])
category_filter = st.sidebar.multiselect("Influencer Category", options=['Fitness', 'Nutrition', 'Yoga', 'Bodybuilding', 'Wellness', 'Parenting', 'Powerlifting', 'Running'], 
                                      default=['Fitness', 'Nutrition', 'Yoga', 'Bodybuilding', 'Wellness', 'Parenting', 'Powerlifting', 'Running'])
date_range = st.sidebar.date_input("Date Range", [datetime(2025, 1, 1), datetime(2025, 7, 26)])

# Filter data
filtered_influencers = st.session_state.influencers[
    (st.session_state.influencers['platform'].isin(platform_filter)) &
    (st.session_state.influencers['category'].isin(category_filter))
]
filtered_posts = st.session_state.posts[
    (st.session_state.posts['influencer_id'].isin(filtered_influencers['influencer_id'])) &
    (st.session_state.posts['date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]
filtered_tracking = st.session_state.tracking_data[
    (st.session_state.tracking_data['influencer_id'].isin(filtered_influencers['influencer_id'])) &
    (st.session_state.tracking_data['product'].isin(brand_filter)) &
    (st.session_state.tracking_data['date'].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]
filtered_payouts = st.session_state.payouts[st.session_state.payouts['influencer_id'].isin(filtered_influencers['influencer_id'])]

# Calculate ROAS and Incremental ROAS
def calculate_roas(tracking, payouts):
    total_revenue = tracking.groupby('influencer_id')['revenue'].sum().reset_index()
    total_payout = payouts.groupby('influencer_id')['total_payout'].sum().reset_index()
    roas_data = pd.merge(total_revenue, total_payout, on='influencer_id', how='left')
    roas_data['roas'] = roas_data['revenue'] / roas_data['total_payout'].replace(0, 1)
    # Assume 10% of revenue is baseline (non-influencer driven)
    roas_data['incremental_revenue'] = roas_data['revenue'] * 0.9
    roas_data['incremental_roas'] = roas_data['incremental_revenue'] / roas_data['total_payout'].replace(0, 1)
    return roas_data

roas_data = calculate_roas(filtered_tracking, filtered_payouts)

# Dashboard layout
st.header("Campaign Overview")
col1, col2 = st.columns([3, 2])

with col1:
    # Campaign Performance
    st.subheader("Performance by Brand")
    performance_fig = px.bar(
        filtered_tracking.groupby('product').agg({'orders': 'sum', 'revenue': 'sum'}).reset_index(),
        x='product', y=['orders', 'revenue'], barmode='group',
        title="Orders and Revenue by Brand",
        color_discrete_map={'orders': '#4CAF50', 'revenue': '#2196F3'}
    )
    st.plotly_chart(performance_fig, use_container_width=True)

    # ROAS and Incremental ROAS
    st.subheader("ROAS Analysis")
    roas_fig = go.Figure(data=[
        go.Bar(name='ROAS', x=roas_data.merge(filtered_influencers[['influencer_id', 'name']], on='influencer_id')['name'], 
               y=roas_data['roas'], marker_color='#4CAF50'),
        go.Bar(name='Incremental ROAS', x=roas_data.merge(filtered_influencers[['influencer_id', 'name']], on='influencer_id')['name'], 
               y=roas_data['incremental_roas'], marker_color='#FF9800')
    ])
    roas_fig.update_layout(barmode='group', title="ROAS and Incremental ROAS by Influencer")
    st.plotly_chart(roas_fig, use_container_width=True)

with col2:
    # Top Influencers
    st.subheader("Top Influencers by Revenue")
    top_influencers = pd.merge(
        filtered_tracking.groupby('influencer_id')['revenue'].sum().reset_index(),
        filtered_influencers[['influencer_id', 'name', 'category']],
        on='influencer_id'
    ).sort_values('revenue', ascending=False).head(5)
    top_fig = px.bar(top_influencers, x='name', y='revenue', color='category', 
                     title="Top 5 Influencers by Revenue", text='revenue')
    top_fig.update_traces(texttemplate='$%{text:,.0f}', textposition='auto')
    st.plotly_chart(top_fig, use_container_width=True)

    # Engagement Trends
    st.subheader("Engagement Trends")
    engagement_trend = filtered_posts.groupby('date').agg({'reach': 'sum', 'likes': 'sum', 'comments': 'sum'}).reset_index()
    trend_fig = px.line(engagement_trend, x='date', y=['reach', 'likes', 'comments'], 
                        title="Engagement Over Time")
    st.plotly_chart(trend_fig, use_container_width=True)

# Payout Tracking
st.header("Payout Tracking")
payout_display = pd.merge(
    filtered_payouts,
    filtered_influencers[['influencer_id', 'name', 'platform']],
    on='influencer_id'
)[['name', 'platform', 'basis', 'rate', 'orders', 'total_payout']]
payout_display['rate'] = payout_display['rate'].apply(lambda x: f"${x:,.2f}")
payout_display['total_payout'] = payout_display['total_payout'].apply(lambda x: f"${x:,.2f}")
st.dataframe(payout_display, use_container_width=True)

# Insights Summary
st.header("Insights Summary")
insights = f"""
- **Top Performing Brand**: {filtered_tracking.groupby('product')['revenue'].sum().idxmax()} with ${filtered_tracking.groupby('product')['revenue'].sum().max():,.2f}
- **Best ROAS**: {roas_data.merge(filtered_influencers[['influencer_id', 'name']], on='influencer_id').iloc[roas_data['roas'].idxmax()]['name']} with ROAS of {roas_data['roas'].max():.2f}x
- **Best Incremental ROAS**: {roas_data.merge(filtered_influencers[['influencer_id', 'name']], on='influencer_id').iloc[roas_data['incremental_roas'].idxmax()]['name']} with Incremental ROAS of {roas_data['incremental_roas'].max():.2f}x
- **Most Engaged Platform**: {filtered_posts.groupby('platform')['likes'].sum().idxmax()} with {filtered_posts.groupby('platform')['likes'].sum().max():,.0f} likes
- **Top Persona**: {top_influencers['category'].iloc[0]} influencers drive the highest revenue
- **Recommendation**: Prioritize {category_filter[0]} influencers on {platform_filter[0]} for optimal engagement and ROAS
"""
st.markdown(insights)

# Export Options
st.header("Export Options")
col_export1, col_export2 = st.columns(2)
with col_export1:
    csv = filtered_tracking.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{b64}" download="campaign_data.csv"><button>Download CSV</button></a>', unsafe_allow_html=True)

with col_export2:
    # Generate LaTeX for PDF export
    latex_content = f"""
\\documentclass{{article}}
\\usepackage{{geometry}}
\\geometry{{a4paper, margin=1in}}
\\usepackage{{booktabs}}
\\usepackage{{pdflscape}}
\\usepackage{{enumitem}}
\\usepackage[utf8]{{inputenc}}
\\begin{{document}}
\\section*{{HealthKart Influencer Campaign Insights}}
\\begin{{itemize}}
    \\item \\textbf{{Top Performing Brand}}: {filtered_tracking.groupby('product')['revenue'].sum().idxmax()} with \\${filtered_tracking.groupby('product')['revenue'].sum().max():,.2f}
    \\item \\textbf{{Best ROAS}}: {roas_data.merge(filtered_influencers[['influencer_id', 'name']], on='influencer_id').iloc[roas_data['roas'].idxmax()]['name']} with ROAS of {roas_data['roas'].max():.2f}x
    \\item \\textbf{{Best Incremental ROAS}}: {roas_data.merge(filtered_influencers[['influencer_id', 'name']], on='influencer_id').iloc[roas_data['incremental_roas'].idxmax()]['name']} with Incremental ROAS of {roas_data['incremental_roas'].max():.2f}x
    \\item \\textbf{{Most Engaged Platform}}: {filtered_posts.groupby('platform')['likes'].sum().idxmax()} with {filtered_posts.groupby('platform')['likes'].sum().max():,.0f} likes
    \\item \\textbf{{Top Persona}}: {top_influencers['category'].iloc[0]} influencers drive the highest revenue
    \\item \\textbf{{Recommendation}}: Prioritize {category_filter[0]} influencers on {platform_filter[0]} for optimal engagement and ROAS
\\end{{itemize}}
\\section*{{Top 5 Influencers by Revenue}}
\\begin{{table}}[h]
    \\centering
    \\begin{{tabular}}{{|l|c|c|}}
        \\hline
        \\textbf{{Name}} & \\textbf{{Category}} & \\textbf{{Revenue}} \\\\
        \\hline
        {''.join([f"{row['name']} & {row['category']} & \\${row['revenue']:,.2f} \\\\ \\hline" for _, row in top_influencers.iterrows()])}
    \\end{{tabular}}
    \\caption{{Top 5 Influencers by Revenue}}
\\end{{table}}
\\end{{document}}
"""
    b64_latex = base64.b64encode(latex_content.encode()).decode()
    st.markdown(f'<a href="data:file/latex;base64,{b64_latex}" download="insights_summary.tex"><button>Download PDF Source (LaTeX)</button></a>', unsafe_allow_html=True)