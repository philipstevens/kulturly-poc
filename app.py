import streamlit as st
import datetime
import time  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import altair as alt
from sklearn.manifold import TSNE 


def render_narratives_tab():
    narratives = [
        {
            "title": "TikTok Commerce Revolution",
            "story": (
                "In Indonesia, TikTok Shop transforms shopping into live entertainment—"
                "streamers debut new collections and viewers buy directly via in-app links."),
            "evidence": (
                "[VulcanPost on TikTok Shop’s growth]"
                "(https://vulcanpost.com/834059/can-tiktok-shop-dethrone-shopee-lazada/) and "
                "[RTL Today on social-commerce trends]"
                "(https://today.rtl.lu/news/business-and-tech/a/2078371.html)"),
            "impact": "Leverage shoppable live events to create buzz around product launches."
        },
        {
            "title": "Authentic Local Pride Movement",
            "story": (
                "‘Made in Indonesia’ sneaker pop-ups spark grassroots rallies—"
                "consumers wear local brands as statements of national pride."),
            "evidence": (
                "60.7% of Indonesians prefer local affordable products "
                "[SemanticsScholar study]"
                "(https://pdfs.semanticscholar.org/f0f9/df7097005f4aad83088ec3528c5d1d7e417a.pdf)"),
            "impact": "Co-create limited editions with local artisans to tap into cultural nationalism."
        },
        {
            "title": "Traditional Sports Resurgence",
            "story": (
                "Sepak Takraw tournaments and Muay Thai events go viral on social feeds, "
                "drawing millions of interactions."),
            "evidence": (
                "Thailand’s Panipak Tennis Olympic gold generated 3M+ social interactions in one day "
                "[DataXet report]"
                "(https://www.dataxet.co/insights/olympic-games-2024-en)"),
            "impact": "Sponsor grassroots tournaments and integrate classical motifs into designs."
        },
        {
            "title": "Nano-Influencer Trust Economy",
            "story": (
                "Micro-influencers (1k–10k followers) spark authentic conversations—"
                "their daily posts on Puma gear drive deeper trust than celebrity endorsements."),
            "evidence": (
                "Nano-influencers command 46% greater trust [Pongoshare report]"
                "(http://pongoshare.com/trends-in-influencer-marketing-southeast-asia/) and "
                "87% of Indonesians prefer intimate messaging interactions [Statista]"
                "(https://www.statista.com/forecasts/1345510/asia-most-used-social-media-platforms-of-gen-z-by-country-and-type)"),
            "impact": "Build city-by-city micro-ambassador programs to amplify genuine stories."
        },
        {
            "title": "Cross-Cultural K-Wave Integration",
            "story": (
                "K-pop ambassadors like Blackpink’s Rosé make Puma styles aspirational—"
                "fans emulate viral dance looks across SEA."),
            "evidence": (
                "K-pop drives SEA sportswear trends [Retail Asia]"
                "(https://retailasia.com/videos/korean-culture-drives-southeast-asia-sportswear-trends)"),
            "impact": "Align product drops with major K-pop comebacks and fan events."
        },
        {
            "title": "Digital-Physical Sport Fusion",
            "story": (
                "Runners and athletes document temple runs and treks in Puma gear—"
                "turning workouts into social challenges."),
            "evidence": (
                "Over 40% run weekly and share journeys online [YouGov Singapore]"
                "(https://business.yougov.com/content/50255-a-look-at-singapores-growing-running-community)"),
            "impact": "Create geo-tagged digital challenges that bridge culture and sport."
        },
        {
            "title": "Multigenerational Athletic Identity",
            "story": (
                "Olympic heroes and wellness seekers unite—grandparents and grandchildren "
                "share Puma fitness moments across generations."),
            "evidence": (
                "Cross-generational fitness engagement rising in SEA [DataXet, JLL]"
                "(https://www.jll.com.sg/en/trends-and-insights/research/thailand-s-sports-boom-energizes-the-retail-market)"),
            "impact": "Design campaigns celebrating family fitness and rituals."
        }
    ]

    st.markdown("### Emergent Cultural Narratives")
    for nar in narratives:
        with st.expander(nar["title"], expanded=False):
            st.markdown(f"**Story:** {nar['story']}")
            st.markdown(f"**Evidence:** {nar['evidence']}")
            st.markdown(f"**Strategic Impact:** {nar['impact']}")

    st.markdown("### Cross-Cultural Differences in Framing")
    with st.expander("Performance vs. Lifestyle", expanded=False):
        st.markdown("**Indonesia:** frames fitness as community building and faith-compatible wellness")
        st.markdown("**Malaysia:** balances multicultural sporting traditions with modern athleisure")
        st.markdown("**Thailand:** emphasizes individual achievement and national pride.")
        st.markdown("**Evidence:** [Sport in Thailand – Wikipedia](https://en.wikipedia.org/wiki/Sport_in_Thailand), "
                    "[JLL Thailand Sports Boom](https://www.jll.com.sg/en/trends-and-insights/research/thailand-s-sports-boom-energizes-the-retail-market)")
        st.markdown("**Strategic Impact:** Tailor messaging to resonate with local cultural values and sporting traditions.")
    with st.expander("Community vs. Individualism", expanded=False):
        st.markdown("**Indonesia:** emphasizes collective fitness journeys and community events")
        st.markdown("**Malaysia:** blends individual aspirations with multicultural community spirit")
        st.markdown("**Thailand:** focuses on personal achievement and national pride in sports.")
        st.markdown("**Evidence:** [YouGov Singapore Running Community](https://business.yougov.com/content/50255-a-look-at-singapores-growing-running-community), "
                    "[Retail Asia K-Wave Trends](https://retailasia.com/videos/korean-culture-drives-southeast-asia-sportswear-trends)")
        st.markdown("**Strategic Impact:** Leverage local cultural narratives to build community-driven campaigns.")
    with st.expander("Tradition vs. Modernity", expanded=False):
        st.markdown("**Indonesia:** integrates traditional sports with modern athleticism")
        st.markdown("**Malaysia:** balances heritage sports with contemporary fitness trends")
        st.markdown("**Thailand:** celebrates traditional martial arts alongside modern fitness.")
        st.markdown("**Evidence:** [SemanticsScholar Local Product Preference](https://pdfs.semanticscholar.org/f0f9/df7097005f4aad83088ec3528c5d1d7e417a.pdf), "
                    "[DataXet Olympic Engagement](https://www.dataxet.co/insights/olympic-games-2024-en)")
        st.markdown("**Strategic Impact:** Highlight Puma’s role in bridging cultural heritage with modern athleticism.")


