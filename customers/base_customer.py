# customers/base_customer.py

import streamlit as st
import time

default_config = {
            "query_placeholder": "What do you want to explore?",
            "internal_url": "https://example.com/internal-assets",
            "default_geographies": ["Global"],
            "default_objective": "Understand consumer behavior",
            "default_segments": ["Urban Millennials"],
            "default_industry": "Consumer Packaged Goods",
            "default_product_types": ["Luxury Couture & Designer Apparel"],
            "default_sources": ["Social: Media Posts", "Behavioral: Web & Trends"],
            "default_modalities": ["Text", "Image"],
            "enable_network_analysis": True
        }

class BaseCustomerRenderer:
    def __init__(self, name="Generic Customer", config=default_config):
        self.name = name
        self.config = config

    def render_context(self):
        # --- Global CSS for space-building interface ---
        st.markdown("""
            <style>
            .space-title {
            text-align: center;
            font-size: 1.6rem;
            margin-bottom: 0.5rem;
            color: #1f1f1f;
            }
            .space-subtitle {
            text-align: center;
            font-size: 1rem;
            margin-bottom: 1.5rem;
            color: #666;
            }
            .section-header {
            font-size: 1.1rem;
            font-weight: 600;
            margin: 1.5rem 0 0.5rem 0;
            color: #333;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 0.3rem;
            }
            .stButton button {
                margin-left: auto;
                margin-right: auto;
                display: block;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

        st.markdown('<div class="space-title">Build Your Cultural Observatory</div>', unsafe_allow_html=True)
        st.markdown('<div class="space-subtitle">Define your cultural space before exploring insights</div>', unsafe_allow_html=True)

        # Space Name
        space_name = st.text_input(
            "Space Name",
            placeholder="e.g., 'SEA Sports x Lifestyle x Fashion' or 'Malaysian Parenting x Health x Trust'",
            help="Give your cultural observatory a memorable name"
        )

        st.markdown('<div class="section-header">Cultural Space</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Primary Cultural Domains
            cultural_domains = st.multiselect(
                "Primary Cultural Domains",
                [
                    "Sports & Athletics", "Fashion & Style", "Lifestyle & Wellness", 
                    "Technology & Innovation", "Entertainment & Media", "Food & Cuisine",
                    "Art & Design", "Music & Audio", "Gaming & Esports", "Beauty & Personal Care",
                    "Parenting & Family", "Health & Fitness", "Travel & Adventure", 
                    "Education & Learning", "Sustainability & Environment", "Finance & Wealth",
                    "Spirituality & Religion", "Politics & Social Issues", "Work & Career"
                ],
                default=self.config.get("default_cultural_domains", ["Sports & Athletics"]),
                help="Select 2-4 primary cultural areas that define your space"
            )

        with col2:
            # Cultural Modifiers
            cultural_modifiers = st.multiselect(
                "Cultural Modifiers",
                [
                    "Luxury", "Premium", "Affordable", "Sustainable", "Traditional", "Modern",
                    "Local", "Global", "Underground", "Mainstream", "Emerging", "Established",
                    "Youth", "Adult", "Senior", "Male", "Female", "Non-binary", "Urban", "Rural"
                ],
                help="Add modifiers to refine your cultural space"
            )

        st.markdown('<div class="section-header">Geographic & Demographic Space</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            geographies = st.multiselect(
                "Geographies",
                [
                    "Global", "Southeast Asia", "East Asia", "South Asia", "North America", 
                    "Europe", "Latin America", "Africa", "Middle East", "Oceania",
                    "Malaysia", "Singapore", "Thailand", "Indonesia", "Philippines", 
                    "Vietnam", "Japan", "South Korea", "China", "India", "Australia"
                ],
                default=self.config.get("default_geographies", ["Global"]),
                help="Select geographic markets to focus on"
            )

        with col2:
            languages = st.multiselect(
                "Languages",
                [
                    "Any", "English", "Mandarin", "Bahasa Melayu", "Bahasa Indonesia", 
                    "Thai", "Vietnamese", "Tagalog", "Japanese", "Korean", "Hindi", 
                    "Tamil", "Arabic", "Spanish", "French", "German"
                ],
                default=["Any"],
                help="Language preferences for cultural signals"
            )

        with col3:
            age_groups = st.multiselect(
                "Age Groups",
                [
                    "Gen Alpha (2010+)", "Gen Z (1997-2012)", "Millennials (1981-1996)", 
                    "Gen X (1965-1980)", "Boomers (1946-1964)", "All Ages"
                ],
                default=["Gen Z (1997-2012)", "Millennials (1981-1996)"],
                help="Target age demographics"
            )

        st.markdown('<div class="section-header">Source Materials & Resources</div>', unsafe_allow_html=True)
        
        # Resource Input Tabs
        resource_tabs = st.tabs(["Websites & URLs", "Social Handles", "Documents & Reports", "Keywords & Tags"])
        
        with resource_tabs[0]:
            st.text_area(
                "Websites & URLs",
                height=100,
                placeholder="https://example.com/brand-page\nhttps://competitor.com\nhttps://industry-report.com",
                help="Add websites, brand pages, competitor sites, industry resources (one per line)"
            )
            
        with resource_tabs[1]:
            col1, col2 = st.columns(2)
            with col1:
                st.text_area(
                    "Social Media Handles",
                    height=80,
                    placeholder="@brand_handle\n@competitor\n@influencer",
                    help="Social media accounts to monitor (one per line)"
                )
            with col2:
                social_platforms = st.multiselect(
                    "Platforms to Monitor",
                    ["Instagram", "TikTok", "Twitter/X", "LinkedIn", "YouTube", "Facebook", "Reddit", "Discord"],
                    default=["Instagram", "TikTok"]
                )
        
        with resource_tabs[2]:
            uploaded_files = st.file_uploader(
                "Upload Documents",
                accept_multiple_files=True,
                type=['pdf', 'docx', 'txt', 'csv'],
                help="Market reports, brand guidelines, research documents"
            )
            
            st.text_area(
                "External Report URLs",
                height=68,
                placeholder="https://research-firm.com/report.pdf",
                help="Links to external research and reports"
            )
            
        with resource_tabs[3]:
            col1, col2 = st.columns(2)
            with col1:
                st.text_area(
                    "Brand Keywords",
                    height=80,
                    placeholder="brand name\nproduct line\ncompetitor names\ncampaign hashtags",
                    help="Brand-specific terms to track (one per line)"
                )
            with col2:
                st.text_area(
                    "Cultural Keywords",
                    height=80,
                    placeholder="streetwear\nsustainable fashion\nK-beauty\nwellness trends",
                    help="Cultural terms and trends to monitor (one per line)"
                )

        st.markdown('<div class="section-header">Analysis Settings</div>', unsafe_allow_html=True)
        
        with st.expander("Advanced Settings", expanded=False):
            # Analysis objectives
            objectives = st.multiselect(
                "Analysis Objectives",
                [
                    "Understand consumer behavior",
                    "Identify emerging trends", 
                    "Analyze cultural sentiment",
                    "Benchmark competition",
                    "Assess brand perception",
                    "Find partnership opportunities",
                    "Discover unaddressed needs",
                    "Map influence networks",
                    "Predict cultural shifts"
                ],
                default=["Identify emerging trends", "Understand consumer behavior"],
                help="Select multiple objectives for comprehensive analysis"
            )

            # Industry context
            industries = st.multiselect(
                "Industry Context",
                [
                    "Apparel & Fashion", "Consumer Packaged Goods", "Technology", "Healthcare",
                    "Financial Services", "Retail & E-commerce", "Automotive", "Entertainment & Media", 
                    "Food & Beverage", "Beauty & Personal Care", "Sports & Fitness", "Travel & Hospitality",
                    "Education", "Real Estate", "Energy & Environment"
                ],
                default=[self.config.get("default_industry", "Consumer Packaged Goods")],
                help="Industry context helps refine cultural analysis"
            )

            # Time horizon
            time_horizon = st.selectbox(
                "Analysis Time Horizon",
                ["Real-time (last 30 days)", "Recent trends (last 6 months)", "Emerging patterns (last 2 years)", "Historical context (5+ years)"],
                index=1,
                help="How far back to analyze cultural signals"
            )

        # Source configuration
        st.markdown('<div class="section-header">Data Sources</div>', unsafe_allow_html=True)
        
        source_tabs = st.tabs(["Content Types", "Platform Sources", "Research Sources"])
        
        with source_tabs[0]:
            modalities = st.multiselect(
                "Content Modalities",
                ["Text", "Images", "Videos", "Audio", "Live Streams", "Stories", "Memes", "Infographics"],
                default=["Text", "Images", "Videos"],
                help="Types of content to analyze"
            )
            
        with source_tabs[1]:
            platform_sources = st.multiselect(
                "Platform Sources", 
                [
                    "Instagram", "TikTok", "Twitter/X", "LinkedIn", "YouTube", "Facebook",
                    "Reddit", "Discord", "Telegram", "WhatsApp", "Clubhouse", "Twitch",
                    "Pinterest", "Snapchat", "BeReal", "Threads"
                ],
                default=["Instagram", "TikTok", "Twitter/X"],
                help="Social platforms to monitor"
            )
            
        with source_tabs[2]:
            research_sources = st.multiselect(
                "Research & Media Sources",
                [
                    "Academic Papers", "Market Research Reports", "Industry White Papers",
                    "News Articles", "Press Releases", "Patent Filings", "Government Data",
                    "Survey Data", "Review Platforms", "Forums & Communities", "Podcasts",
                    "Cultural Artifacts", "Fashion Lookbooks", "Music Charts", "Trend Reports"
                ],
                default=["Market Research Reports", "News Articles", "Review Platforms"],
                help="Research and media sources to include"
            )

        # Analysis capabilities
        st.markdown('<div class="section-header">Analysis Capabilities</div>', unsafe_allow_html=True)
        
        capabilities_col1, capabilities_col2 = st.columns(2)
        
        with capabilities_col1:
            enable_network = st.checkbox(
                "Network Analysis & Influence Mapping",
                value=True,
                help="Map cultural influencers and information flow"
            )
            
            enable_sentiment = st.checkbox(
                "Cultural Sentiment Analysis", 
                value=True,
                help="Analyze emotional tone and cultural reception"
            )
            
        with capabilities_col2:
            enable_prediction = st.checkbox(
                "Trend Prediction & Forecasting",
                value=True, 
                help="Predict future cultural movements"
            )
            
            enable_gaps = st.checkbox(
                "Opportunity Gap Detection",
                value=True,
                help="Identify unaddressed cultural needs"
            )

        st.markdown("---")
        
        if st.button("Build Cultural Space", type="primary", use_container_width=True):
            steps = [
                "Initializing...",
                "Retrieving relevant sources…",
                "Applying cultural lens...",
                "Finding hidden patterns...",
                "Generating insights...",
                "Finalizing...",
            ]
            progress = st.progress(0)
            status = st.empty()

            for i, msg in enumerate(steps):
                status.text(msg)
                # advance progress bar incrementally
                progress.progress((i + 1) / len(steps))
                if i in [0, 2, 5]:
                    time.sleep(1) 
                else: 
                    time.sleep(3)

            # clean up
            progress.empty()
            status.empty()

            st.session_state.configured = True
            st.success("✅ Insights Generated! Other tabs are now unlocked.")

    def render_stories(self):
        pass

    def render_people(self):
        pass

    def render_influencers(self):
        pass

    def render_trends(self):
        pass

    def render_ideas(self):
        pass
