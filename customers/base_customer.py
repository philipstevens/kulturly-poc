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
        # --- Global CSS for centered, larger title ---
        st.markdown("""
            <style>
            .centered-title {
            text-align: center;
            font-size: 1.4rem;
            margin-bottom: 0.1rem;  /* reduced space below title */
            }
            /* center all Streamlit buttons */
            .stButton button {
                margin-left: auto;
                margin-right: auto;
                display: block;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

        st.markdown('<div class="centered-title">What Do You Want to Explore?</div>', unsafe_allow_html=True)
        query = st.text_area(
            "",
            height=80,
            placeholder=(self.config["query_placeholder"])
        )

        st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

        # --- Advanced Context Expander ---
        with st.expander("Context Settings", expanded=False):
            internal = st.text_input(
                "Internal Assets (URL or upload)",
                placeholder=self.config["internal_url"],
                help="Optional: include a company domain or local file for context"
            )

            geographies = st.multiselect(
                "Geography",
                ["Global", "Malaysia", "Thailand", "Indonesia", "Japan"],
                default=self.config["default_geographies"],
                help="Restrict to specific regions"
            )
            languages = st.multiselect(
                "Language",
                ["Any", "English", "Bahasa Melayu", "Mandarin", "Tamil"],
                default=["Any"],
                help="Restrict to specific languages"
            )


            objectives = [
                "Understand consumer behavior",
                "Identify emerging trends",
                "Analyze sentiment",
                "Benchmark competition",
                "Assess brand perception"
            ]
            objective = st.selectbox(
                "Primary Objective",
                objectives,
                placeholder=self.config["default_objective"],
                help="Choose your primary research goal. All will be considered, but this will guide the analysis focus."
            )

            segment_options = [
                "Urban Millennials",
                "Gen Z",
                "Working Professionals",
                "New Parents",
                "Health-conscious consumers"
            ]
            segments = st.multiselect(
                "Customer Segments",
                segment_options,
                default=self.config["default_segments"],
                help="Select one or more market segments"
            )

            # Industry selection
            industries = [
                "Consumer Packaged Goods",
                "Technology",
                "Healthcare",
                "Financial Services",
                "Retail",
                "Automotive",
                "Entertainment", 
                "Apparel & Fashion"
            ]
            industry = st.selectbox(
                "Industry",
                industries,
                index=industries.index(self.config["default_industry"]),
                placeholder=self.config["default_industry"],
                help="Choose the industry relevant to your research"
            )

            # Product type selection
            product_types = [
                "Luxury Couture & Designer Apparel",
                "Formalwear & Business Attire",
                "Fast Fashion & Mass Retail",
                "Intimate Apparel & Lingerie",
                "Traditional & Ethnic Wear",
                "Outdoor & Technical Apparel",
                "Footwear",  
                "Athleisure & Activewear",  
                "Streetwear & Urban Fashion",  
                "Children’s & Maternity Clothing",
                "Infant Formula",
                "Probiotic Supplements",
                "Health & Wellness Food",
                "Organic & Natural Products",
                "Sustainable & Eco-friendly Brands"
            ]
            product_type = st.multiselect(
                "Product Type",
                product_types,
                default=self.config["default_product_types"],
                help="Select product categories relevant to your research"
            )


        with st.expander("Source Settings", expanded=False):
            SOURCE_CATEGORIES = [
                "Social: Media Posts",
                "Social: Forums & Communities",
                "Behavioral: Web & Trends",
                "Behavioral: Reviews & Ratings",
                "Behavioral: Surveys & Polls",
                "Research & Reports: Academic Papers & White Papers",
                "Research & Reports: Proprietary Market Reports",
                "Media & News: Articles & Broadcast Transcripts",
                "Media & News: Press Releases & Patents",
                "Cultural Artifacts (Memes, Short Video Clips, Music Charts, Fashion Lookbooks)",
                "Talent Market"
            ]
            select_all = st.checkbox(
                "All Sources",
                key="adv_select_all_sources",
                help="Select every top-level source category"
            )

            if select_all:
                sources = SOURCE_CATEGORIES.copy()
            else:
                sources = st.multiselect(
                    "Sources",
                    SOURCE_CATEGORIES,
                    default=self.config["default_sources"],
                    key="adv_sources_multiselect",
                    help="Pick one or more source categories"
                )

            modalities = st.multiselect(
                "Modalities",
                ["Text", "Image", "Video", "Audio"],
                default=self.config["default_modalities"],
                help="Select content formats to include. Text includes available transcripts for audio/video sources."
            )

            # Enable network/influence analysis
            enable_network = st.checkbox(
                "Enable Network Analysis & Influence Mapping",
                key="adv_enable_network",
                value=self.config["enable_network_analysis"],
                help="Include social graph mapping and influence metrics"
            )


        if st.button("Generate Insights", type="primary"):
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