def render_personas_tab():
    personas = [
        {
            "name": "Digital Native Athletes",
            "share": "25%",
            "traits": ["Gen Z (18–25)", "Urban & tech‑savvy", "60% spend 6+ hours on mobile daily", "Performance‑focused", "Fastest growing segment 🚀"],
            "behaviors": "Document fitness journeys, value tech innovation; Paralympic inclusion sparked fresh momentum in Indonesia.",
            "evidence": (
                '<a href="https://www.mili.eu/sg/insights/meet-southeast-asias-gen-z" target="_blank">Meet SEA’s Gen Z</a>'
                ', '
                '<a href="https://seasia.co/infographic/what-are-the-top-google-searches-in-southeast-asia-in-2024" target="_blank">Top SEA searches 2024</a>'
            ),
            "implications": "Engage via in-app fitness features and inclusive performance storytelling."
        },
        {
            "name": "Heritage‑Forward Trendsetters",
            "share": "30%",
            "traits": ["Millennials (26–35)", "Middle‑income", "Cultural pride‑driven", "Multilingual content creators"],
            "behaviors": "Blend traditional & modern aesthetics, support local brands, lead cultural storytelling.",
            "evidence": ('<a href="https://seasia.co/infographic/how-many-gen-z-in-southeast-asia-2024" target="_blank">SEA Gen Z insights</a>'),
            "implications": "Collaborate with artisans for fusion designs and heritage narratives."
        },
        {
            "name": "Social Commerce Enthusiasts",
            "share": "20%",
            "traits": ["Gen Z females (18–24)", "High social‑media engagement", "Live shopping participants"],
            "behaviors": "Drive purchases through entertaining live‑shop events on TikTok & Instagram.",
            "evidence": ('<a href="https://vulcanpost.com/834059/can-tiktok-shop-dethrone-shopee-lazada/" target="_blank">TikTok Shop growth</a> , '
                        '<a href="https://today.rtl.lu/news/business-and-tech/a/2078371.html" target="_blank">TikTok commerce trends</a>'),
            "implications": "Host influencer‑led live shopping events to accelerate conversion."
        },
        {
            "name": "Authentic Community Builders",
            "share": "25%",
            "traits": ["Mixed ages (20–35)", "Micro‑influencers", "Community‑focused", "Authenticity‑driven"],
            "behaviors": "Trust nano‑influencers, champion transparent practices, create lasting advocacy.",
            "evidence": ('<a href="http://pongoshare.com/trends-in-influencer-marketing-southeast-asia/" target="_blank">Nano-influencer trust</a>'),
            "implications": "Launch micro‑ambassador programs to amplify authentic stories."
        },
        {
            "name": "Glocal Cultural Curators",
            "share": "Emergent segment",
            "traits": ["Hybrid global‑local identities", "Trend synthesizers", "Resist categorization", "High creativity"],
            "behaviors": "Blend global trends with local expressions to craft unique cultural mashups.",
            "evidence": "Identified via emergent content clustering in SEA channels.",
            "implications": "Pilot co‑creation labs with curators to refine hybrid campaigns."
        }
    ]

    # Display as styled cards with inline details
    cols = st.columns(3)
    for idx, p in enumerate(personas):
        col = cols[idx % 3]
        traits_str = "<br> ".join(p['traits'])
        card_html = (
            '<div style="border:1px solid #ddd; border-radius:8px; padding:16px; margin-bottom:16px;">'
            '  <h4 style="margin:0 0 8px 0;">{name} <span style="font-size:0.85em; color:#666;">({share})</span></h4>'
            '  <p style="margin:4px 0;"><strong>Traits:</strong> <br> {traits}</p>'
            '  <details style="margin-top:8px;">'
            '    <summary style="font-weight:bold; cursor:pointer;">More details</summary>'
            '    <p style="margin:4px 0;"><strong>Behaviors:</strong> {behaviors}</p>'
            '    <p style="margin:4px 0;"><strong>Evidence:</strong> {evidence}</p>'
            '    <p style="margin:4px 0;"><strong>Implications:</strong> {implications}</p>'
            '  </details>'
            '</div>'
        ).format(
            name=p['name'], share=p['share'], traits=traits_str,
            behaviors=p['behaviors'], evidence=p['evidence'], implications=p['implications']
        )
        col.markdown(card_html, unsafe_allow_html=True)


