import json
import os
from pathlib import Path
import time

from dotenv import load_dotenv
import streamlit as st

from insights_renderer import InsightsRenderer

load_dotenv()

is_dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"

if "global_configured" not in st.session_state:
    st.session_state.global_configured = False
if "studies" not in st.session_state:
    st.session_state.studies = []
if "selected_study" not in st.session_state:
    st.session_state.selected_study = None

st.set_page_config(layout="wide")

@st.cache_data
def load_all_insights(data_dir="data"):
    brands = {}
    for brand_dir in Path(data_dir).iterdir():
        if not brand_dir.is_dir():
            continue
        key = brand_dir.name.lower() 
        brands.setdefault(key, {})
        for file in brand_dir.glob("*.json"):
            brands[key][file.stem] = json.loads(file.read_text())
    return brands

all_data = load_all_insights()

# 1. Landing page
if not st.session_state.global_configured:  
    if is_dev_mode:
        default_brand = next(iter(all_data))
        st.session_state.brand_config = {"brand_name": default_brand}
        st.session_state.selected_study = next(iter(all_data[default_brand]))
        st.session_state.studies = [] 
        st.session_state.global_configured = True
    else:
        st.markdown("""
            <style>
            .space-title {
            text-align: center;
            font-size: 1.6rem;
            margin-bottom: 0.5rem;
            }
            .space-subtitle {
            text-align: center;
            font-size: 1rem;
            margin-bottom: 1.5rem;
            opacity: 0.8;
            }
            .section-header {
            font-size: 1.1rem;
            font-weight: 600;
            margin: 1.5rem 0 0.5rem 0;
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

        st.markdown('<div class="space-title">Build Your Cultural Space</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="space-subtitle">Define your brand\'s default cultural space before exploring insights.</div>',
            unsafe_allow_html=True
        )

        display_brands = [""] + [b.title() for b in all_data.keys()]
        choice = st.selectbox("Space Name", display_brands)
        brand_key = choice.lower()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Primary Cultural Domains
            cultural_domains = st.multiselect(
                "Primary Industry",
                [
                    "Sports & Athletics", "Fashion & Style", "Lifestyle & Wellness", 
                    "Technology & Innovation", "Entertainment & Media", "Food & Cuisine",
                    "Art & Design", "Music & Audio", "Gaming & Esports", "Beauty & Personal Care",
                    "Parenting & Family", "Health & Fitness", "Travel & Adventure", 
                    "Education & Learning", "Sustainability & Environment", "Finance & Wealth",
                    "Spirituality & Religion", "Politics & Social Issues", "Work & Career"
                ],
                help="Select 2-4 primary industries",
            )

        with col2:
            # Cultural Modifiers
            cultural_modifiers = st.multiselect(
                "Brand Modifiers",
                [
                    "Adult", "Affordable", "Emerging", "Established", "Female", "Global", 
                    "Local", "Luxury", "Male", "Mainstream", "Modern", "Non-binary", "Premium", 
                    "Romance", "Rural", "Senior", "Social", "Sustainable", "Traditional", 
                    "Underground", "Urban", "Youth"
                ],
                help="Add modifiers to refine your brand space"
            )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            geographies = st.multiselect(
                "Default Geographies",
                [
                    "Global", "Africa", "Australia", "Brazil", "China", "East Asia", "Europe", 
                    "India", "Indonesia", "Japan", "Latin America", "Malaysia", "Middle East", 
                    "North America", "Oceania", "Philippines", "Singapore", "South Asia", 
                    "South Korea", "Southeast Asia", "Thailand", "Vietnam"
                ],
                default=["Global"],
                help="Select geographic markets to focus on"
            )

        with col2:
            languages = st.multiselect(
                "Default Languages",
                [
                    "Any", "Arabic", "Bahasa Indonesia", "Bahasa Melayu", "English", "French", 
                    "German", "Hindi", "Japanese", "Korean", "Mandarin", "Spanish", 
                    "Tagalog", "Tamil", "Thai", "Vietnamese"
                ],
                default=["Any"],
                help="Language preferences for cultural signals"
            )

        with col3:
            age_groups = st.multiselect(
                "Defualt Age Groups",
                [
                    "Gen Alpha (2010+)", "Gen Z (1997-2012)", "Millennials (1981-1996)", 
                    "Gen X (1965-1980)", "Boomers (1946-1964)", "All Ages"
                ],
                default=["All Ages"],
                help="Target age demographics"
            )

        st.markdown('<div class="section-header">References</div>', unsafe_allow_html=True)
        
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
            st.text_area(
                "Social Media Handles",
                height=80,
                placeholder="@brand_handle\n@competitor\n@influencer",
                help="List social media accounts that reflect the tone or community of this space. One per line. These will be used for alignment only, not for tracking or monitoring."
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
                    help="Cultural terms and trends to monitor (one per line)"
                )

        build_disabled = (choice == "")

        # show the button, but greyed out until they pick a brand
        build_clicked = st.button(
            "Build Cultural Space",
            type="primary",
            use_container_width=True,
            disabled=build_disabled,
            help="Enter a brand to continue" if build_disabled else None
        )

        if not choice:
            st.stop()

        st.session_state.brand_config = {
            "brand_name": brand_key,
            "cultural_domains": cultural_domains,
            "cultural_modifiers": cultural_modifiers,
            "default_geographies": geographies,
            "default_languages": languages,
            "default_segments": age_groups,
            "websites": st.session_state.get("websites", []),
            "social_handles": st.session_state.get("social_handles", []),
            "uploaded_files": [f.name for f in uploaded_files] if uploaded_files else [],
            "brand_keywords": st.session_state.get("brand_keywords", ""),
            "cultural_keywords": st.session_state.get("cultural_keywords", "")
        }

        if build_clicked:
            if not is_dev_mode:
                steps = [
                    ("🔧", "Initializing observatory environment..."),
                    ("🔗", "Linking relevant data and signal sources..."),
                    ("🧠", "Applying cultural and contextual frameworks..."),
                    ("🔍", "Structuring pattern detection models..."),
                    ("⚡", "Preparing systems for insight extraction..."),
                    ("🏁", "Finalizing observatory setup..."),
                ]

                build_container = st.container()
                
                with build_container:
                    build_log = st.empty()
                    
                    completed_steps = []
                    
                    for i, (emoji, msg) in enumerate(steps):
                        
                        current_steps = completed_steps + [f"🔄 {msg}"]
                        
                        # Display all steps
                        log_html = "<div style='font-family: monospace; font-size: 14px; line-height: 1.8;'>"
                        for step in current_steps[:-1]:  # completed steps
                            log_html += f"<div style='margin: 5px 0;'>{step}</div>"
                        # current step with spinner
                        log_html += f"<div style='margin: 5px 0; animation: pulse 1.5s infinite;'>{current_steps[-1]}</div>"
                        log_html += "</div>"
                        
                        # Add CSS for spinner animation
                        st.markdown("""
                        <style>
                        @keyframes pulse {
                            0% { opacity: 1; }
                            50% { opacity: 0.5; }
                            100% { opacity: 1; }
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        build_log.markdown(log_html, unsafe_allow_html=True)
                        
                        # Simulate work time
                        if i in [0, 5]:
                            time.sleep(1.5)
                        else:
                            time.sleep(2.5)
                        
                        completed_steps.append(f"✅ {emoji} {msg.replace('...', ' - Complete')}")
                    
                    # Final display with all completed steps
                    final_log_html = "<div style='font-family: monospace; font-size: 14px; line-height: 1.8;'>"
                    for step in completed_steps:
                        final_log_html += f"<div style='margin: 5px 0;'>{step}</div>"
                    final_log_html += "</div>"
                    
                    build_log.markdown(final_log_html, unsafe_allow_html=True)
                    
                    time.sleep(1)
                    
                    st.success("🎉 Observatory Built Successfully!")
            
            st.session_state.selected_study = next(iter(all_data[st.session_state.brand_config["brand_name"]]))
            st.session_state.studies = []
            st.session_state.global_configured = True
            st.rerun()

        st.stop()

# 2. Left Sidebar
with st.sidebar:
    brand = st.session_state.brand_config["brand_name"]

    # --- Group 1: Market ---
    studies = list(all_data[brand].keys())
    if st.session_state.selected_study not in studies:
        st.session_state.selected_study = studies[0]
    
    current = st.session_state.selected_study
    selection = st.selectbox(
        "Active Market",
        studies,
        index=studies.index(current)
    )
    if selection != current:
        st.session_state.selected_study = selection
        st.rerun()

    if st.button("➕ New Market", use_container_width=True):
        pass

    # Bigger gap between sections
    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

    # --- Group 2: Brand ---
    brand_options = [b.title() for b in all_data.keys()]
    default_idx = brand_options.index(brand.title()) if brand.title() in brand_options else 0
    selected_brand = st.selectbox("Active Brand", brand_options, index=default_idx)

    if selected_brand.lower() != brand.lower():
        st.session_state.brand_config["brand_name"] = selected_brand.lower()
        st.session_state.selected_study = next(iter(all_data[selected_brand.lower()]))
        st.rerun()

    if st.button("➕ New Brand", use_container_width=True):
        pass

    # Bigger gap between sections
    st.markdown("<div style='margin-bottom:1.5rem;'></div>", unsafe_allow_html=True)

    # --- Group 3: Ask Kultie ---
    user_query = st.text_area(
        "Ask Kultie ✨",
        placeholder="Type your question about markets, brands, or culture..."
    )
    if st.button("Send", use_container_width=True):
        pass


# 3. Create Study Form
if st.session_state.get("creating_study", False):
    st.subheader("Create New Project")

    if "study_templates_remaining" not in st.session_state:
        st.session_state.study_templates_remaining = [
            name
            for name in all_data.get(brand, {})
            if name != "Global Insights"
        ]

    with st.form("new_study"):
        choices = [""] + st.session_state.study_templates_remaining
        name = st.selectbox("Project Name", choices)
        
        focus = st.multiselect(
            "Strategic Focus Areas",
            options=[
                "Increase Brand Awareness",
                "Create a New Product Category",
                "Mitigate Brand or Reputation Risk",
                "Assess a New Business Opportunity",
                "Understand Consumer Behavior",
                "Identify Market Trends",
                "Measure Brand Perception",
                "Competitive & White Space Analysis",
                "Cultural Signals & Sentiment"
            ],
            placeholder="Select key focus areas",
            help="High-level business driver or purpose (e.g., launch planning, risk mitigation, trend spotting)."
        )

        objectives = st.text_area(
            "Research Objectives",
            placeholder=(
                "What do you need to learn or decide? "
                "Frame as specific objectives (e.g., size the market, map competitors, "
                "explore consumer motivations, test concept resonance)."
            ),
            help="Specific outcomes or decisions the research should enable. Action-oriented and measurable."
        )

        assumptions = st.text_area(
            "Assumptions, Hypotheses & Open Questions",
            placeholder=(
                "List starting assumptions, cultural/contextual beliefs, and hypotheses to test. "
                "Include open questions driving exploration."
            ),
            help="Current beliefs, theories or unknowns that shape the research. "
                "These will be validated, challenged or refined."
        )

        use_of_findings = st.text_area(
            "Intended Use of Findings",
            placeholder="e.g., support product launch strategy, investor pitch, brand repositioning",
            help="Where and how the results will influence decisions or actions."
        )

        kpis = st.text_area(
            "Key Metrics or KPIs",
            placeholder="e.g., awareness lift %, adoption intent, market size (USD), NPS change",
            help="Quantifiable measures of success or indicators you plan to track."
        )

        geos = st.multiselect(
            "Target Geographies",
            options=[
                "Global", "North America", "Europe", "Asia-Pacific", "Latin America", 
                "Middle East & Africa", "Thailand", "Malaysia", "Singapore", 
                "Indonesia", "Philippines", "Vietnam", "Japan", "South Korea", 
                "China", "India", "Australia"
            ],
            placeholder="Select target markets",
            help="Regions or markets relevant to this study."
        )
        
        ages = st.multiselect(
            "Target Age Groups",
            options=[
                "All Ages", "Gen Alpha (2010+)", "Gen Z (1997-2012)", 
                "Millennials (1981-1996)", "Gen X (1965-1980)", 
                "Boomers (1946-1964)"
            ],
            placeholder="Select audience age ranges",
            help="Target consumer age segments."
        )
        
        personas = st.multiselect(
            "Target Personas",
            options=[
                "Category Buyers", "Early Adopters", "Influencers/Trendsetters",
                "Cultural Creatives", "Value-Conscious Consumers", 
                "Industry Decision Makers", "Custom Persona"
            ],
            placeholder="Select audience personas",
            help="Key consumer or stakeholder profiles for focus."
        )
        
        create = st.form_submit_button("Create Project")

    if create:
        if name:
            new = {
                "id": str(len(st.session_state.studies)+1),
                "name": name,
                "focus": focus,
                "objectives": objectives,
                "assumptions": assumptions,
                "demographics": {"geos": geos, "ages": ages, "personas": personas}
            }
            st.session_state.studies.append(new)
            st.session_state.study_templates_remaining.remove(name)
            st.session_state.selected_study = name
        
            if not is_dev_mode:
                steps = [
                    ("🔧", f"Initializing project '{name}' environment..."),
                    ("📝", "Generating project structure..."),
                    ("⚙️", "Integrating parameters and settings..."),
                    ("🏁", "Finalizing project setup..."),
                ]
                log = st.empty()
                done = []
                for i, (emoji, msg) in enumerate(steps):
                    html = "<div style='font-family: monospace;'>"
                    for step in done:
                        html += f"<div>✅ {step}</div>"
                    html += f"<div style='animation: pulse 1.5s infinite;'>🔄 {msg}</div></div>"
                    st.markdown(
                        "<style>@keyframes pulse {0%{opacity:1;}50%{opacity:0.5;}100%{opacity:1;}}</style>",
                        unsafe_allow_html=True
                    )
                    log.markdown(html, unsafe_allow_html=True)
                    time.sleep(1 if i in (0, len(steps)-1) else 1.5)
                    done.append(f"{emoji} {msg}")
                # final success
                st.success(f"🎉 Project '{name}' Created Successfully!")
        
        st.session_state.creating_study = False
        st.rerun()
    st.stop()

# 4. Main Insight Page
brand = st.session_state.brand_config["brand_name"]
study = st.session_state.selected_study

st.markdown(
    f"<h1 style='text-align:center'>{brand.title()}: {study}</h1>",
    unsafe_allow_html=True,
)

if study is None or study not in all_data.get(brand, {}):
    st.error(f"No project selected for {brand}.")
    st.stop()

data = all_data[brand][study]
renderer = InsightsRenderer(data)
renderer.render()
