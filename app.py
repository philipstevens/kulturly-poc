import streamlit as st

st.set_page_config(page_title="Kulturly Prototype", layout="wide")

# Sidebar: User Info and Journey Selection
st.sidebar.title("Welcome, Joe!")
focus_area = st.sidebar.selectbox("What’s your focus area?", [
    "Brand Planning", "Product Innovation", "Managing Risk", "Enter a New Market"
])
goal = st.sidebar.selectbox("What would you like to achieve?", [
    "Increase Brand Awareness", "Mitigate Brand Risk",
    "Assess a New Business Opportunity", "Create a New Product Category"
])
market = st.sidebar.selectbox("What are your focus market(s)?", [
    "Indonesia", "Singapore", "Vietnam", "Thailand", "Global Scan"
])

st.sidebar.markdown("---")
brand_keywords = st.sidebar.text_area("Describe your brand in keywords or phrases", "sporty, fun, fashionable")

# Tabs for each Journey
tab1, tab2, tab3, tab4, tab5 = st.tabs(["PLAN", "CREATE", "WATCHOUT", "REACT", "ALIGN"])

# ---- PLAN Tab ---- #
with tab1:
    st.header("PLAN: Strategy, Competition, Customer")
    st.subheader(f"Market Analysis for {market}")
    st.markdown("""
    - Market Entry/Exit
    - Product Diversification
    - Strategic Partnerships
    - Competitor Benchmarking (Price / Features / Campaigns)
    - Personalization & Emerging Needs
    
    **Magic Card Example**:
    > *"In {market}, working mums are increasingly turning to fitness apps integrated with social features. Consider a co-branded content push with regional health influencers."*
    """)

# ---- CREATE Tab ---- #
with tab2:
    st.header("CREATE: Innovation & New Product Development")
    st.markdown("""
    - Track Emerging Technologies
    - Sense Social Shifts
    - Identify Latent Needs
    - Observe Competitive Products & Feedback
    
    **Magic Card Example**:
    > *"Gen Z in {market} are adopting meatless snacks via micro-influencer trends. Opportunity for functional, snackable wellness foods."*
    """)

# ---- WATCHOUT Tab ---- #
with tab3:
    st.header("WATCHOUT: Risk Assessment & Org Perception")
    st.markdown("""
    - Regulatory Change Tracking
    - Geopolitical Risk
    - Reputation & Sentiment Analysis
    - Employee Perception

    **Magic Card Example**:
    > *"Local backlash in {market} around greenwashing claims linked to wellness brands. Rethink sustainability messaging strategy."*
    """)

# ---- REACT Tab ---- #
with tab4:
    st.header("REACT: Real-Time Response")
    st.markdown("""
    - Spot Short-Lived Trends
    - Respond to Backlash
    - Generate Trend-Based Content
    - Real-Time Event Impact Analysis

    **Magic Card Example**:
    > *"Rising meme traffic around heat waves + parenting. Opportunity for timely product placement: eco-toys, home cooling kits."*
    """)

# ---- ALIGN Tab ---- #
with tab5:
    st.header("ALIGN: Cultural & Social Fit")
    st.markdown("""
    - Translate Global Campaigns
    - Track Local Sentiment on Sustainability
    - Observe Local Influencers
    - Ensure Cultural Fitment of Content

    **Magic Card Example**:
    > *"In {market}, modest fashion collabs with local artists are surging. A regional capsule line could boost both equity and relatability."*
    """)