def render_networks_tab():
    st.subheader("Core Networks & Influencers")

    # 1) Core Influence Narratives
    narratives = [
        {
            "title": "TikTok Creator Economy",
            "story": (
                "Algorithm‑driven discovery on TikTok spawns new influence pathways beyond simple follower counts. "
                "Nano‑influencers (1k–10k followers) achieve viral reach by blending entertainment and commerce—"
                "key brokers are live sellers who demo product and entertain in one stream."
            ),
            "evidence": (
                "[RTL Today on social commerce trends]"
                "(https://today.rtl.lu/news/business-and-tech/a/2078371.html)  "
                "[Marketing Interactive on TikTok cultural play]"
                "(https://www.marketing-interactive.com/tiktok-is-gen-z-s-cultural-playground-in-southeast-asia)"
            ),
            "takeaway": "Partner with top live sellers and optimize for discovery‑first content formats."
        },
        {
            "title": "Traditional Sports Communities",
            "story": (
                "Olympic heroes (like Tennis Panipak), community gym leaders and indigenous sport masters "
                "create authentic cultural moments that bridge the digital and physical worlds."
            ),
            "evidence": (
                "[DataXet Olympic social engagement]"
                "(https://www.dataxet.co/insights/olympic-games-2024-en)"
            ),
            "takeaway": "Activate athlete ambassadors and local club sponsorships to spark organic buzz."
        },
        {
            "title": "Sneakerhead Collectors",
            "story": (
                "Local sneaker exhibitions and heritage‑brand founders fuel the #LocalPride movement. "
                "They blend IRL events with digital storytelling to anchor powerful cultural narratives."
            ),
            "evidence": (
                "[SemScholar on local product preference]"
                "(https://pdfs.semanticscholar.org/f0f9/df7097005f4aad83088ec3528c5d1d7e417a.pdf)  "
                "[SNKRDUNK on sneaker culture]"
                "(https://snkrdunk.com/en/magazine/2024/08/07/snkrdunk-streetsnaps-rise-of-the-sneakers-the-playground-2024/)"
            ),
            "takeaway": "Co‑produce limited‑edition drops and livestream event recaps to amplify collector networks."
        }
    ]

    for n in narratives:
        with st.expander(n["title"], expanded=False):
            st.markdown(f"**Story:** {n['story']}")
            st.markdown(f"**Evidence:** {n['evidence']}")
            st.markdown(f"**Strategic Takeaway:** {n['takeaway']}")

    # 2) Diffusion Pathways
    st.markdown("### 🔄 Diffusion Pathways")
    st.code(
        "Cultural Moment → TikTok Algorithm → Instagram Reels → Local Forums → Physical Adoption\n"
        "Olympic Victory → Viral Content → Community Discussion → Product Interest → Purchase\n"
        "Local Exhibition → Social Documentation → Hashtag Movement → Mainstream Adoption"
    )

    # 3) Key Cultural Brokers
    st.markdown("### Key Cultural Brokers by Market")
    brokers = {
        "Indonesia": [
            "Christine Febriyanti (TikTok live seller)",
            "Local sneaker exhibition organizers",
            "Paralympic athlete influencers"
        ],
        "Malaysia": [
            "Multilingual content creators",
            "Sepak Takraw community leaders",
            "Tech‑lifestyle influencers"
        ],
        "Thailand": [
            "Tennis Panipak (Olympic gold medalist)",
            "Muay Thai fitness influencers",
            "Royal‑aesthetic lifestyle creators"
        ]
    }
    for market, names in brokers.items():
        st.markdown(f"**{market}:**")
        for name in names:
            st.markdown(f"- {name}")

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
# st.session_state.configured = True # default to True for demo purposes, remove for deployment
if "configured" not in st.session_state:
    st.session_state.configured = False


