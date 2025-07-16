import streamlit as st
import datetime
import time  

# ― Page layout ―
st.set_page_config(layout="wide")

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

# ― State initialization ―
if "configured" not in st.session_state:
    st.session_state.configured = False

# ― Tabs ―
tabs = st.tabs([
    "Context",
    "Narratives & Topics",
    "Personas & Cohorts",
    "Networks & Influence",
    "Trends & Events"
])

# ― Tab 1: Data Configuration ―
with tabs[0]:
    # Main search box
    st.markdown('<div class="centered-title">What Do You Want to Explore?</div>', unsafe_allow_html=True)
    query = st.text_area(
        "",
        height=80,
        placeholder=(
            "Describe the market, segment, and key question you’re exploring…"
        )
    )

    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

    # --- Advanced Context Expander ---
    with st.expander("Context Settings", expanded=False):
        internal = st.text_input(
            "Internal Assets (URL or upload)",
            help="Optional: include a company domain or local file for context"
        )

        geographies = st.multiselect(
            "Target Geography",
            ["Global", "Malaysia", "Thailand", "Japan"],
            default=["Global"],
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
            "Objective",
            objectives,
            help="Choose your primary research goal"
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
            "Entertainment"
        ]
        industry = st.selectbox(
            "Industry",
            industries,
            help="Choose the industry relevant to your research"
        )

        # Product type selection
        product_types = [
            "Food & Beverage",
            "Personal Care",
            "Home Goods",
            "Electronics",
            "Apparel & Fashion",
            "Software & Apps"
        ]
        product_type = st.multiselect(
            "Product Type",
            product_types,
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
                default=[
                    "Social: Media Posts",
                    "Social: Forums & Communities",
                    "Behavioral: Web & Trends"
                ],
                key="adv_sources_multiselect",
                help="Pick one or more source categories"
            )

        modalities = st.multiselect(
            "Modalities",
            ["Text", "Image", "Video", "Audio"],
            default=["Text"],
            help="Select content formats to include"
        )

        # Enable network/influence analysis
        enable_network = st.checkbox(
            "Enable Network Analysis & Influence Mapping",
            key="adv_enable_network",
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

# ― Tab 2: Narrative Themes ―
with tabs[1]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        themes = [
            {
                "theme": "Breastfeeding Tradition vs Formula Modernity",
                "definition": "Conflict between natural nursing practices and packaged formula adoption",
                "subthemes": [
                    "Maternal Bonding ↔ Convenience",
                    "Natural Immunity ↔ Fortified Nutrition",
                    "Cultural Pride ↔ Global Standards"
                ],
                "codes": [
                    "nenek’s breastmilk lore",
                    "formula label nutrient claims",
                    "nursing support group advice"
                ],
                "example_quotes": [
                    "\"I wanted to nurse as my mother did, but my schedule made formula easier.\"",
                    "\"This formula has DHA and probiotics—my doctor recommended it over exclusive breastfeeding.\""
                ],
                "implications": "Frame messaging to honor nursing heritage while highlighting formula’s science-backed benefits"
            },
            {
                "theme": "Convenience & Control vs Natural Bonding",
                "definition": "Balancing ease of formula feeding with the emotional closeness of breastfeeding",
                "subthemes": [
                    "Time‑saving feeds",
                    "Shared caregiving",
                    "Skin‑to‑skin attachment"
                ],
                "codes": [
                    "bottle‑warming gadgets",
                    "expressed milk storage tips",
                    "kangaroo care practices"
                ],
                "example_quotes": [
                    "\"Using formula lets my partner feed baby at night so I can rest.\"",
                    "\"I miss the closeness of nursing when I pump instead.\""
                ],
                "implications": "Develop content that shows formula as a tool for shared bonding, not a replacement for closeness"
            },
            {
                "theme": "Brand Trust vs Health Authority",
                "definition": "Weighing marketing claims against pediatrician and public health guidelines",
                "subthemes": [
                    "Label Transparency",
                    "Doctor Endorsements",
                    "Government Recommendations"
                ],
                "codes": [
                    "KKM breastmilk promotion posters",
                    "clinic formula samples",
                    "online review comparisons"
                ],
                "example_quotes": [
                    "\"The clinic gives free formula samples, but I read reviews saying it’s too sweet.\"",
                    "\"KKM still recommends exclusive breastfeeding for six months, yet brands tout early weaning formulas.\""
                ],
                "implications": "Craft communications that align brand science claims with official health guidance to build credibility"
            }
        ]

        cols = st.columns(len(themes))
        for col, t in zip(cols, themes):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### {t['theme']}")
                st.markdown(f"*{t['definition']}*")
                st.markdown("**Subthemes:**")
                for stheme in t["subthemes"]:
                    st.markdown(f"- {stheme}")
                st.markdown("**Key Codes:**")
                for code in t["codes"]:
                    st.markdown(f"- {code}")
                st.markdown("**Example Quotes:**")
                for q in t["example_quotes"]:
                    st.markdown(f"> {q}")
                st.markdown("**Implications:**")
                st.markdown(f"- {t['implications']}")
                st.markdown('</div>', unsafe_allow_html=True)

# ― Tab 3: Persona Snapshots ―
with tabs[2]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        persona_data = [
            {
                "name": "Scientific Modern Mom",
                "traits": ["Data‑driven", "Expert trust", "Analytical"],
                "motivations": ["Optimal child health", "Scientific validation"],
                "media": ["@health_blog", "ScienceDaily"]
            },
            {
                "name": "Traditional Herbalist",
                "traits": ["Holistic", "Cultural roots", "Natural remedies"],
                "motivations": ["Ancestral wisdom", "Organic living"],
                "media": ["HerbWorld", "NativePlantsMag"]
            },
            {
                "name": "Anxious First‑Timer",
                "traits": ["Safety‑first", "Over‑researcher", "Risk‑averse"],
                "motivations": ["Peace of mind", "Community reassurance"],
                "media": ["BabyStepsForum", "ParentingNow"]
            }
        ]

        cols = st.columns(len(persona_data))
        for col, persona in zip(cols, persona_data):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### {persona['name']}")
                st.markdown("**Traits:**")
                for trait in persona["traits"]:
                    st.markdown(f"- {trait}")
                st.markdown("**Motivations:**")
                for motive in persona["motivations"]:
                    st.markdown(f"- {motive}")
                st.markdown("**Media Anchors:**")
                for anchor in persona["media"]:
                    st.markdown(f"- {anchor}")
                st.markdown('</div>', unsafe_allow_html=True)
                
# ― Tab 4: Networks & Influence ―
with tabs[3]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        influence_data = [
            {
                "name": "Dr. Sarah Lim",
                "role": "Pediatrician & Parenting Author",
                "influence": "Trusted source for infant nutrition advice",
                "reach": "200K followers on Instagram",
                "impact": "Endorses specific formula brands"
            },
            {
                "name": "MamaMia Community",
                "role": "Parenting Forum & Support Group",
                "influence": "Platform for shared experiences and recommendations",
                "reach": "50K active members",
                "impact": "High engagement on formula discussions"
            },
            {
                "name": "Healthy Baby Blog",
                "role": "Nutrition & Wellness Influencer",
                "influence": "Focuses on science-backed parenting tips",
                "reach": "150K followers across platforms",
                "impact": "Promotes clean-label formulas"
            }
        ]

        cols = st.columns(len(influence_data))
        for col, influencer in zip(cols, influence_data):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### {influencer['name']}")
                st.markdown(f"*{influencer['role']}*")
                st.markdown("**Influence:**")
                st.markdown(f"- {influencer['influence']}")
                st.markdown("**Reach:**")
                st.markdown(f"- {influencer['reach']}")
                st.markdown("**Impact:**")
                st.markdown(f"- {influencer['impact']}")
                st.markdown('</div>', unsafe_allow_html=True)

# ― Tab 5: Trends & Events ―
with tabs[4]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        trend_data = [
            {
                "name": "Probiotic‑Enriched Formulas",
                "description": "Growing interest in gut health support for infants",
                "metrics": [
                    "+25% search volume MoM",
                    "+30% social mentions",
                    "Top hashtag: #BabyGutHealth"
                ],
                "forecast": "Continued growth as parents prioritize immunity and digestion."
            },
            {
                "name": "Clean‑Label & Digestibility",
                "description": "Demand for formulas with minimal, recognizable ingredients",
                "metrics": [
                    "+18% mentions in parenting forums",
                    "High engagement on clean‑label posts",
                    "Rising requests for transparency"
                ],
                "forecast": "Brands that highlight simple ingredient lists will capture market share."
            },
            {
                "name": "Hybrid Feeding Practices",
                "description": "Combining breastfeeding with supplemental formula feeding",
                "metrics": [
                    "+22% forum discussions",
                    "Increasing pediatrician articles endorsing flexibility",
                    "Surge in ‘combo‑feeding’ online queries"
                ],
                "forecast": "Hybrid models to become standard recommendation for busy urban parents."
            }
        ]

        cols = st.columns(len(trend_data))
        for col, trend in zip(cols, trend_data):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### {trend['name']}")
                st.markdown(f"*{trend['description']}*")
                st.markdown("**Key Metrics:**")
                for m in trend["metrics"]:
                    st.markdown(f"- {m}")
                st.markdown("**Forecast:**")
                st.markdown(f"- {trend['forecast']}")
                st.markdown('</div>', unsafe_allow_html=True)

















#     # --- Module 2: Thematic Analysis — Narrative Themes ---
#     st.subheader("Narrative Themes")



#     # --- Module 3: Emerging Trends & Forecasts ---
#     st.subheader("Emerging Trends & Forecasts")


