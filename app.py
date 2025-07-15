import streamlit as st

# --- Page Config & Custom CSS ---
st.set_page_config(page_title="Cultural Insight Demo", layout="wide")

# --- Sidebar: Data Source & Modality Selection ---
with st.sidebar:
    st.header("Data Configuration")
    sources = st.multiselect("Select Sources", 
        ["Reddit", "YouTube", "Blogs", "Forums", "Transcripts"]
        , default=["Reddit", "YouTube", "Blogs"]
    )
    modalities = st.multiselect("Select Modalities",
        ["Text", "Images", "Video", "Audio", "Networks"],
         default=["Text"]
    )
    geographies = st.multiselect(
        "Select Geography",
        ["Global", "Malaysia", "Thailand", "Japan"],
        default=["Malaysia"]
    )
    languages = st.multiselect(
        "Select Language",
        ["Any", "English", "Bahasa Melayu", "Mandarin", "Tamil"],
        default=["English", "Bahasa Melayu"]
    )
    keywords = st.text_input("Target Keywords/Phrases", "parenting, health")
    instructions = st.text_area(
        "Text Instructions",
        "E.g. focus on urban millennial parents"
    )
    website = st.text_input(
        "Company Website",
        "https://www.morinaga.co.jp/"
    )
    apply_config = st.button("Apply Configuration")

if not apply_config:
    st.info("Please choose your data sources, modalities and keywords, then click **Apply Configuration** to view insights.")
else:
    # --- Module 1: Persona Snapshots ---
    st.subheader("Persona Snapshots")

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


    # --- Module 2: Thematic Analysis — Narrative Themes ---
    st.subheader("Narrative Themes")

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

    # --- Module 3: Emerging Trends & Forecasts ---
    st.subheader("Emerging Trends & Forecasts")

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