# ― Tabs ―
tabs = st.tabs([
    "Context",
    "Narratives & Topics",
    "Personas & Cohorts",
    "Networks & Influence",
    "Trends & Events",
    "Hypotheses & Recommendations"
])

# ― Tab 1: Data Configuration ―
with tabs[0]:
    # Main search box
    st.markdown('<div class="centered-title">What Do You Want to Explore?</div>', unsafe_allow_html=True)
    query = st.text_area(
        "",
        height=80,
        placeholder=(
            "I want to better understand what’s shaping Puma’s relevance and growth in SEA, based on recent campaigns, social media activity, and cultural signals. " +
            "Specifically, how does Puma balance global consistency with local authenticity? " +
            "Which emerging trends define Puma’s cultural relevance in Thailand, Malaysia, Indonesia?"
            
            # "Describe the market, segment, and key question you’re exploring…"
        )
    )

    st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)

    # --- Advanced Context Expander ---
    with st.expander("Context Settings", expanded=False):
        internal = st.text_input(
            "Internal Assets (URL or upload)",
            placeholder="https://www.puma.com/",
            help="Optional: include a company domain or local file for context"
        )

        geographies = st.multiselect(
            "Geography",
            ["Global", "Malaysia", "Thailand", "indonesia", "Japan"],
            default=["Malaysia", "Thailand", "indonesia"],
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
            placeholder="Identify emerging trends",
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
            default=["Urban Millennials", "Gen Z"],
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
            index=industries.index("Apparel & Fashion"),
            placeholder="Apparel & Fashion",
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
            "Children’s & Maternity Clothing"
        ]
        product_type = st.multiselect(
            "Product Type",
            product_types,
            default=[
                "Footwear",
                "Athleisure & Activewear",
                "Streetwear & Urban Fashion"
            ],
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
            default=["Text", "Image"],
            help="Select content formats to include. Text includes available transcripts for audio/video sources."
        )

        # Enable network/influence analysis
        enable_network = st.checkbox(
            "Enable Network Analysis & Influence Mapping",
            key="adv_enable_network",
            value=True,
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
        render_narratives_tab()

# ― Tab 3: Persona Snapshots ―
with tabs[2]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        render_personas_tab()
        # persona_data = [
        #     {
        #         "name": "Scientific Modern Mom",
        #         "traits": ["Data‑driven", "Expert trust", "Analytical"],
        #         "motivations": ["Optimal child health", "Scientific validation"],
        #         "media": ["@health_blog", "ScienceDaily"]
        #     },
        #     {
        #         "name": "Traditional Herbalist",
        #         "traits": ["Holistic", "Cultural roots", "Natural remedies"],
        #         "motivations": ["Ancestral wisdom", "Organic living"],
        #         "media": ["HerbWorld", "NativePlantsMag"]
        #     },
        #     {
        #         "name": "Anxious First‑Timer",
        #         "traits": ["Safety‑first", "Over‑researcher", "Risk‑averse"],
        #         "motivations": ["Peace of mind", "Community reassurance"],
        #         "media": ["BabyStepsForum", "ParentingNow"]
        #     }
        # ]

        # cols = st.columns(len(persona_data))
        # for col, persona in zip(cols, persona_data):
        #     with col:
        #         st.markdown('<div class="card">', unsafe_allow_html=True)
        #         st.markdown(f"### {persona['name']}")
        #         st.markdown("**Traits:**")
        #         for trait in persona["traits"]:
        #             st.markdown(f"- {trait}")
        #         st.markdown("**Motivations:**")
        #         for motive in persona["motivations"]:
        #             st.markdown(f"- {motive}")
        #         st.markdown("**Media Anchors:**")
        #         for anchor in persona["media"]:
        #             st.markdown(f"- {anchor}")
        #         st.markdown('</div>', unsafe_allow_html=True)

# ― Tab 4: Networks & Influence ―
with tabs[3]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        render_networks_tab()
        # influence_data = [
        #     {
        #         "name": "Dr. Sarah Lim",
        #         "role": "Pediatrician & Parenting Author",
        #         "influence": "Trusted source for infant nutrition advice",
        #         "reach": "200K followers on Instagram",
        #         "impact": "Endorses specific formula brands"
        #     },
        #     {
        #         "name": "MamaMia Community",
        #         "role": "Parenting Forum & Support Group",
        #         "influence": "Platform for shared experiences and recommendations",
        #         "reach": "50K active members",
        #         "impact": "High engagement on formula discussions"
        #     },
        #     {
        #         "name": "Healthy Baby Blog",
        #         "role": "Nutrition & Wellness Influencer",
        #         "influence": "Focuses on science-backed parenting tips",
        #         "reach": "150K followers across platforms",
        #         "impact": "Promotes clean-label formulas"
        #     }
        # ]

        # cols = st.columns(len(influence_data))
        # for col, influencer in zip(cols, influence_data):
        #     with col:
        #         st.markdown('<div class="card">', unsafe_allow_html=True)
        #         st.markdown(f"### {influencer['name']}")
        #         st.markdown(f"*{influencer['role']}*")
        #         st.markdown("**Influence:**")
        #         st.markdown(f"- {influencer['influence']}")
        #         st.markdown("**Reach:**")
        #         st.markdown(f"- {influencer['reach']}")
        #         st.markdown("**Impact:**")
        #         st.markdown(f"- {influencer['impact']}")
        #         st.markdown('</div>', unsafe_allow_html=True)

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

with tabs[5]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        st.markdown("### Hypotheses & Recommendations")
        st.markdown(
            "Based on the insights generated, we recommend the following strategic hypotheses:"
        )
        st.markdown(
            "- **Hypothesis 1:** Puma can enhance brand loyalty by integrating local cultural narratives into product design."
        )
        st.markdown(
            "- **Hypothesis 2:** Collaborating with micro-influencers will amplify authentic engagement in SEA markets."
        )
        st.markdown(
            "- **Hypothesis 3:** Leveraging TikTok’s live shopping features can drive higher conversion rates among Gen Z consumers."
        )















#     # --- Module 2: Thematic Analysis — Narrative Themes ---
#     st.subheader("Narrative Themes")



#     # --- Module 3: Emerging Trends & Forecasts ---
#     st.subheader("Emerging Trends & Forecasts")


