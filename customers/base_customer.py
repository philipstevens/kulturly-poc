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

        st.markdown('<div class="space-title">Build Your Cultural Observatory</div>', unsafe_allow_html=True)
        st.markdown('<div class="space-subtitle">Define your cultural space before exploring insights</div>', unsafe_allow_html=True)

        # Space Name
        space_name = st.text_input(
            "Space Name",
            placeholder="e.g., 'Puma Culture Watch: SEA'",
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
                default=self.config.get("default_cultural_domains", ["Sports & Athletics", "Lifestyle & Wellness", "Fashion & Style"]),
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
                default=self.config.get("default_modifiers", ["Youth", "Modern", "Urban"]),
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

        st.markdown('<div class="section-header">Alignment References</div>', unsafe_allow_html=True)
        
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
                    placeholder="streetwear\nsustainable fashion\nK-beauty\nwellness trends",
                    help="Cultural terms and trends to monitor (one per line)"
                )
    
        
        if st.button("Build Cultural Observatory", type="primary", use_container_width=True):
            steps = [
                ("🔧", "Initializing observatory environment..."),
                ("🔗", "Linking relevant data and signal sources..."),
                ("🧠", "Applying cultural and contextual frameworks..."),
                ("🔍", "Structuring pattern detection models..."),
                ("⚡", "Preparing systems for insight extraction..."),
                ("🏁", "Finalizing observatory setup..."),
            ]
            
            # Container for the build log
            build_container = st.container()
            
            with build_container:
                build_log = st.empty()
                
                completed_steps = []
                
                for i, (emoji, msg) in enumerate(steps):
                    # Add current step as "in progress"
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
                    
                    # Mark step as completed
                    completed_steps.append(f"✅ {emoji} {msg.replace('...', ' - Complete')}")
                
                # Final display with all completed steps
                final_log_html = "<div style='font-family: monospace; font-size: 14px; line-height: 1.8;'>"
                for step in completed_steps:
                    final_log_html += f"<div style='margin: 5px 0;'>{step}</div>"
                final_log_html += "</div>"
                
                build_log.markdown(final_log_html, unsafe_allow_html=True)
                
                # Add a brief pause before success message
                time.sleep(1)
                
                st.success("🎉 Observatory Built Successfully! Other tabs are now unlocked.")
                
            st.session_state.configured = True

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

    def render_ask(self):
        pass

    def render_deep_dive(self):
        pass
