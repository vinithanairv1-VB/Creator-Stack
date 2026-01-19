"""
CREATOR STACK - Creator Economy Market Intelligence Dashboard
==============================================================
Track platforms, monetization trends, rising creators, and tools
shaping the creator economy.

To run locally:
  pip install streamlit plotly pandas
  streamlit run creator_stack.py

Author: Vinitha Nair
Date: January 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Creator Stack | Creator Economy Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# DATA
# ============================================

# Platform Data
PLATFORMS = {
    "YouTube": {
        "monthly_active_creators": 50000000,
        "monetized_creators": 2000000,
        "avg_cpm": 4.50,
        "avg_sponsorship_rate": 20000,
        "revenue_share": 55,
        "min_monetization": "1K subs + 4K watch hours",
        "trend": "stable",
        "yoy_creator_growth": 15,
        "top_category": "Entertainment"
    },
    "TikTok": {
        "monthly_active_creators": 80000000,
        "monetized_creators": 5000000,
        "avg_cpm": 0.50,
        "avg_sponsorship_rate": 15000,
        "revenue_share": 50,
        "min_monetization": "10K followers + 100K views",
        "trend": "growing",
        "yoy_creator_growth": 45,
        "top_category": "Entertainment"
    },
    "Instagram": {
        "monthly_active_creators": 60000000,
        "monetized_creators": 3000000,
        "avg_cpm": 1.00,
        "avg_sponsorship_rate": 10000,
        "revenue_share": 55,
        "min_monetization": "10K followers",
        "trend": "stable",
        "yoy_creator_growth": 12,
        "top_category": "Lifestyle"
    },
    "Twitch": {
        "monthly_active_creators": 9000000,
        "monetized_creators": 300000,
        "avg_cpm": 2.50,
        "avg_sponsorship_rate": 8000,
        "revenue_share": 50,
        "min_monetization": "50 followers + 8hrs streamed",
        "trend": "declining",
        "yoy_creator_growth": -5,
        "top_category": "Gaming"
    },
    "Patreon": {
        "monthly_active_creators": 250000,
        "monetized_creators": 250000,
        "avg_cpm": 0,
        "avg_sponsorship_rate": 0,
        "revenue_share": 88,
        "min_monetization": "None",
        "trend": "stable",
        "yoy_creator_growth": 8,
        "top_category": "Podcasts"
    },
    "Substack": {
        "monthly_active_creators": 35000,
        "monetized_creators": 17000,
        "avg_cpm": 0,
        "avg_sponsorship_rate": 5000,
        "revenue_share": 90,
        "min_monetization": "None",
        "trend": "growing",
        "yoy_creator_growth": 35,
        "top_category": "News/Opinion"
    },
    "Spotify (Podcasts)": {
        "monthly_active_creators": 5000000,
        "monetized_creators": 200000,
        "avg_cpm": 18.00,
        "avg_sponsorship_rate": 25000,
        "revenue_share": 50,
        "min_monetization": "Varies by program",
        "trend": "growing",
        "yoy_creator_growth": 25,
        "top_category": "Podcasts"
    },
    "X (Twitter)": {
        "monthly_active_creators": 10000000,
        "monetized_creators": 500000,
        "avg_cpm": 1.50,
        "avg_sponsorship_rate": 5000,
        "revenue_share": 70,
        "min_monetization": "500 followers + Premium",
        "trend": "uncertain",
        "yoy_creator_growth": 20,
        "top_category": "News/Commentary"
    },
}

# Top Creators by Platform (sample data)
TOP_CREATORS = [
    {"name": "MrBeast", "platform": "YouTube", "followers": 340000000, "est_annual_revenue": 85000000, "category": "Entertainment", "trend": "↑"},
    {"name": "Khaby Lame", "platform": "TikTok", "followers": 162000000, "est_annual_revenue": 25000000, "category": "Comedy", "trend": "→"},
    {"name": "Cristiano Ronaldo", "platform": "Instagram", "followers": 650000000, "est_annual_revenue": 120000000, "category": "Sports", "trend": "↑"},
    {"name": "Kai Cenat", "platform": "Twitch", "followers": 15000000, "est_annual_revenue": 12000000, "category": "Gaming", "trend": "↑"},
    {"name": "Joe Rogan", "platform": "Spotify (Podcasts)", "followers": 15000000, "est_annual_revenue": 60000000, "category": "Podcasts", "trend": "→"},
    {"name": "Charli D'Amelio", "platform": "TikTok", "followers": 155000000, "est_annual_revenue": 20000000, "category": "Dance", "trend": "↓"},
    {"name": "Addison Rae", "platform": "TikTok", "followers": 88000000, "est_annual_revenue": 15000000, "category": "Lifestyle", "trend": "→"},
    {"name": "Lenny Rachitsky", "platform": "Substack", "followers": 850000, "est_annual_revenue": 5000000, "category": "Business", "trend": "↑"},
    {"name": "The Chainsmokers", "platform": "Patreon", "followers": 45000, "est_annual_revenue": 2000000, "category": "Music", "trend": "↑"},
    {"name": "PewDiePie", "platform": "YouTube", "followers": 111000000, "est_annual_revenue": 15000000, "category": "Gaming", "trend": "↓"},
]

# Rising Creators - Up and coming talent to watch
RISING_CREATORS = [
    # YouTube Rising
    {"name": "JiDion", "platform": "YouTube", "followers": 9800000, "growth_rate": 145, "category": "Comedy/Pranks", "started": "2021", "why_watch": "Viral prank format, crossed 10M in 18 months", "brand_ready": True},
    {"name": "Lexi Hensler", "platform": "YouTube", "followers": 5200000, "growth_rate": 85, "category": "Lifestyle/Comedy", "started": "2020", "why_watch": "Strong female demo, high engagement rate", "brand_ready": True},
    {"name": "Caleb Hammer", "platform": "YouTube", "followers": 2100000, "growth_rate": 320, "category": "Finance", "started": "2023", "why_watch": "Financial audit format going viral, 3x growth in 6mo", "brand_ready": True},
    {"name": "Jenny Hoyos", "platform": "YouTube", "followers": 4500000, "growth_rate": 250, "category": "Shorts/Challenge", "started": "2022", "why_watch": "Shorts algorithm master, $1 vs $1000 format", "brand_ready": True},
    
    # TikTok Rising
    {"name": "Tobe Nwigwe", "platform": "TikTok", "followers": 3200000, "growth_rate": 180, "category": "Music", "started": "2022", "why_watch": "Unique Afrobeat sound, crossover potential", "brand_ready": True},
    {"name": "Rod", "platform": "TikTok", "followers": 8500000, "growth_rate": 95, "category": "Comedy", "started": "2021", "why_watch": "Relatable humor, high share rate", "brand_ready": True},
    {"name": "Nara Smith", "platform": "TikTok", "followers": 11000000, "growth_rate": 420, "category": "Lifestyle/Cooking", "started": "2023", "why_watch": "ASMR cooking aesthetic, explosive 2024 growth", "brand_ready": True},
    {"name": "Jools Lebron", "platform": "TikTok", "followers": 2800000, "growth_rate": 8500, "category": "Comedy/Beauty", "started": "2024", "why_watch": "'Very demure' viral moment, cultural impact", "brand_ready": False},
    
    # Instagram Rising
    {"name": "Wisdom Kaye", "platform": "Instagram", "followers": 4100000, "growth_rate": 75, "category": "Fashion", "started": "2020", "why_watch": "High fashion + accessibility, IMG signed", "brand_ready": True},
    {"name": "Chris Olsen", "platform": "Instagram", "followers": 3800000, "growth_rate": 110, "category": "Lifestyle/LGBTQ+", "started": "2021", "why_watch": "Authentic storytelling, strong brand partnerships", "brand_ready": True},
    
    # Twitch Rising
    {"name": "Ironmouse", "platform": "Twitch", "followers": 4200000, "growth_rate": 65, "category": "VTuber/Gaming", "started": "2020", "why_watch": "Top English VTuber, subathon records", "brand_ready": True},
    {"name": "Caedrel", "platform": "Twitch", "followers": 1800000, "growth_rate": 140, "category": "Esports/League", "started": "2022", "why_watch": "Ex-pro to top streamer pipeline, sports crossover", "brand_ready": True},
    
    # X (Twitter) Rising
    {"name": "Sahil Bloom", "platform": "X (Twitter)", "followers": 1800000, "growth_rate": 85, "category": "Business/Self-improvement", "started": "2020", "why_watch": "Thread master, newsletter + X combo, $2M+ revenue", "brand_ready": True},
    {"name": "Shaan Puri", "platform": "X (Twitter)", "followers": 620000, "growth_rate": 120, "category": "Business/Startups", "started": "2021", "why_watch": "My First Million pod host, authentic voice", "brand_ready": True},
    {"name": "Nikita Bier", "platform": "X (Twitter)", "followers": 450000, "growth_rate": 200, "category": "Tech/Product", "started": "2022", "why_watch": "Sold 2 apps to Facebook, product insights go viral", "brand_ready": True},
    {"name": "Trung Phan", "platform": "X (Twitter)", "followers": 980000, "growth_rate": 65, "category": "Business/History", "started": "2020", "why_watch": "Visual business storytelling, The Hustle alum", "brand_ready": True},
    {"name": "Alex Hormozi", "platform": "X (Twitter)", "followers": 2400000, "growth_rate": 180, "category": "Business/Entrepreneurship", "started": "2021", "why_watch": "$100M Offers author, cross-platform domination", "brand_ready": True},
    {"name": "Pirate Wires (Mike Solana)", "platform": "X (Twitter)", "followers": 380000, "growth_rate": 95, "category": "Tech/Politics", "started": "2021", "why_watch": "Tech contrarian voice, Founders Fund connection", "brand_ready": False},
    {"name": "Kyla Scanlon", "platform": "X (Twitter)", "followers": 520000, "growth_rate": 150, "category": "Finance/Economics", "started": "2022", "why_watch": "Gen Z economics explainer, vibecession coined", "brand_ready": True},
    {"name": "Dan Go", "platform": "X (Twitter)", "followers": 750000, "growth_rate": 110, "category": "Fitness/Health", "started": "2021", "why_watch": "High-performer fitness coach, strong thread game", "brand_ready": True},
    
    # Substack/Newsletter Rising
    {"name": "Packy McCormick", "platform": "Substack", "followers": 225000, "growth_rate": 55, "category": "Business/Tech", "started": "2020", "why_watch": "Not Boring - top business newsletter, VC connections", "brand_ready": True},
    {"name": "Heather Cox Richardson", "platform": "Substack", "followers": 1400000, "growth_rate": 45, "category": "Politics/History", "started": "2019", "why_watch": "Largest Substack, $5M+ annual revenue", "brand_ready": False},
    {"name": "Casey Newton", "platform": "Substack", "followers": 175000, "growth_rate": 40, "category": "Tech", "started": "2020", "why_watch": "Platformer - must-read for tech industry", "brand_ready": True},
    
    # Podcast Rising
    {"name": "Alex Cooper", "platform": "Spotify (Podcasts)", "followers": 5000000, "growth_rate": 35, "category": "Lifestyle/Interviews", "started": "2018", "why_watch": "Call Her Daddy $60M Spotify deal, expanding empire", "brand_ready": True},
    {"name": "Theo Von", "platform": "Spotify (Podcasts)", "followers": 4200000, "growth_rate": 85, "category": "Comedy", "started": "2016", "why_watch": "This Past Weekend crossover moment, Netflix special", "brand_ready": True},
    
    # Multi-Platform Rising
    {"name": "Alix Earle", "platform": "TikTok", "followers": 7200000, "growth_rate": 380, "category": "Lifestyle/Beauty", "started": "2023", "why_watch": "Fastest growing lifestyle creator 2023-24, authenticity", "brand_ready": True},
    {"name": "Dylan Mulvaney", "platform": "TikTok", "followers": 10800000, "growth_rate": 200, "category": "LGBTQ+/Lifestyle", "started": "2022", "why_watch": "Cultural moment, brand controversy = awareness", "brand_ready": False},
]

# Creator Economy Market Data
MARKET_DATA = {
    "2024_market_size": 250,  # billions
    "2025_projected": 350,
    "2027_projected": 500,
    "cagr": 22.5,
    "total_creators_globally": 300000000,
    "full_time_creators": 4000000,
    "avg_creator_income": 55000,
    "median_creator_income": 15000,
    "brand_deal_market": 35,  # billions
}

# Creator Tools & Startups
CREATOR_TOOLS = [
    {"name": "Patreon", "category": "Membership", "funding": 412, "valuation": 4000, "status": "Established", "use_case": "Subscription/membership monetization"},
    {"name": "Kajabi", "category": "Courses", "funding": 550, "valuation": 2000, "status": "Established", "use_case": "Online courses & digital products"},
    {"name": "Beehiiv", "category": "Newsletter", "funding": 52, "valuation": 300, "status": "Growth", "use_case": "Newsletter platform for creators"},
    {"name": "Stan Store", "category": "Link-in-bio", "funding": 5, "valuation": 50, "status": "Growth", "use_case": "Creator storefronts"},
    {"name": "Riverside", "category": "Recording", "funding": 47, "valuation": 200, "status": "Growth", "use_case": "Podcast/video recording"},
    {"name": "Descript", "category": "Editing", "funding": 100, "valuation": 550, "status": "Growth", "use_case": "AI video/podcast editing"},
    {"name": "Spotter", "category": "Financing", "funding": 500, "valuation": 1700, "status": "Scaling", "use_case": "Creator capital/catalog deals"},
    {"name": "Jellysmack", "category": "Financing", "funding": 265, "valuation": 800, "status": "Restructuring", "use_case": "Creator accelerator (pivoting)"},
    {"name": "Creative Juice", "category": "Financing", "funding": 50, "valuation": 150, "status": "Growth", "use_case": "Creator banking & advances"},
    {"name": "Karat", "category": "Fintech", "funding": 70, "valuation": 300, "status": "Growth", "use_case": "Creator credit cards"},
    {"name": "Passes", "category": "Membership", "funding": 40, "valuation": 200, "status": "Growth", "use_case": "Creator fan platforms"},
    {"name": "Fourthwall", "category": "Merch", "funding": 30, "valuation": 150, "status": "Growth", "use_case": "Creator merch & storefronts"},
]

# Monetization Trends
MONETIZATION_TRENDS = [
    {"method": "Brand Sponsorships", "2023_share": 35, "2025_share": 32, "trend": "Stable but CPMs declining"},
    {"method": "Ad Revenue Share", "2023_share": 30, "2025_share": 25, "trend": "Declining share of income"},
    {"method": "Subscriptions/Memberships", "2023_share": 15, "2025_share": 22, "trend": "Growing - direct fan support"},
    {"method": "Digital Products/Courses", "2023_share": 10, "2025_share": 12, "trend": "Growing - high margins"},
    {"method": "Affiliate Marketing", "2023_share": 5, "2025_share": 5, "trend": "Stable"},
    {"method": "Merch & Physical Products", "2023_share": 5, "2025_share": 4, "trend": "Slight decline"},
]

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.title("🎬 Creator Stack")
    st.caption("Creator Economy Intelligence")
    st.markdown("---")
    
    st.subheader("📊 Market Overview")
    st.metric("2025 Market Size", f"${MARKET_DATA['2025_projected']}B", f"+{MARKET_DATA['cagr']}% CAGR")
    st.metric("Global Creators", f"{MARKET_DATA['total_creators_globally']/1e6:.0f}M", "Active monthly")
    st.metric("Full-Time Creators", f"{MARKET_DATA['full_time_creators']/1e6:.1f}M", "As primary income")
    
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    st.caption("Built by Vinitha Nair")
    st.caption("📧 vinithanair.v1@gmail.com")

# ============================================
# MAIN DASHBOARD
# ============================================

st.title("🎬 Creator Stack")
st.markdown("*Market intelligence for the creator economy*")

# Top metrics row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="2025 Market Size",
        value=f"${MARKET_DATA['2025_projected']}B",
        delta=f"+{int((MARKET_DATA['2025_projected']-MARKET_DATA['2024_market_size'])/MARKET_DATA['2024_market_size']*100)}% YoY"
    )

with col2:
    st.metric(
        label="Brand Deal Market",
        value=f"${MARKET_DATA['brand_deal_market']}B",
        delta="+18% YoY"
    )

with col3:
    st.metric(
        label="Avg Creator Income",
        value=f"${MARKET_DATA['avg_creator_income']:,}",
        delta="Top 10% skew"
    )

with col4:
    st.metric(
        label="Median Income",
        value=f"${MARKET_DATA['median_creator_income']:,}",
        delta="More realistic"
    )

with col5:
    st.metric(
        label="Platforms Tracked",
        value=len(PLATFORMS),
        delta="Major platforms"
    )

st.markdown("---")

# ============================================
# SECTION 1: PLATFORM COMPARISON
# ============================================
st.subheader("📱 Platform Comparison")

col_plat1, col_plat2 = st.columns(2)

with col_plat1:
    # Creator growth by platform
    df_platforms = pd.DataFrame([
        {"Platform": name, **data} for name, data in PLATFORMS.items()
    ])
    
    fig1 = px.bar(
        df_platforms.sort_values('yoy_creator_growth', ascending=True),
        x='yoy_creator_growth',
        y='Platform',
        orientation='h',
        title='Creator Growth Rate by Platform (YoY %)',
        labels={'yoy_creator_growth': 'YoY Growth %'},
        color='yoy_creator_growth',
        color_continuous_scale='RdYlGn'
    )
    fig1.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_plat2:
    # Revenue share comparison
    fig2 = px.bar(
        df_platforms.sort_values('revenue_share', ascending=True),
        x='revenue_share',
        y='Platform',
        orientation='h',
        title='Creator Revenue Share by Platform (%)',
        labels={'revenue_share': 'Revenue Share %'},
        color='revenue_share',
        color_continuous_scale='Greens'
    )
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# Platform details table
st.markdown("**Platform Monetization Details:**")
platform_table = df_platforms[['Platform', 'avg_cpm', 'avg_sponsorship_rate', 'revenue_share', 'min_monetization', 'trend']].copy()
platform_table.columns = ['Platform', 'Avg CPM ($)', 'Avg Sponsorship ($)', 'Rev Share (%)', 'Min Requirements', 'Trend']
st.dataframe(platform_table, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================
# SECTION 2: TOP CREATORS
# ============================================
st.subheader("⭐ Top Creators by Estimated Revenue")

col_creator1, col_creator2 = st.columns([2, 1])

with col_creator1:
    df_creators = pd.DataFrame(TOP_CREATORS)
    df_creators_sorted = df_creators.sort_values('est_annual_revenue', ascending=True)
    
    fig3 = px.bar(
        df_creators_sorted,
        x='est_annual_revenue',
        y='name',
        color='platform',
        orientation='h',
        title='Top Creators by Estimated Annual Revenue',
        labels={'est_annual_revenue': 'Est. Annual Revenue ($)', 'name': ''},
        hover_data=['followers', 'category']
    )
    fig3.update_layout(height=450)
    st.plotly_chart(fig3, use_container_width=True)

with col_creator2:
    st.markdown("**Key Insights:**")
    st.markdown("""
    - 🏆 **MrBeast** dominates YouTube with $85M+
    - 📱 **TikTok creators** monetize less per follower
    - 🎙️ **Podcasters** (Rogan) have premium CPMs
    - 📧 **Newsletter creators** (Lenny) prove text works
    - ⚠️ Some top creators **declining** (↓)
    """)
    
    st.markdown("**Revenue per Follower:**")
    df_creators['rev_per_follower'] = df_creators['est_annual_revenue'] / df_creators['followers']
    top_rpm = df_creators.nlargest(3, 'rev_per_follower')[['name', 'platform', 'rev_per_follower']]
    for _, row in top_rpm.iterrows():
        st.write(f"• {row['name']}: ${row['rev_per_follower']:.2f}/follower")

st.markdown("---")

# ============================================
# SECTION 3: RISING CREATORS (NEW!)
# ============================================
st.subheader("🚀 Rising Creators to Watch")
st.markdown("*Early-stage talent with breakout potential — the valuable intel*")

df_rising = pd.DataFrame(RISING_CREATORS)

# Filters
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    platform_filter = st.multiselect(
        "Filter by Platform",
        options=df_rising['platform'].unique(),
        default=df_rising['platform'].unique()
    )

with filter_col2:
    category_filter = st.multiselect(
        "Filter by Category", 
        options=df_rising['category'].unique(),
        default=df_rising['category'].unique()
    )

with filter_col3:
    brand_ready_filter = st.checkbox("Brand-Ready Only", value=False)

# Apply filters
df_filtered = df_rising[
    (df_rising['platform'].isin(platform_filter)) & 
    (df_rising['category'].isin(category_filter))
]
if brand_ready_filter:
    df_filtered = df_filtered[df_filtered['brand_ready'] == True]

# Rising creators chart
col_rising1, col_rising2 = st.columns([2, 1])

with col_rising1:
    fig_rising = px.scatter(
        df_filtered,
        x='followers',
        y='growth_rate',
        size='followers',
        color='platform',
        hover_name='name',
        hover_data=['category', 'why_watch', 'started'],
        title='Rising Creators: Followers vs Growth Rate',
        labels={'followers': 'Current Followers', 'growth_rate': 'Growth Rate (% YoY)'},
        size_max=50
    )
    fig_rising.update_layout(height=450)
    st.plotly_chart(fig_rising, use_container_width=True)

with col_rising2:
    st.markdown("**🔥 Fastest Growing:**")
    top_growth = df_filtered.nlargest(5, 'growth_rate')[['name', 'platform', 'growth_rate']]
    for _, row in top_growth.iterrows():
        st.write(f"• **{row['name']}** ({row['platform']}): +{row['growth_rate']}%")
    
    st.markdown("---")
    st.markdown("**💡 Why Track Rising Creators?**")
    st.markdown("""
    - Lower partnership costs
    - Higher engagement rates
    - Authentic audience connection
    - First-mover brand advantage
    - Better ROI than mega-influencers
    """)

# Rising creators table
st.markdown("**Full Rising Creators Directory:**")
rising_display = df_filtered[['name', 'platform', 'followers', 'growth_rate', 'category', 'started', 'why_watch', 'brand_ready']].copy()
rising_display.columns = ['Creator', 'Platform', 'Followers', 'Growth %', 'Category', 'Started', 'Why Watch', 'Brand Ready']
rising_display['Followers'] = rising_display['Followers'].apply(lambda x: f"{x/1e6:.1f}M" if x >= 1e6 else f"{x/1e3:.0f}K")
rising_display['Brand Ready'] = rising_display['Brand Ready'].apply(lambda x: "✅" if x else "⚠️")
st.dataframe(rising_display.sort_values('Growth %', ascending=False), use_container_width=True, hide_index=True)

# Breakout alerts
st.markdown("**🚨 Breakout Alerts (Highest Growth Velocity):**")
alert_col1, alert_col2, alert_col3 = st.columns(3)

breakout = df_rising.nlargest(3, 'growth_rate')
for i, (col, (_, creator)) in enumerate(zip([alert_col1, alert_col2, alert_col3], breakout.iterrows())):
    with col:
        st.markdown(f"""
        **{creator['name']}**  
        📱 {creator['platform']} | {creator['category']}  
        👥 {creator['followers']/1e6:.1f}M followers  
        📈 **+{creator['growth_rate']}% growth**  
        💡 {creator['why_watch']}
        """)

st.markdown("---")

# ============================================
# SECTION 4: MONETIZATION TRENDS
# ============================================
st.subheader("💰 Monetization Mix Evolution")

col_mon1, col_mon2 = st.columns(2)

df_monetization = pd.DataFrame(MONETIZATION_TRENDS)

with col_mon1:
    fig4 = px.pie(
        df_monetization,
        values='2023_share',
        names='method',
        title='2023 Revenue Mix',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig4.update_layout(height=350)
    st.plotly_chart(fig4, use_container_width=True)

with col_mon2:
    fig5 = px.pie(
        df_monetization,
        values='2025_share',
        names='method',
        title='2025 Revenue Mix (Projected)',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig5.update_layout(height=350)
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("**Key Shifts:**")
shift_col1, shift_col2, shift_col3 = st.columns(3)
with shift_col1:
    st.markdown("📈 **Growing:**")
    st.markdown("• Subscriptions/Memberships\n• Digital Products\n• Direct fan monetization")
with shift_col2:
    st.markdown("📉 **Declining:**")
    st.markdown("• Ad revenue share\n• Platform dependency\n• Brand deal reliance")
with shift_col3:
    st.markdown("🔮 **Emerging:**")
    st.markdown("• AI-assisted content\n• Micro-communities\n• Tokenized ownership")

st.markdown("---")

# ============================================
# SECTION 5: CREATOR TOOLS LANDSCAPE
# ============================================
st.subheader("🛠️ Creator Tools & Startups")

col_tools1, col_tools2 = st.columns([2, 1])

with col_tools1:
    df_tools = pd.DataFrame(CREATOR_TOOLS)
    
    fig6 = px.scatter(
        df_tools,
        x='funding',
        y='valuation',
        size='valuation',
        color='category',
        hover_name='name',
        hover_data=['status', 'use_case'],
        title='Creator Tools: Funding vs Valuation ($M)',
        labels={'funding': 'Total Funding ($M)', 'valuation': 'Valuation ($M)'},
        size_max=50
    )
    fig6.update_layout(height=400)
    st.plotly_chart(fig6, use_container_width=True)

with col_tools2:
    st.markdown("**Category Breakdown:**")
    category_counts = df_tools.groupby('category').agg({
        'funding': 'sum',
        'name': 'count'
    }).reset_index()
    category_counts.columns = ['Category', 'Total Funding ($M)', 'Companies']
    category_counts = category_counts.sort_values('Total Funding ($M)', ascending=False)
    st.dataframe(category_counts, use_container_width=True, hide_index=True)

# Tools table
st.markdown("**Full Tools Directory:**")
tools_display = df_tools[['name', 'category', 'funding', 'valuation', 'status', 'use_case']].copy()
tools_display.columns = ['Company', 'Category', 'Funding ($M)', 'Valuation ($M)', 'Status', 'Use Case']
st.dataframe(tools_display.sort_values('Valuation ($M)', ascending=False), use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================
# SECTION 6: MARKET OPPORTUNITIES
# ============================================
st.subheader("🎯 Market Opportunities & Gaps")

opp_col1, opp_col2, opp_col3 = st.columns(3)

with opp_col1:
    st.markdown("**🟢 Hot Opportunities:**")
    st.markdown("""
    1. **AI Content Tools**
       - Auto-editing, thumbnail generation
       - Script writing assistants
       - Dubbing/translation
    
    2. **Creator Fintech**
       - Revenue-based financing
       - Tax/accounting tools
       - International payments
    
    3. **B2B Creator Services**
       - Talent management SaaS
       - Brand deal marketplaces
       - Analytics platforms
    """)

with opp_col2:
    st.markdown("**🟡 Emerging Trends:**")
    st.markdown("""
    1. **Short-Form Dominance**
       - Vertical video everywhere
       - Micro-drama explosion
       - Snackable content wins
    
    2. **Owned Audiences**
       - Newsletter resurgence
       - Discord communities
       - Membership platforms
    
    3. **Creator-Led Brands**
       - Product launches
       - Equity deals
       - Media companies
    """)

with opp_col3:
    st.markdown("**🔴 Risk Factors:**")
    st.markdown("""
    1. **Platform Risk**
       - Algorithm changes
       - TikTok ban uncertainty
       - Demonetization waves
    
    2. **Market Saturation**
       - 300M+ creators globally
       - Attention competition
       - CPM compression
    
    3. **Creator Burnout**
       - Unsustainable pace
       - Mental health crisis
       - High churn rates
    """)

st.markdown("---")

# ============================================
# SECTION 7: STRATEGIC RECOMMENDATIONS
# ============================================
st.subheader("✅ Strategic Recommendations")

rec_col1, rec_col2 = st.columns(2)

with rec_col1:
    st.markdown("**For Creators:**")
    st.markdown("""
    1. 📧 **Build owned channels** — Email list > follower count
    2. 💰 **Diversify revenue** — Don't rely on one platform
    3. 🎯 **Niche down** — Specific > broad audiences
    4. 📦 **Productize expertise** — Courses, templates, tools
    5. 🤝 **Build community** — Engaged > large audiences
    """)

with rec_col2:
    st.markdown("**For Brands/Platforms:**")
    st.markdown("""
    1. 🎬 **Invest in mid-tier creators** — Better ROI than mega-influencers
    2. 📊 **Track engagement, not followers** — Quality > quantity
    3. 🔄 **Long-term partnerships** — Authenticity matters
    4. 📱 **Go vertical-first** — Short-form is the language
    5. 🛠️ **Enable creators** — Tools > restrictions
    """)

st.markdown("---")

# ============================================
# SECTION 8: MARKET PROJECTIONS
# ============================================
st.subheader("📈 Market Growth Projections")

projection_years = ['2023', '2024', '2025', '2026', '2027']
projection_values = [200, 250, 350, 420, 500]

fig7 = go.Figure()
fig7.add_trace(go.Scatter(
    x=projection_years,
    y=projection_values,
    mode='lines+markers+text',
    text=[f'${v}B' for v in projection_values],
    textposition='top center',
    line=dict(color='#00D4AA', width=3),
    marker=dict(size=12)
))
fig7.update_layout(
    title='Creator Economy Market Size Projection',
    xaxis_title='Year',
    yaxis_title='Market Size ($B)',
    height=350,
    showlegend=False
)
st.plotly_chart(fig7, use_container_width=True)

# Footer
st.markdown("---")
st.caption("""
📊 **Data Sources:** Company reports, Influencer Marketing Hub, SignalFire Creator Economy Report, Goldman Sachs Research, CB Insights
🔄 **Update Frequency:** Monthly market data, Weekly platform changes
📧 **Contact:** vinithanair.v1@gmail.com
""")

# Expandable raw data
with st.expander("📋 View Raw Data"):
    tab1, tab2, tab3, tab4 = st.tabs(["Platforms", "Top Creators", "Rising Creators", "Tools"])
    
    with tab1:
        st.dataframe(df_platforms, use_container_width=True)
    with tab2:
        st.dataframe(df_creators, use_container_width=True)
    with tab3:
        st.dataframe(df_rising, use_container_width=True)
    with tab4:
        st.dataframe(df_tools, use_container_width=True)
    
    # Download buttons
    st.download_button(
        label="Download Platform Data (CSV)",
        data=df_platforms.to_csv(index=False),
        file_name=f"creator_stack_platforms_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    st.download_button(
        label="Download Rising Creators (CSV)",
        data=df_rising.to_csv(index=False),
        file_name=f"creator_stack_rising_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    st.download_button(
        label="Download Tools Data (CSV)",
        data=df_tools.to_csv(index=False),
        file_name=f"creator_stack_tools_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
