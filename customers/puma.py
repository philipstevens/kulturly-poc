# customers/puma.py

import streamlit as st
from customers.base_customer import BaseCustomerRenderer
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import openai
import os
import time
import pathlib
import altair as alt

class Puma(BaseCustomerRenderer):
    def __init__(self):
        super().__init__(
            name="Puma",
            data_path="data/puma.json"
        )
    
    def _parse_markdown_links(self, text):
        """Convert markdown-style links [text](url) to HTML <a> tags"""
        import re
        # if they passed a list of strings, join into one
        if isinstance(text, (list, tuple)):
            text = "<br>".join(text)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.sub(pattern, r'<a href="\2" target="_blank">\1</a>', text)
    
    def render_stories(self):
        main_tabs = st.tabs([
            "📖 Themes", 
            "🔎 Deep Patterns", 
            "🔗 Shared Signals",
            "🌍 Local Lenses", 
            "🧠 Word Shifts"  
        ])
        
        # Tab 1: Cultural Narratives
        with main_tabs[0]:
            st.caption("Observable stories and behaviors shaping culture right now • Last scan: 2 hours ago")
            
            stories = self.data.get("stories", [])

            cols = st.columns(2)
            for idx, nar in enumerate(stories):
                col = cols[idx % 2]
                confidence_pct = int(nar["confidence"] * 100)
                evidence_html = self._parse_markdown_links(nar["evidence"])
                
                # Create an engaging card with key info upfront
                with col:
                    # Create card using simple HTML structure like in render_people
                    card_html = (
                        f'<div style="border: 2px solid {nar["trend_color"]}; border-radius: 8px; padding: 16px; margin-bottom: 16px;">'
                        f'  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
                        f'    <strong style="font-size: 16px;">{nar["title"]}</strong>'
                        f'    <b><small style="background-color: {nar["trend_color"]}; color: black; padding: 2px 6px; border-radius: 4px; font-size: 14px;">{nar["maturity"]}</small></b>'
                        f'  </div>'
                        f'  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 12px 0;">'
                        f'    <div><strong>{nar["momentum"]}</strong></div>'
                        f'    <div><strong>{confidence_pct}% confidence</strong></div>'
                        f'    <div><strong>Volume:</strong> {nar["volume"]}</div>'
                        f'    <div><strong>Velocity:</strong> {nar["velocity"]}</div>'
                        f'  </div>'
                        f'  <details style="margin-top: 16px; border-radius: 8px; overflow: hidden;">'
                        f'    <summary style="font-weight: bold; cursor: pointer;">Full Details</summary>'
                        f'    <div style="padding: 0 16px 16px; border-top: 1px solid; line-height: 1.6;">'
                        f'      <section style="margin: 12px 0;">'
                        f'        <h4 style="margin: 0 0 4px; font-size: 14px;">Story</h4>'
                        f'        <p style="margin: 0;">{nar["story"]}</p>'
                        f'      </section>'
                        f'      <section style="margin: 12px 0;">'
                        f'        <h4 style="margin: 0 0 4px; font-size: 14px;">Evidence</h4>'
                        f'        <p style="margin: 0;">{evidence_html}</p>'
                        f'      </section>'
                        f'      <section style="margin: 12px 0;">'
                        f'        <h4 style="margin: 0 0 4px; font-size: 14px;">Strategic Impact</h4>'
                        f'        <p style="margin: 0;">{nar["impact"]}</p>'
                        f'      </section>'
                        f'      <section style="margin: 12px 0;">'
                        f'        <h4 style="margin: 0 0 4px; font-size: 14px;">Timeline</h4>'
                        f'        <p style="margin: 0;">First seen: {nar["first_seen"]}</p>'
                        f'      </section>'
                        f'    </div>'
                        f'  </details>'
                        '</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

        # Tab 2: Regional Framings
        with main_tabs[3]:
            st.caption("How core ideas are locally interpreted and emphasized across cultures")
            
            framing_tabs = st.tabs(["Performance vs. Lifestyle", "Community vs. Individualism", "Tradition vs. Modernity"])
            
            regional_framing_data = [
                {
                    "title": "Performance vs. Lifestyle",
                    "data": [
                        {"Country": "Indonesia", "Cultural Framing": "Frames fitness as community building and faith-compatible wellness", "Key Indicators": "Community gyms, halal fitness programs"},
                        {"Country": "Malaysia", "Cultural Framing": "Balances multicultural sporting traditions with modern athleisure", "Key Indicators": "Multi-ethnic sports, fusion wear trends"},
                        {"Country": "Thailand", "Cultural Framing": "Emphasizes individual achievement and national pride", "Key Indicators": "Olympic focus, Muay Thai heritage"}
                    ],
                    "evidence": [
                        ("Sport in Thailand – Wikipedia", "https://en.wikipedia.org/wiki/Sport_in_Thailand"),
                        ("JLL Thailand Sports Boom", "https://www.jll.com.sg/en/trends-and-insights/research/thailand-s-sports-boom-energizes-the-retail-market")
                    ],
                    "strategic_impact": "Tailor messaging to resonate with local cultural values and sporting traditions"
                },
                {
                    "title": "Community vs. Individualism", 
                    "data": [
                        {"Country": "Indonesia", "Cultural Framing": "Emphasizes collective fitness journeys and community events", "Key Indicators": "Group challenges, family fitness rituals"},
                        {"Country": "Malaysia", "Cultural Framing": "Blends individual aspirations with multicultural community spirit", "Key Indicators": "Personal goals within diverse communities"},
                        {"Country": "Thailand", "Cultural Framing": "Focuses on personal achievement and national pride in sports", "Key Indicators": "Individual excellence, national identity"}
                    ],
                    "evidence": [
                        ("YouGov Singapore Running Community", "https://business.yougov.com/content/50255-a-look-at-singapores-growing-running-community"),
                        ("Retail Asia K-Wave Trends", "https://retailasia.com/videos/korean-culture-drives-southeast-asia-sportswear-trends")
                    ],
                    "strategic_impact": "Leverage local cultural narratives to build community-driven campaigns"
                },
                {
                    "title": "Tradition vs. Modernity",
                    "data": [
                        {"Country": "Indonesia", "Cultural Framing": "Integrates traditional sports with modern athleticism", "Key Indicators": "Sepak takraw evolution, modern training methods"},
                        {"Country": "Malaysia", "Cultural Framing": "Balances heritage sports with contemporary fitness trends", "Key Indicators": "Traditional games, tech-enabled fitness"},
                        {"Country": "Thailand", "Cultural Framing": "Celebrates traditional martial arts alongside modern fitness", "Key Indicators": "Muay Thai culture, contemporary workouts"}
                    ],
                    "evidence": [
                        ("SemanticsScholar Local Product Preference", "https://pdfs.semanticscholar.org/f0f9/df7097005f4aad83088ec3528c5d1d7e417a.pdf"),
                        ("DataXet Olympic Engagement", "https://www.dataxet.co/insights/olympic-games-2024-en")
                    ],
                    "strategic_impact": "Highlight Puma's role in bridging cultural heritage with modern athleticism"
                }
            ]
            
            for i, content in enumerate(regional_framing_data):
                with framing_tabs[i]:
                    # Create an interactive table
                    import pandas as pd
                    df = pd.DataFrame(content["data"])
                    
                    # Display the table with proper formatting
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Country": st.column_config.TextColumn("Country", width="small"),
                            "Cultural Framing": st.column_config.TextColumn("Cultural Framing", width="large"),
                            "Key Indicators": st.column_config.TextColumn("Key Indicators", width="medium")
                        }
                    )
                    
                    # Add evidence with preserved links
                    evidence_links = [f"[{text}]({url})" for text, url in content["evidence"]]
                    st.markdown(f"**Evidence Sources:** {', '.join(evidence_links)}")
                    
                    # Add strategic impact
                    st.markdown(f"**Strategic Impact:** {content['strategic_impact']}")

        # Tab 3: Semantic Evolution
        with main_tabs[4]:
            st.caption("How key terms shift meaning across contexts and time")
            evolution_data = {
                "Athletic": {
                    "evolution": {
                        "2020": "Performance-driven, elite training and competition",
                        "2022": "Holistic wellness, part of daily lifestyle",
                        "2024": "Cultural ritual and intergenerational identity expression"
                    },
                    "shift_driver": "Rise of family fitness rituals + digital temple run culture"
                },
                "Local": {
                    "evolution": {
                        "2020": "Lower-cost, less prestigious alternative to global",
                        "2022": "Conscious consumer choice rooted in ethics and community",
                        "2024": "Badge of national pride and creative defiance ('Bangga Buatan Lokal')"
                    },
                    "shift_driver": "Authentic Local Pride Movement + youth-led brand activism"
                },
                "Influencer": {
                    "evolution": {
                        "2020": "Celebrity-endorsed voice with mass appeal",
                        "2022": "Niche content creator with targeted trust",
                        "2024": "Micro-trusted insider shaping local peer norms"
                    },
                    "shift_driver": "Nano-Influencer Trust Economy + community-driven storytelling"
                },
                "Shopping": {
                    "evolution": {
                        "2020": "Utility-based transaction, often price-driven",
                        "2022": "Blended experience—store + screen",
                        "2024": "Live, immersive entertainment-commerce (e.g., TikTok Shop)"
                    },
                    "shift_driver": "TikTok Commerce Revolution + rise of shoppable livestreams"
                },
                "Sport": {
                    "evolution": {
                        "2020": "Competitive, rule-bound, institutional",
                        "2022": "Wellness-focused, self-paced and expressive",
                        "2024": "Hybrid ritual—physical + social + digital (e.g., temple runs, viral Muay Thai clips)"
                    },
                    "shift_driver": "Traditional Sports Resurgence + digital-physical fusion"
                },
                "Run": {
                    "evolution": {
                        "2020": "Solo fitness activity for endurance or health",
                        "2022": "Group challenge, social activity",
                        "2024": "Narrative moment—shared journey through culture and landscape"
                    },
                    "shift_driver": "Geo-tagged storytelling + Digital-Physical Sport Fusion"
                },
                "Family": {
                    "evolution": {
                        "2020": "Private unit of care and tradition",
                        "2022": "Support system for active aging and youth fitness",
                        "2024": "Visible multi-generational wellness tribe (e.g., shared gymwear, joint challenges)"
                    },
                    "shift_driver": "Multigenerational Athletic Identity + SEA aging dynamics"
                },
                "K-Pop": {
                    "evolution": {
                        "2020": "Youth entertainment from Korea",
                        "2022": "Style and beauty benchmark across Asia",
                        "2024": "Global commercial driver shaping fashion, sport, and fan identity"
                    },
                    "shift_driver": "Cross-Cultural K-Wave Integration + fandom-based fashion cycles"
                },
                "Pride": {
                    "evolution": {
                        "2020": "Personal achievement or social status",
                        "2022": "Cultural heritage and collective memory",
                        "2024": "Activist signal and community badge (e.g., wearing local = resistance + celebration)"
                    },
                    "shift_driver": "Local brand loyalty + youth-led identity politics"
                },
                "Event": {
                    "evolution": {
                        "2020": "Fixed-time, in-person occasion (concert, launch)",
                        "2022": "Hybrid, planned-in-advance live/digital blend",
                        "2024": "Fluid, participatory content moment (e.g., live drops, shoppable streams)"
                    },
                    "shift_driver": "Livestream culture + collapse of boundary between media & retail"
                }
            }
            tab_names = list(evolution_data.keys())
            tabs = st.tabs([f"{term}" for term in tab_names])
            for i, (term, data) in enumerate(evolution_data.items()):
                with tabs[i]:               
                    timeline_html = '<div style="border:1px solid #ddd; border-radius:8px; padding:16px; margin-bottom:16px;">'
                    for year, meaning in data["evolution"].items():
                        timeline_html += f'<div style="margin-bottom:12px;"><strong>{year}</strong> → {meaning}</div>'
                    timeline_html += '</div>'               
                    st.markdown(timeline_html, unsafe_allow_html=True)              
                    st.info(f"**Shift driver:** {data['shift_driver']}")

        # Tab 4: Hidden Dimensions
        with main_tabs[1]:
            st.caption("Underlying conceptual tensions organizing meaning across domains")
            dimensions = [
                {
                    "axis": "Traditional Heritage ↔ Global Modernity",
                    "intuitive_label": "From Temple Runs to TikTok Trends",
                    "strength": "Strong",
                    "key_markers": ["sepak takraw", "temple runs", "K-pop fashion", "TikTok Shop"],
                    "narrative": (
                        "This dimension reflects how audiences move between celebrating traditional rituals "
                        "and embracing hyper-globalized, digital-first experiences. Cultural authenticity and modern aspiration "
                        "aren't opposites—they’re being blended in new ways."
                    )
                },
                {
                    "axis": "Collective Identity ↔ Individual Aspiration",
                    "intuitive_label": "From Community Rituals to Personal Style",
                    "strength": "Moderate",
                    "key_markers": ["local brand pride", "family fitness", "nano-influencers", "Puma self-expression"],
                    "narrative": (
                        "People express themselves both as proud members of a cultural group and as individuals with distinct taste. "
                        "Whether through family workouts or curated fashion looks, this tension defines how identity is shaped today."
                    )
                },
                {
                    "axis": "Functional Use ↔ Experiential Performance",
                    "intuitive_label": "From Gear to Theater",
                    "strength": "Emerging",
                    "key_markers": ["product drop events", "live shopping", "temple runs", "performance gear"],
                    "narrative": (
                        "What used to be practical is now performative—shoes are worn to be seen in, shopping is entertainment, "
                        "and sport is a shareable spectacle. Audiences expect experiences, not just utility."
                    )
                }
            ]

            strength_colors = {
                "Emerging": "#FFA500",   # orange
                "Moderate": "#FFD700",   # gold
                "Strong":   "#00B050"    # green
            }

            cols = st.columns(3)
            for idx, dim in enumerate(dimensions):
                col = cols[idx % 3]
                border_color = strength_colors.get(dim["strength"], "#DDD")
                with col:
                    card_html = (
                            f'<div style="border:2px solid {border_color}; border-radius:8px; padding:16px; margin-bottom:16px;">'
                            f'  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">'
                            f'    <strong style="font-size:16px;">{dim["axis"]}</strong>'
                            f'  </div>'
                            f'  <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:12px 0;">'
                            f'    <div><strong>Signal Strength:</strong> <span style="background-color: {border_color}; color: black; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">{dim["strength"]}</span></div>'
                            f'    <div><strong>Key Markers:</strong> {", ".join(dim["key_markers"])}</div>'
                            f'  </div>'
                            f'  <details style="margin-top:16px; border-radius:8px; overflow:hidden;">'
                            f'    <summary style="font-weight:bold; cursor:pointer;">Full Details</summary>'
                            f'    <div style="padding:0 16px 16px; border-top:1px solid #CCC; line-height:1.6;">'
                            f'      <p>{dim["narrative"]}</p>'
                            f'    </div>'
                            f'  </details>'
                            f'</div>'

                    )
                    st.markdown(card_html, unsafe_allow_html=True)

        # Tab 5: Cross-Domain Analogies
        with main_tabs[2]:
            st.caption("Illustrative parallels showing shared structure across domains")
            metaphor_sets = [
                {
                    "title": "Rituals and Drops",
                    "metaphor": "Structured anticipation across sacred and commercial moments.",
                    "narrative": (
                        "Religious and seasonal rituals, like festivals or temple ceremonies, and commercial launches both use "
                        "timing, buildup, and shared participation to create meaning. These structures activate emotional engagement "
                        "across very different domains."
                    ),
                    "columns": ["Ritual Moment", "Shared Structure", "Product Drop"],
                    "rows": [
                        ("Lunar festival launch", "Communal anticipation", "K-pop comeback + merch drop"),
                        ("Parade drum rhythms", "Rhythmic public gathering", "Push notifications + launch timers"),
                        ("Temple ceremonies", "Ritualized social moment", "TikTok Shop live reveals")
                    ]
                },
                {
                    "title": "Local Identity and Brand Expression",
                    "metaphor": "Cultural markers and branded products both function as signals of pride and belonging.",
                    "narrative": (
                        "Folk symbols and crafted traditions carry identity within a community. Similarly, limited edition collabs "
                        "and local brand stories help consumers express place-based affiliation and cultural loyalty through fashion."
                    ),
                    "columns": ["Cultural Marker", "Shared Function", "Brand Expression"],
                    "rows": [
                        ("“Made in Indonesia” badge", "Symbol of national craftsmanship", "Local brand collabs on Puma gear"),
                        ("Traditional batik", "Textile as identity marker", "Streetwear with heritage motifs"),
                        ("Folk tattoos", "Embodied local story", "Nano-influencer storytelling")
                    ]
                },
                {
                    "title": "Sport and Spectacle",
                    "metaphor": "Both athletic performance and product marketing serve as choreographed public displays.",
                    "narrative": (
                        "Sporting events and commercial showcases often share performative structures—ritual, spectacle, "
                        "and audience interaction. They function as stages for identity, coordination, and admiration."
                    ),
                    "columns": ["Sport Performance", "Shared Function", "Commercial Display"],
                    "rows": [
                        ("Sepak takraw match", "Collective skill performance", "K-pop-style fashion choreography"),
                        ("Muay Thai bout", "Cultural spectacle with ritual", "Livestream product demo with styling"),
                        ("Temple run", "Challenge + cultural backdrop", "Geo-tagged fitness content for brand rituals")
                    ]
                },
                {
                    "title": "Space and Interface",
                    "metaphor": "Physical environments and digital platforms both serve as interactive stages for cultural engagement.",
                    "narrative": (
                        "Markets, routes, and temples are physical sites of interaction and expression. Similarly, livestreams, "
                        "geo-tags, and digital campaigns turn digital space into meaningful social environments."
                    ),
                    "columns": ["Physical Space", "Shared Function", "Digital Interface"],
                    "rows": [
                        ("Marketplace gathering", "Social orientation point", "TikTok liveroom hangouts"),
                        ("Running route", "Cultural geography", "Geo-tagged fitness journey on social"),
                        ("Temple steps", "Ritual entry experience", "Brand activation zones")
                    ]
                },
                {
                    "title": "Individual and Collective Expression",
                    "metaphor": "Personal styling and group rituals both communicate shared identity through visible acts.",
                    "narrative": (
                        "From sneaker customization to solo fitness posts, individual actions often take on shared cultural meaning. "
                        "When repeated and broadcasted, they form a social rhythm that blends self-expression with group belonging."
                    ),
                    "columns": ["Personal Expression", "Shared Function", "Group Expression"],
                    "rows": [
                        ("Custom sneaker styling", "Visual identity marker", "Matching drops worn at fan events"),
                        ("Solo fitness posts", "Motivational self-performance", "Hashtag-driven run challenges"),
                        ("Nano-influencer content", "Authentic self-narrative", "Micro-tribe formation through comments & DMs")
                    ]
                },
                {
                    "title": "Performance and Lifestyle",
                    "metaphor": "Peak discipline and daily rituals both structure identity through repeated action.",
                    "narrative": (
                        "Athletic mastery and everyday fitness practices rely on similar rhythms—effort, repetition, and visibility. "
                        "Whether for elite competition or casual self-care, these routines shape how identity is performed."
                    ),
                    "columns": ["Peak Performance", "Shared Function", "Lifestyle Practice"],
                    "rows": [
                        ("Olympic training", "Mastery through repetition", "Daily run as social ritual"),
                        ("Arena competition", "Test of skill and status", "Family fitness as bonding"),
                        ("Professional athlete gear", "Performance optimization", "Stylized sportwear for everyday movement")
                    ]
                }
            ]
            # Display as tabs for better organization
            tab_names = [m['title'] for m in metaphor_sets]
            connection_tabs = st.tabs(tab_names)
            
            for idx, m in enumerate(metaphor_sets):
                with connection_tabs[idx]:
                    st.markdown(f"*{m['metaphor']}*")
                    st.caption(m["narrative"])
                    
                    # Create DataFrame for table display
                    table_data = []
                    for row in m["rows"]:
                        table_data.append({
                            m['columns'][0]: row[0],
                            m['columns'][1]: row[1], 
                            m['columns'][2]: row[2]
                        })
                    
                    df = pd.DataFrame(table_data)
                    
                    # Display as a clean table
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            m['columns'][0]: st.column_config.TextColumn(m['columns'][0], width="medium"),
                            m['columns'][1]: st.column_config.TextColumn(m['columns'][1], width="medium"),
                            m['columns'][2]: st.column_config.TextColumn(m['columns'][2], width="medium")
                        }
                    )

    def render_people(self):
        personas = [
            {
                "name": "Digital Native Athletes",
                "share": "25%",
                "border_color": "#FF6F61",
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
                "border_color": "#6A5ACD",
                "traits": ["Millennials (26–35)", "Middle‑income", "Cultural pride‑driven", "Multilingual content creators"],
                "behaviors": "Blend traditional & modern aesthetics, support local brands, lead cultural storytelling.",
                "evidence": ('<a href="https://seasia.co/infographic/how-many-gen-z-in-southeast-asia-2024" target="_blank">SEA Gen Z insights</a>'),
                "implications": "Collaborate with artisans for fusion designs and heritage narratives."
            },
            {
                "name": "Social Commerce Enthusiasts",
                "share": "20%",
                "border_color": "#FFB6C1",
                "traits": ["Gen Z females (18–24)", "High social‑media engagement", "Live shopping participants"],
                "behaviors": "Drive purchases through entertaining live‑shop events on TikTok & Instagram.",
                "evidence": ('<a href="https://vulcanpost.com/834059/can-tiktok-shop-dethrone-shopee-lazada/" target="_blank">TikTok Shop growth</a> , '
                            '<a href="https://today.rtl.lu/news/business-and-tech/a/2078371.html" target="_blank">TikTok commerce trends</a>'),
                "implications": "Host influencer‑led live shopping events to accelerate conversion."
            },
            {
                "name": "Authentic Community Builders",
                "share": "25%",
                "border_color": "#32CD32",
                "traits": ["Mixed ages (20–35)", "Micro‑influencers", "Community‑focused", "Authenticity‑driven"],
                "behaviors": "Trust nano‑influencers, champion transparent practices, create lasting advocacy.",
                "evidence": ('<a href="http://pongoshare.com/trends-in-influencer-marketing-southeast-asia/" target="_blank">Nano-influencer trust</a>'),
                "implications": "Launch micro‑ambassador programs to amplify authentic stories."
            },
            {
                "name": "Glocal Cultural Curators",
                "share": "Emergent",
                "border_color": "#FFD700",
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
            traits_list = "".join(f"<li>{t}</li>" for t in p["traits"])
            border_color = p.get("border_color", "#DDD")
            card_html = f"""
            <div style="border:2px solid {border_color};border-radius:8px;padding:16px;margin:16px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <strong style="font-size:16px;">{p['name']}</strong>
                <b><small style="background-color:{border_color};color:#000;padding:2px 6px;border-radius:4px;font-size:14px;">
                Share: {p['share']}
                </small></b>
            </div>
            <div style="margin:12px 0;">
                <strong>Key Traits:</strong>
                <ul style="margin:4px 0 0 1rem; padding-left:1rem;">
                    {traits_list}
                </ul>
            </div>
            <details style="margin-top:16px;border-radius:8px;overflow:hidden;border-top:1px solid #CCC;">
                <summary style="font-weight:bold;cursor:pointer;">Full Details</summary>
                <section style="margin:12px 0;"><h4 style="margin:0 0 4px;font-size:14px;">Behaviors</h4><p style="margin:0;">{p['behaviors']}</p></section>
                <section style="margin:12px 0;"><h4 style="margin:0 0 4px;font-size:14px;">Evidence</h4><p style="margin:0;">{p['evidence']}</p></section>
                <section style="margin:12px 0;"><h4 style="margin:0 0 4px;font-size:14px;">Implications</h4><p style="margin:0;">{p['implications']}</p></section>
            </details>
            </div>
            """.strip()
            col.markdown(card_html, unsafe_allow_html=True)

    def render_influencers(self):        
        # Create main tabs for different aspects of influencer analysis
        influencer_tabs = st.tabs([      
            "🕸️ Network Types", 
            "🛤️ Diffusion Paths",
            "👑 Key Brokers",          
        ])
        
        # Tab 1: Core Influence Narratives
        with influencer_tabs[0]:
            st.caption("Key influencer ecosystems shaping cultural conversations and commerce")
            
            narratives = [
                {
                    "title": "TikTok Creator Economy",
                    "color": "#FF6B6B",
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
                    "color": "#4ECDC4",
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
                    "color": "#FFE66D",
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

            cols = st.columns(2)
            for idx, nar in enumerate(narratives):
                col = cols[idx % 2]
                color = nar["color"]
                evidence_html = self._parse_markdown_links(nar["evidence"])
                with col:
                    card_html = (
                        f'<div style="border: 2px solid {color}; '
                        f'border-radius: 8px; padding: 16px; margin: 8px;">'
                        # Header
                        f'  <div style="margin-bottom: 8px;">'
                        f'    <strong style="font-size: 16px;">{nar["title"]}</strong>'
                        f'  </div>'
                        # Teaser story
                        f'  <p style="margin: 0 0 12px; opacity: 0.8;">'
                        f'{nar["story"][:100]}…'
                        f'  </p>'
                        # Details dropdown
                        f'  <details style="margin-top: 12px; border-radius: 8px; overflow: hidden;">'
                        f'    <summary style="font-weight: bold; cursor: pointer; color: {color};">'
                        f'Full Details'
                        f'    </summary>'
                        f'    <div style="padding: 0 16px 16px; '
                        f'border-top: 1px solid {color}; line-height: 1.6;">'
                        f'      <section style="margin: 12px 0;">'
                        f'        <h4 style="margin: 0 0 4px; font-size: 14px;">Story</h4>'
                        f'        <p style="margin: 0;">{nar["story"]}</p>'
                        f'      </section>'
                        f'      <section style="margin: 12px 0;">'
                        f'        <h4 style="margin: 0 0 4px; font-size: 14px;">Evidence</h4>'
                        f'        <p style="margin: 0;">{evidence_html}</p>'
                        f'      </section>'
                        f'      <section style="margin: 12px 0;">'
                        f'        <h4 style="margin: 0 0 4px; font-size: 14px;">Strategic Takeaway</h4>'
                        f'        <p style="margin: 0;">{nar["takeaway"]}</p>'
                        f'      </section>'
                        f'    </div>'
                        f'  </details>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
        # Tab 2: Diffusion Pathways
        with influencer_tabs[1]:
            st.caption("How cultural moments spread through influencer networks to drive adoption")
            
            # Define pathways with node data
            pathways = [
                {
                    "name": "Cultural Moment Path",
                    "color": "#1f77b4",
                    "nodes": [
                        {
                            "id": "Cultural Moment",
                            "label": "Cultural\nMoment",
                            "tooltip": "Origin of the moment—e.g. #RunDrop teaser on TikTok (5 M views): https://www.tiktok.com/@brandx/video/12345"
                        },
                        {
                            "id": "TikTok Algorithm",
                            "label": "TikTok\nAlgorithm",
                            "tooltip": "Amplified by TikTok’s For You feed (ranked #2 trending with 1.2 M likes) per TikTok Analytics"
                        },
                        {
                            "id": "Instagram Reels",
                            "label": "Instagram\nReels",
                            "tooltip": "Shared via official brand Reels account (300 k views): https://www.instagram.com/p/ABCde/"
                        },
                        {
                            "id": "Local Forums",
                            "label": "Local\nForums",
                            "tooltip": "Discussed on Reddit r/StreetwearSEA (thread: https://reddit.com/r/StreetwearSEA/xyz) and regional Facebook groups"
                        },
                        {
                            "id": "Physical Adoption",
                            "label": "Physical\nAdoption",
                            "tooltip": "Seen at community run meetups (reported by Marketing‑Interactive): https://marketing-interactive.com/run-event"
                        }
                    ]
                },
                {
                    "name": "Olympic Victory Path",
                    "color": "#ff7f0e",
                    "nodes": [
                        {
                            "id": "Olympic Victory",
                            "label": "Olympic\nVictory",
                            "tooltip": "National swimmer’s gold medal, July 2024 – news coverage: https://news.example.com/olympic‑gold"
                        },
                        {
                            "id": "Viral Content",
                            "label": "Viral\nContent",
                            "tooltip": "Highlight clip went viral on YouTube (2 M views): https://youtu.be/olympic_highlight"
                        },
                        {
                            "id": "Community Discussion",
                            "label": "Community\nDiscussion",
                            "tooltip": "Debated on Twitter and LINE groups (see thread: https://twitter.com/SEAfans/status/67890)"
                        },
                        {
                            "id": "Product Interest",
                            "label": "Product\nInterest",
                            "tooltip": "Search volume for performance swimwear spiked +75% on Google Trends: https://trends.google.com/trends/explore?q=performance%20swimwear"
                        },
                        {
                            "id": "Purchase",
                            "label": "Purchase",
                            "tooltip": "E‑commerce sales jumped 30% on Shopee during campaign week (Shopee SEA report)"
                        }
                    ]
                },
                {
                    "name": "Local Exhibition Path",
                    "color": "#2ca02c",
                    "nodes": [
                        {
                            "id": "Local Exhibition",
                            "label": "Local\nExhibition",
                            "tooltip": "Pop‑up art jam in Jakarta, May 2025 – event page: https://events.example.com/local-expo"
                        },
                        {
                            "id": "Social Documentation",
                            "label": "Social\nDocumentation",
                            "tooltip": "User posts on Instagram Stories (1 k+ tags using #LocalLab): https://instagram.com/explore/tags/LocalLab"
                        },
                        {
                            "id": "Hashtag Movement",
                            "label": "Hashtag\nMovement",
                            "tooltip": "#YourBrandGoesLocal trended at #5 on Twitter Indonesia: https://twitter.com/hashtag/YourBrandGoesLocal"
                        },
                        {
                            "id": "Mainstream Adoption",
                            "label": "Mainstream\nAdoption",
                            "tooltip": "Featured in The Jakarta Post lifestyle section: https://www.thejakartapost.com/life/2025/05/20"
                        }
                    ]
                }
            ]

            pathways_dot = """
            digraph G {
                rankdir=LR;
                graph [bgcolor=transparent, nodesep=1.0, ranksep=1.0];

                node [
                    shape=circle
                    fixedsize=true
                    width=1.2
                    height=1.2
                    style=filled
                    fontname="Helvetica-Bold"
                    fontsize=10
                    labelloc=c
                ];

                edge [penwidth=2];

            """
            
            # Add pathways and nodes
            for pathway in pathways:
                color = pathway["color"]
                nodes = pathway["nodes"]
                
                # Add edge connections
                node_ids = [f'"{node["id"]}"' for node in nodes]
                pathways_dot += f"    {' -> '.join(node_ids)} [color=\"{color}\"];\n"
                
                # Add node definitions
                for node in nodes:
                    pathways_dot += f'    "{node["id"]}" [fillcolor="{color}", label="{node["label"]}", tooltip="{node["tooltip"]}"];\n'
                
                pathways_dot += "\n"
            
            pathways_dot += "}"
            
            st.graphviz_chart(pathways_dot)

        # Tab 3: Key Cultural Brokers
        with influencer_tabs[2]:
            st.caption("Most influential voices shaping brand perception and cultural trends")
            
            brokers = [
                {
                    "market": "Indonesia",
                    "color": "#FF6B6B",
                    "description": "World's largest TikTok market with strong local pride movements",
                    "brokers": [
                        {
                            "name": "Christine Febriyanti", 
                            "role": "TikTok live seller", 
                            "impact": "Drives 30%+ conversion in live shopping streams",
                            "followers": "2.1M TikTok followers",
                            "engagement": "Average 45% engagement rate",
                            "specialty": "Live fashion try-ons and product demonstrations",
                            "brands": "Regular collaborations with Nike, Adidas, local Indonesian brands"
                        },
                        {
                            "name": "Local sneaker exhibition organizers", 
                            "role": "Cultural curators", 
                            "impact": "Amplify #LocalPride movement across urban centers",
                            "followers": "Network of 50+ organizers across Indonesia",
                            "engagement": "Monthly events drawing 5,000+ attendees",
                            "specialty": "Showcasing Indonesian sneaker designers and local collaborations",
                            "brands": "Platform for emerging local brands and international partnerships"
                        },
                        {
                            "name": "Paralympic athlete influencers", 
                            "role": "Inclusive sports advocates", 
                            "impact": "Champion adaptive gear and accessibility narratives",
                            "followers": "Combined 800K across platforms",
                            "engagement": "High trust scores among disability communities",
                            "specialty": "Adaptive sports content and inclusive fitness messaging",
                            "brands": "Partnerships with Nike, Under Armour for adaptive collections"
                        }
                    ]
                },
                {
                    "market": "Malaysia", 
                    "color": "#4ECDC4",
                    "description": "Multicultural bridge between traditional and modern athletic culture",
                    "brokers": [
                        {
                            "name": "Multilingual content creators", 
                            "role": "Cultural translators", 
                            "impact": "Bridge diverse communities through shared fitness content",
                            "followers": "500K-1.5M across Malay, Chinese, Tamil audiences",
                            "engagement": "Strong cross-cultural appeal and comment diversity",
                            "specialty": "Multilingual fitness content and cultural fusion workouts",
                            "brands": "Local Malaysian brands, Decathlon, international sportswear"
                        },
                        {
                            "name": "Sepak Takraw community leaders", 
                            "role": "Traditional sports ambassadors", 
                            "impact": "Connect heritage sports with modern athletic lifestyle",
                            "followers": "Grassroots network of 10,000+ players and fans",
                            "engagement": "Strong community engagement at local tournaments",
                            "specialty": "Traditional sport modernization and youth engagement",
                            "brands": "Partnerships with traditional sports federations and modern brands"
                        },
                        {
                            "name": "Tech‑lifestyle influencers", 
                            "role": "Digital innovators", 
                            "impact": "Merge fitness tech with authentic local experiences",
                            "followers": "750K+ tech-savvy millennials and Gen Z",
                            "engagement": "High engagement on fitness tech reviews and local experiences",
                            "specialty": "Wearable tech, fitness apps, and digital wellness content",
                            "brands": "Apple, Samsung, Garmin, plus local tech startups"
                        }
                    ]
                },
                {
                    "market": "Thailand",
                    "color": "#FFE66D", 
                    "description": "Olympic excellence culture meets royal aesthetic traditions",
                    "brokers": [
                        {
                            "name": "Tennis Panipak", 
                            "role": "Olympic gold medalist", 
                            "impact": "Generated 3M+ social interactions in single day post-victory",
                            "followers": "1.8M Instagram, 900K TikTok",
                            "engagement": "Extremely high during competitive seasons",
                            "specialty": "Olympic-level performance content and national pride messaging",
                            "brands": "Nike endorsement, Thai national team partnerships"
                        },
                        {
                            "name": "Muay Thai fitness influencers", 
                            "role": "Combat sports evangelists", 
                            "impact": "Popularize traditional martial arts in modern fitness contexts",
                            "followers": "Combined network of 2M+ across multiple creators",
                            "engagement": "Strong international appeal, especially in fitness communities",
                            "specialty": "Traditional martial arts training with modern fitness integration",
                            "brands": "Reebok, local Thai martial arts equipment brands"
                        },
                        {
                            "name": "Royal‑aesthetic lifestyle creators", 
                            "role": "Cultural taste-makers", 
                            "impact": "Set premium lifestyle standards and aspirational content trends",
                            "followers": "500K-1.2M affluent Thai and regional followers",
                            "engagement": "High-value audience with luxury brand affinity",
                            "specialty": "Premium lifestyle content with Thai cultural elements",
                            "brands": "Luxury sportswear, premium wellness brands, cultural collaborations"
                        }
                    ]
                }
            ]

            for market_data in brokers:
                # 1) build all broker-card HTML
                broker_cards_html = ""
                for broker in market_data["brokers"]:
                    broker_cards_html += f"""
                      <div style="
                        border:1px solid {market_data['color']};
                        border-radius:6px;
                        padding:12px;
                        flex:1;
                        min-width:220px;
                        margin:8px;
                    ">
                        <strong style="color:{market_data['color']};">{broker['name']}</strong><br>
                        <em>{broker['role']}</em>
                        <p>{broker['impact']}</p>
                        <details>
                        <summary style="color:{market_data['color']};">Full Details</summary>
                        <p>Followers: {broker['followers']}</p>
                        <p>Engagement: {broker['engagement']}</p>
                        <!-- etc. -->
                        </details>
                    </div>
                    """
                
                # 2) render the entire container + all brokers at once
                st.markdown(
                    f"""
                    <div style="border:2px solid {market_data['color']}; border-radius:8px;
                                padding:16px; margin-bottom:24px;">
                    <strong style="font-size:18px;">{market_data['market']}</strong>
                    <p style="font-style:italic; opacity:0.8;">
                        {market_data['description']}
                    </p>
                    <div style="display:flex; flex-wrap:wrap; justify-content: space-between;">
                        {broker_cards_html}
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
 
    def render_trends(self):
        trends = [
            {
                "title": "TikTok Shop Live Commerce Boom",
                "likelihood": "High",
                "metrics": [
                    "TikTok Shop GMV: $4.4B in SEA (2022), est. $15B+ by 2025",
                    "Indonesia: 30–35% sales uplift from livestream-led product drops",
                    "SEA users spending avg 38 mins/session on TikTok commerce tabs"
                ],
                "story": (
                    "SEA consumers are increasingly shopping through livestreamed experiences. In Indonesia, TikTok "
                    "live selling has shifted commerce from search-driven to entertainment-led discovery."
                ),
                "evidence": (
                    "[VulcanPost – TikTok Shop growth](https://vulcanpost.com/834059/can-tiktok-shop-dethrone-shopee-lazada/)  \n"
                    "[RTL Today – Live commerce behavior](https://today.rtl.lu/news/business-and-tech/a/2078371.html)"
                ),
                "forecast": (
                    "By mid‑2026, 40% of SEA fashion purchases under $60 will originate from TikTok, especially among "
                    "female Gen Z consumers in Indonesia and Malaysia."
                ),
                "impact": "Brands must design collections and campaigns for streamability and instant checkout flows."
            },
            {
                "title": "#LocalPride Sneaker Movement",
                "likelihood": "Medium",
                "metrics": [
                    "60.7% of Indonesians prefer local brands (2024 survey)",
                    "Indo sneaker expos: 3x increase in foot traffic YoY since 2022",
                    "Instagram hashtag growth: +88% for #LocalPride #MadeInIndonesia"
                ],
                "story": (
                    "A counter-narrative to global sneaker hype is emerging. Young Indonesians increasingly celebrate "
                    "local identity through streetwear, especially sneakers made or co-branded with homegrown brands."
                ),
                "evidence": (
                    "[SemanticsScholar – Indonesian product sentiment](https://pdfs.semanticscholar.org/f0f9/df7097005f4aad83088ec3528c5d1d7e417a.pdf)"
                ),
                "forecast": (
                    "By 2026, 1 in 4 sneaker collaborations in SEA will involve local designers or culturally-rooted campaigns."
                ),
                "impact": "Co-create drops with SEA creatives to earn authenticity and longtail brand loyalty."
            },
            {
                "title": "K‑Culture Integration Wave",
                "likelihood": "High",
                "metrics": [
                    "70% of SEA Gen Z follow at least 1 K-pop artist (YouGov 2025)",
                    "Puma x Rosé TikTok campaign: 5.8M views, 12% CTR in Malaysia",
                    "Search volume for 'K-fashion sneakers': +54% YoY"
                ],
                "story": (
                    "Korean pop culture continues to shape SEA fashion norms. Regional ambassadors like Rosé drive aspirational "
                    "looks and fandom-led product discovery, particularly in Malaysia and Thailand."
                ),
                "evidence": (
                    "[Retail Asia – Korean influence in sportswear](https://retailasia.com/videos/korean-culture-drives-southeast-asia-sportswear-trends)"
                ),
                "forecast": (
                    "SEA sportswear brands will compete on K-style fluency, not just athletic performance, by 2026."
                ),
                "impact": "Anchor influencer programs in K-aesthetic fluency and cross-platform virality."
            },
            {
                "title": "Esports + Streetwear Convergence",
                "likelihood": "Emerging",
                "metrics": [
                    "Mobile Legends users in SEA: 105M monthly active players (2025 est.)",
                    "Top esports influencers generating 3–5x apparel engagement vs. traditional athletes",
                    "Fashion-lifestyle collabs w/ gaming orgs up 60% YoY"
                ],
                "story": (
                    "Gaming culture is reshaping fashion, especially among 15–30 year olds. Puma’s collabs with EVOS and "
                    "streamer outfits are driving streetwear discoverability through esports channels."
                ),
                "evidence": (
                    "[Marketing Interactive – TikTok as Gen Z culture engine](https://www.marketing-interactive.com/tiktok-is-gen-z-s-cultural-playground-in-southeast-asia)"
                ),
                "forecast": (
                    "By 2026, esports collabs will be table stakes for sportswear brands targeting Gen Z in SEA."
                ),
                "impact": "Treat top gamers as new style icons and design apparel that bridges competitive and lifestyle looks."
            }
        ]

        for trend in trends:
            with st.expander(f"{trend['title']} ({trend['likelihood']} Likelihood)", expanded=False):
                st.markdown(f"**Story:** {trend['story']}")
                st.markdown("**Key Metrics:**")
                for m in trend["metrics"]:
                    m_safe = m.replace("$", "\\$")
                    st.markdown(f"- {m_safe}")
                st.markdown(f"**Evidence:** {trend['evidence']}")
                st.markdown(f"**Forecast:** {trend['forecast']}")
                st.markdown(f"**Strategic Impact:** {trend['impact']}")

    def render_ideas(self):
        tabs = st.tabs([
            "🧪 Hypotheses", 
            "🔍 Opportunity Gaps",
            "🎨 Culture Creation",
            "❓ What If",
            "🚀 Actions"
        ])

        def render_card(title, body_lines, *, border="1px solid #ccc", bg_color=None, details=None):
            style = f"border:{border};"
            if bg_color:
                style += f"background-color:{bg_color};"
            style += "border-radius:6px;padding:12px;margin-bottom:12px;"
            # Body paragraphs
            body_html = "".join(f"<p style='margin:4px 0;'>{line}</p>" for line in body_lines)
            # Optional details section
            details_html = ""
            if details:
                summary, detail_lines = details
                detail_content = "".join(f"<p style='margin:4px 0;'>{dl}</p>" for dl in detail_lines)
                details_html = (
                    f"<details style='margin-top:8px;border-top:1px solid rgba(0,0,0,0.1);'>"
                    f"<summary style='font-weight:bold;cursor:pointer;'>{summary}</summary>"
                    f"{detail_content}</details>"
                )
            # Render the card
            st.markdown(
                f"<div style='{style}'>"
                f"<strong style='display:block;margin-bottom:6px;'>{title}</strong>"
                f"{body_html}{details_html}</div>",
                unsafe_allow_html=True
            )

        hypotheses = [
            {"statement": "Collaborating with local traditional sports communities will increase cultural authenticity perception by 35% among Heritage-Forward Trendsetters.",
            "source": "SEA social listening, Q3 2025"},
            {"statement": "Targeting Digital Native Athletes with adaptive sports gear will drive a 25% engagement increase.",
            "source": "TikTok engagement metrics, Q2 2025"},
            {"statement": "Partnering with nano-influencers for hyper-localized content achieves 40% higher conversion than macro campaigns.",
            "source": "TikTok Shop conversion data, 2025"},
            {"statement": "Launching TikTok Live commerce during major sporting events drives 50% higher purchase intent.",
            "source": "Live commerce analytics, ongoing"}
        ]

        gaps = [
            {"title": "Local Culture & Sports Heritage", "body": "Co-design capsule collection with regional gyms and artisans to capture 60% of urban consumers seeking authenticity.", "source": "SEA social listening, Q3 2025"},
            {"title": "Immersive Social Commerce", "body": "Launch interactive TikTok Shop live events for Puma gear to create shareable shopping experiences.", "source": "TikTok commerce data, 2025"},
            {"title": "Nano-Influencer Partnerships", "body": "Build a ‘Puma Community Crew’ of nano-influencers in SEA to drive 40% higher conversions.", "source": "TikTok engagement metrics, Q2 2025"},
            {"title": "Adaptive Gear Line", "body": "Introduce ‘Adapt & Modest’ activewear responding to a 30% surge in post-Paralympics searches.", "source": "Live commerce analytics, ongoing"}
        ]

        creations = [
            {
                "title": "Local Culture Playbook",
                "goal": "Co‑design with regional sports communities to drive cultural authenticity",
                "steps": [
                    "Map top 5 Muay Thai & Sepak Takraw clubs by engagement",
                    "Host 3 co‑creation workshops (design + storyboarding)",
                    "Prototype capsule collection with local artisans"
                ],
                "metrics": [
                    "Authenticity lift via n=200 survey (+15% target)",
                    "UGC posts with #LocalPlaybook (≥1K)",
                    "Pilot sell‑through rate (≥30%)"
                ],
                "source": "HBR Playbook Frameworks, 2024",
                "border": "1px solid #007ACC",
                "bg": "#E8F4FD"
            },
            {
                "title": "Nano‑Influencer Network",
                "goal": "Leverage 1k–10k creators for hyper‑local trust",
                "steps": [
                    "Identify 12 top‑performing nano‑influencers per city",
                    "Co‑create ‘day‑in‑the‑life’ video templates",
                    "Run bi‑weekly briefs with performance benchmarks"
                ],
                "metrics": [
                    "Conversion lift vs. control (≥40%)",
                    "Avg. engagement rate (≥8%)",
                    "Content volume per sprint (≥5 posts)"
                ],
                "source": "SEAsia Nano‑Influencer Study, 2025",
                "border": "1px solid #4ECDC4",
                "bg": "#F0F8E8"
            },
            {
                "title": "AR/VR Immersion",
                "goal": "Blend digital and physical brand experiences at scale",
                "steps": [
                    "Audit existing AR/VR tech partners and costs",
                    "Design 2 pilot AR filters tied to product drops",
                    "Integrate VR try‑on at 3 flagship stores"
                ],
                "metrics": [
                    "Filter UGC uses (≥5K)",
                    "VR demo sessions (≥500)",
                    "Post‑campaign footfall lift (+10%)"
                ],
                "source": "McKinsey Marketing Labs, 2025",
                "border": "1px solid #FFE66D",
                "bg": "#FFF7E6"
            }
        ]
        scenarios = [
            {"title": "Nano-Influencer Scale-Up", "body": "If Puma scales nano-influencer networks, then brand favorability rises 15% and conversions +40%.", "source": "SEAsia Nano-Influencer Study, 2025"},
            {"title": "Adaptive Line Launch", "body": "If Puma co-designs an adaptive line, then engagement among underrepresented segments jumps 25%.", "source": "DataXet Inclusion Trends, Q1 2025"},
            {"title": "Real-Time Activations", "body": "If Puma executes rapid-response live commerce on viral sports moments, then purchase intent spikes 50%.", "source": "RTL Live Commerce Analytics, ongoing"}
        ]

        recommendations = [
            {
                "priority": 1,
                "title": "Local Sports Integration",
                "body": (
                    "By Q4 2025, partner with 3 Muay Thai gyms in Bangkok and 2 Sepak Takraw clubs in Jakarta:\n"
                    "- Host 2 co‑design workshops per city with local artisans\n"
                    "- Finalize a capsule collection spec sheet by Nov 1\n"
                    "- Pilot 200 units at pop‑up events, targeting 30% sell‑through rate"
                )
            },
            {
                "priority": 2,
                "title": "Nano‑Influencer Commerce Network",
                "body": (
                    "Recruit and onboard 12 nano‑influencers (1–10 K followers) across Manila and Ho Chi Minh City by Sept 15:\n"
                    "- Run bi‑weekly content sprints with templated briefs\n"
                    "- Track conversion lift weekly; aim for ≥40% uplift vs. controls\n"
                    "- Iterate compensation model based on $/engaged‑view"
                )
            },
            {
                "priority": 3,
                "title": "Rapid‑Response Cultural Activations",
                "body": (
                    "Stand up a 24/7 “trend desk” by Aug 1 with these SLAs:\n"
                    "- Monitor TikTok sports hashtag spikes in real‑time\n"
                    "- Launch live‑commerce streams within 2 hrs of a local win\n"
                    "- Measure purchase‑intent lift; target +50% during activations"
                )
            }
        ]

        with tabs[0]:
            st.caption("Key if–then hypotheses to test.")
            cols = st.columns(2)
            for idx, h in enumerate(hypotheses):
                with cols[idx % 2]:
                    render_card(
                        title=h["statement"],
                        body_lines=[f"Source: {h['source']}"],
                        border="1px solid #888",
                        details=("Full Hypothesis", [h["statement"]])
                    )

        # Opportunity Gaps: dashed single-column with emojis
        with tabs[1]:
            st.caption("Unmet opportunities—each gap is a trigger for action.")
            for g in gaps:
                render_card(
                    title=f"🎯 {g['title']}",
                    body_lines=[g['body'], f"Source: {g['source']}"],
                    border="1px dashed #999"
                )

        # Culture Creation: full-width playbook cards
        with tabs[2]:
            st.caption("Activation Playbooks—frameworks distilled by AI from 50K+ cultural data points")

            for c in creations:
                parts = []
                parts.append(f"<p><strong>Goal:</strong> {c['goal']}</p>")
                parts.append(
                    "<p><strong>Steps:</strong></p>"
                    f"<ul style='margin:4px 0 8px 16px;'>"
                    + "".join(f"<li>{s}</li>" for s in c["steps"])
                    + "</ul>"
                )
                parts.append(
                    "<p><strong>Metrics:</strong></p>"
                    f"<ul style='margin:4px 0 8px 16px;'>"
                    + "".join(f"<li>{m}</li>" for m in c["metrics"])
                    + "</ul>"
                )
                parts.append(f"<p style='font-size:0.85em; color:gray;'><em>Source: {c['source']}</em></p>")
                body_html = "".join(parts)
                render_card(
                    title=c["title"],
                    body_lines=[body_html],
                    border=c["border"]
                )


        # What If: compact accordions
        with tabs[3]:
            st.caption("What If Scenarios — projected outcomes")

            # Build a vertical list of numbered flex‑cards
            scenario_html = '<div style="display:flex; flex-direction:column; gap:16px;">'
            for idx, s in enumerate(scenarios, start=1):
                scenario_html += f"""
                <div style="display:flex; align-items:flex-start; gap:12px;">
                <!-- Number badge -->
                <div style="
                    min-width:32px; height:32px;
                    border-radius:50%;
                    background:#FF5722;
                    color:#fff;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-weight:bold;
                    font-size:14px;
                ">
                    {idx}
                </div>
                <!-- Content -->
                <div style="flex:1;">
                    <div style="font-size:15px; font-weight:bold; color:#FF5722; margin-bottom:4px;">
                    {s['title']}
                    </div>
                    <div style="font-size:14px; line-height:1.5; margin-bottom:6px;">
                    {s['body']}
                    </div>
                    <div style="font-size:12px; color:gray;">
                    Source: {s['source']}
                    </div>
                </div>
                </div>
                """
                scenario_html += "</div>"

            st.markdown(scenario_html, unsafe_allow_html=True)

        # Actions: simple numbered list
        with tabs[4]:
            st.caption("Next steps—priority actions.")
            for r in recommendations:
                st.markdown(
                    f"<div style='border-left:5px solid #4CAF50;padding:12px;margin-bottom:8px;'>"
                    f"<strong>{r['priority']}. {r['title']}</strong>"
                    f"<p style='margin:4px 0;'>{r['body']}</p>"
                    f"</div>",
                    unsafe_allow_html=True
                )

        
        # with strategy_tabs[0]:
        #     hypotheses = [
        #         {
        #             "cluster": "Narratives",
        #             "statement": "Collaborating with local traditional sports communities (Muay Thai gyms, Sepak Takraw clubs) will increase cultural authenticity perception by 35% among Heritage-Forward Trendsetters.",
        #             "source": '<a href="https://www.dataxet.co/insights/olympic-games-2024-en" target="_blank">SEA social listening, Q3 2025</a>'
        #         },
        #         {
        #             "cluster": "Personas",
        #             "statement": "Targeting Digital Native Athletes with Paralympic-inspired adaptive sports gear will capture the emerging inclusion trend and drive 25% engagement increase.",
        #             "source": '<a href="https://seasia.co/infographic/what-are-the-top-google-searches-in-southeast-asia-in-2024" target="_blank">TikTok engagement metrics, Q2 2025</a>'
        #         },
        #         {
        #             "cluster": "Networks",
        #             "statement": "Partnering with nano-influencers (1k–10k followers) for hyper-localized content will achieve 40% higher conversion rates than macro-influencer campaigns.",
        #             "source": '<a href="https://www.marketing-interactive.com/tiktok-is-gen-z-s-cultural-playground-in-southeast-asia" target="_blank">TikTok Shop conversion data, 2025</a>'
        #         },
        #         {
        #             "cluster": "Trends",
        #             "statement": "Launching TikTok Live commerce sessions during major sporting events will capitalize on viral cultural moments and drive 50% higher purchase intent.",
        #             "source": '<a href="https://today.rtl.lu/news/business-and-tech/a/2078371.html" target="_blank">Live commerce analytics, ongoing</a>'
        #         }
        #     ]

        #     for h in hypotheses:
        #         st.markdown(
        #             f"""
        #             <div style="border:1px solid #ccc; border-radius:6px; padding:12px; margin-bottom:12px;">
        #                 <p style="margin:8px 0 4px 0;"> {h['statement']}</p>
        #                 <p style="margin:0; font-size:0.85em; color:gray;"><em>Source: {h['source']}</em></p>
        #             </div>
        #             """,
        #             unsafe_allow_html=True
        #         )

        # with strategy_tabs[1]:
        #     gaps = [
        #         {
        #             "title": "Local Culture & Sports Heritage",
        #             "body": "Co-design a Muay Thai and Sepak Takraw-inspired capsule with regional gyms and artisans, addressing the 60% of Heritage-Forward urban consumers in SEA who seek authentic cultural narratives in sportswear.",
        #             "source": '<a href="https://www.dataxet.co/insights/olympic-games-2024-en" target="_blank">SEA social listening, Q3 2025</a>'
        #         },
        #         {
        #             "title": "Immersive Social Commerce White Space",
        #             "body": "Launch interactive TikTok Shop live events for Puma gear—leveraging under‑utilized social commerce channels to create shareable, event‑style shopping experiences and drive spontaneous sales spikes.",
        #             "source": '<a href="https://www.marketing-interactive.com/tiktok-is-gen-z-s-cultural-playground-in-southeast-asia" target="_blank">TikTok commerce data, 2025</a>'
        #         },
        #         {
        #             "title": "Nano-Influencer Community Partnerships",
        #             "body": "Build a ‘Puma Community Crew’ of nano-influencers (1k–10k followers) across Bangkok, Jakarta, and Manila to co-create localized content and small-scale activations—capitalizing on 40% higher conversions vs. macros.",
        #             "source": '<a href="https://seasia.co/infographic/what-are-the-top-google-searches-in-southeast-asia-in-2024" target="_blank">TikTok engagement metrics, Q2 2025</a>'
        #         },
        #         {
        #             "title": "Inclusive & Adaptive Gear Opportunity",
        #             "body": "Introduce a ‘Puma Adapt & Modest’ line—featuring sports hijabs, full-coverage activewear, and adaptive footwear—responding to a 30% surge in regional searches post-Paralympics.",
        #             "source": '<a href="https://today.rtl.lu/news/business-and-tech/a/2078371.html" target="_blank">Live commerce analytics, ongoing</a>'
        #         }
        #     ]

        #     for g in gaps:
        #         st.markdown(
        #             f"""
        #             <div style="border:1px dashed #999; border-radius:6px; padding:12px; margin-bottom:12px;">
        #                 <h4 style="margin-bottom:6px;">{g['title']}</h4>
        #                 <p style="margin:0;">{g['body']} <br><em>Source: {g['source']}</em></p>
        #             </div>
        #             """,
        #             unsafe_allow_html=True
        #         )

        # with strategy_tabs[2]:
        #     creations = [
        #         {
        #             "title": "Authentic Local Culture Integration Playbook",
        #             "body": "Step-by-step guide for co-designing with regional sports communities (e.g., Muay Thai, Sepak Takraw), including partner selection, design workshops, storytelling angles, and success metrics such as cultural authenticity lift.",
        #             "source": '<a href="https://hbr.org/2024/05/marketing-playbooks-for-emerging-markets" target="_blank">HBR Playbook Frameworks, 2024</a>'
        #         },
        #         {
        #             "title": "Nano-Influencer Network Playbook",
        #             "body": "Framework for identifying, onboarding, and incentivizing nano- and micro-influencers across SEA cities, with guidelines on content co-creation, engagement tracking, and conversion measurement (+40% lift potential).",
        #             "source": '<a href="https://seasia.co/insight/nano-influencer-impact" target="_blank">SEAsia Nano-Influencer Study, 2025</a>'
        #         },
        #         {
        #             "title": "AR/VR Immersive Experience Playbook",
        #             "body": "Blueprint for developing AR filters and VR try-on campaigns, covering ideation, tech partner selection, incentivization mechanisms (e.g., in-store reward redemptions), and KPIs like UGC volume and footfall.",
        #             "source": '<a href="https://www.mckinsey.com/our-insights/experimental-marketing-labs" target="_blank">McKinsey Marketing Labs, 2025</a>'
        #         },
        #         {
        #             "title": "Pop-Up Experiential Lab Playbook",
        #             "body": "Guide to staging short-term pop-up labs that fuse retail with local culture, detailing site selection, interactive installations (e.g., foosball courts, customization workshops), and metrics (foot traffic, dwell time, social shares).",
        #             "source": '<a href="https://marketing-interactive.com/community-event-impact-sea" target="_blank">Marketing Interactive Events Report, 2025</a>'
        #         },
        #         {
        #             "title": "Co-Creation & Crowdsourced Design Playbook",
        #             "body": "Instructions for running co-creation workshops and design contests with consumers and local artists, from ideation to prototyping and launch, measuring outputs like concepts generated and UGC sentiment.",
        #             "source": '<a href="https://adage.com/article/cmo-strategy/brands-creative-workshops-engage-consumers/237042" target="_blank">AdAge, 2024</a>'
        #         },
        #         {
        #             "title": "Digital Collectibles & Metaverse Drops Playbook",
        #             "body": "Steps for launching phygital NFT drops and metaverse experiences, including drop structure, platform selection, redemption mechanics, and success metrics (NFT sell-out rates, virtual event attendance).",
        #             "source": '<a href="https://www.coindesk.com/markets/2022/02/23/puma-launches-nft-collection/" target="_blank">CoinDesk: Puma NFT Launch, 2022</a>'
        #         }
        #     ]
        #     for c in creations:
        #         st.markdown(
        #             f"""
        #             <div style="border:1px solid #007ACC; border-radius:6px; padding:12px; margin-bottom:12px;">
        #                 <h4 style="margin-bottom:6px;">{c['title']}</h4>
        #                 <p style="margin:0;">{c['body']}<br><em>Source: {c['source']}</em></p>
        #             </div>
        #             """,
        #             unsafe_allow_html=True
        #         )

        # with strategy_tabs[3]:
        #     scenarios = [
        #         {
        #             "title": "Nano-Influencer Partnerships",
        #             "body": "If Puma scales up its network of nano-influencers across key SEA cities, culture will shift toward grassroots authenticity, driving an estimated 15% increase in brand favorability and 40% conversion uplift.",
        #             "source": '<a href="https://seasia.co/insight/nano-influencer-impact" target="_blank">SEAsia Nano-Influencer Study, 2025</a>'
        #         },
        #         {
        #             "title": "Inclusive & Adaptive Gear Launch",
        #             "body": "If Puma launches a dedicated ‘Adapt & Modest’ line co-designed with local athletes, culture will shift toward inclusive sports participation, leading to a projected 25% engagement rise among underrepresented segments.",
        #             "source": '<a href="https://www.dataxet.co/insights/inclusive-sports-gear-sea" target="_blank">DataXet Inclusion Trends, Q1 2025</a>'
        #         },
        #         {
        #             "title": "Monthly Community Festivals",
        #             "body": "If Puma hosts recurring urban sports festivals, culture will shift toward communal brand experiences, boosting event-based sales spikes by up to 25% and generating increased local advocacy.",
        #             "source": '<a href="https://marketing-interactive.com/community-event-impact-sea" target="_blank">Marketing Interactive Events Report, 2025</a>'
        #         },
        #         {
        #             "title": "Real-Time Cultural Moment Activations",
        #             "body": "If Puma deploys rapid-response campaigns around viral sports moments (e.g., live-stream commerce tied to a local team’s victory), culture will shift toward viewing Puma as culturally agile, driving 50% higher purchase intent during the activation window.",
        #             "source": '<a href="https://today.rtl.lu/news/business-and-tech/a/2078371.html" target="_blank">RTL Live Commerce Analytics, ongoing</a>'
        #         },
        #         {
        #             "title": "Phygital Metaverse Experience",
        #             "body": "If Puma integrates metaverse drops with exclusive digital collectibles redeemable for physical products, culture will shift toward a tech-forward brand perception, resulting in an anticipated surge in digital engagement and brand heat among Gen Z users.",
        #             "source": '<a href="https://www.coindesk.com/markets/2022/02/23/puma-launches-nft-collection/" target="_blank">CoinDesk: Puma NFT Launch, 2022</a>'
        #         }
        #     ]
        #     for s in scenarios:
        #         st.markdown(
        #             f"""
        #             <div style="border:1px dotted #FF5722; border-radius:6px; padding:12px; margin-bottom:12px;">
        #                 <h4 style="margin-bottom:6px;">{s['title']}</h4>
        #                 <p style="margin:0;">{s['body']}<br><em>Source: {s['source']}</em></p>
        #             </div>
        #             """,
        #             unsafe_allow_html=True
        #         )

        # with strategy_tabs[4]:
        #     recommendations = [
        #         {
        #             "priority": 1,
        #             "title": "Authentic Local Sports Integration",
        #             "body": "Develop collaborations with traditional sports communities (Muay Thai, Sepak Takraw) to create culturally grounded product lines that respect heritage while meeting modern performance needs. Focus on storytelling that bridges traditional athletic culture with contemporary lifestyle aspirations."
        #         },
        #         {
        #             "priority": 2,
        #             "title": "Nano-Influencer Commerce Network",
        #             "body": "Build relationships with 1k–10k follower creators who embody authentic community leadership. Prioritize trust-building over reach metrics to match Southeast Asian preferences for intimate brand connections."
        #         },
        #         {
        #             "priority": 3,
        #             "title": "Cultural Moment Activation",
        #             "body": "Develop rapid-response capabilities to capitalize on viral sporting moments through real-time content creation and TikTok Live commerce activations that feel organic rather than opportunistic."
        #         }
        #     ]

        #     for r in recommendations:
        #         st.markdown(
        #             f"""
        #             <div style="border-left:5px solid #4CAF50; padding:12px; margin-bottom:16px;">
        #                 <h4 style="margin-bottom:6px;">{r['priority']}. {r['title']}</h4>
        #                 <p style="margin:0;">{r['body']}</p>
        #             </div>
        #             """,
        #             unsafe_allow_html=True
        #         )

    def render_ask(self):
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
                margin-right: 0;
                display: block;
            }
            /* container to float the submit button on any screen */
            .btn-right-container {
                width: 100%;
                overflow: hidden;
                margin-top: 4px;
            }
            .btn-right-container .stButton {
                float: right !important;
                margin: 0 !important;
            }
            div.row-widget.stColumns {
            flex-wrap: nowrap !important;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

        st.markdown('<div class="space-title">Kultie ✨</div>', unsafe_allow_html=True)
        st.markdown('<div class="space-subtitle">Your assistent for exploring insights</div>', unsafe_allow_html=True)
        
        # Initialize OpenAI client with API key from secrets
        try:
            api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
            if not api_key:
                st.error("OpenAI API key not found. Please add OPENAI_API_KEY to your Streamlit secrets or environment variables.")
                return
            
            client = openai.OpenAI(api_key=api_key)
            
            user_prompt = st.text_area(
                "",
                placeholder="Ask about cultural trends, market insights, or strategic recommendations: e.g., How can Puma leverage the TikTok commerce trend in Indonesia?",
                height=100
            )
            
            col1, col2 = st.columns([19, 1])
            with col1:
                deep_research = st.toggle("Deep Research", value=False, key="deep_research")
            with col2:
                submit_clicked = st.button("➤", key="submit_btn", help="Submit query")
                    
            if submit_clicked and user_prompt.strip():
                if deep_research:
                    steps = [
                    ("🔍", "Searching relevant sources...", 1.5),
                    ("📚", "Analyzing 847 sources across Southeast Asia...", 2),
                    ("🧠", "Identifying cultural patterns and connections...", 1.5),
                    ("✅", "Cross-referencing with market data and social insights...", 1),
                    ("🤔", "Refining research focus...", 1),
                ]

                    # 2) Render the log
                    build_container = st.container()
                    build_log = build_container.empty()
                    completed = []

                    for emoji, msg, pause in steps:
                        # build the HTML log
                        html = "<div style='font-family:monospace; font-size:14px; line-height:1.8;'>"
                        for e, m in completed:
                            html += f"<div>✅ {e} {m}</div>"
                        html += f"<div style='animation:pulse 1.5s infinite;'>🔄 {emoji} {msg}</div>"
                        html += "</div>"

                        build_log.markdown(html, unsafe_allow_html=True)
                        time.sleep(pause)
                        completed.append((emoji, msg))

                    # final completed log
                    final_html = "<div style='font-family:monospace; font-size:14px; line-height:1.8;'>"
                    for e, m in completed:
                        final_html += f"<div>✅ {e} {m}</div>"
                    final_html += "</div>"
                    build_log.markdown(final_html, unsafe_allow_html=True)

                    # 3) Load & display your local markdown
                    # Load the raw Markdown
                    raw_md = pathlib.Path("puma_research.md").read_text()

                    # Split on the "## Sources" header
                    if "## Sources" in raw_md:
                        main_md, sources_md = raw_md.split("## Sources", 1)
                        sources_md = "## Sources" + sources_md  # re‑attach the header
                    else:
                        main_md = raw_md
                        sources_md = ""

                    st.markdown(
                        main_md,
                        unsafe_allow_html=True
                    )

                    # 2) Collapsible Sources expander
                    if sources_md:
                        with st.expander("📑 Sources & Links", expanded=False):
                            st.markdown(sources_md, unsafe_allow_html=True)


                else:
                    with st.spinner("Analyzing cultural context..."):
                        try:
                            # Context and role setup for Puma Southeast Asia cultural insights
                            system_context = """You are a cultural strategy expert specializing in Southeast Asian markets, specifically Indonesia, Malaysia, and Thailand. You have deep knowledge of:
                            - TikTok commerce and live shopping trends
                            - Local pride movements and authentic brand positioning  
                            - Traditional sports culture (Muay Thai, Sepak Takraw) integration
                            - K-pop cultural influence on fashion and lifestyle
                            - Nano-influencer trust economy
                            - Multi-generational fitness and family wellness trends
                            - Digital-physical sport fusion and temple running culture

                            Your responses should be:
                            1. Culturally nuanced and respectful
                            2. Backed by specific Southeast Asian consumer insights
                            3. Actionable for Puma's brand strategy
                            4. Focused on authentic engagement rather than superficial trends

                            Provide strategic recommendations that balance global brand consistency with local cultural authenticity."""

                            response = client.chat.completions.create(
                                model="gpt-4o-mini",  # Cheapest OpenAI model
                                messages=[
                                    {"role": "system", "content": system_context},
                                    {"role": "user", "content": user_prompt}
                                ],
                                max_tokens=800,
                                temperature=0.7
                            )
                            
                            # Display the response
                            st.markdown("#### 💡 Cultural Insights & Recommendations")
                            st.markdown(response.choices[0].message.content)   
                        except Exception as e:
                            st.error(f"Error generating insights: {str(e)}")
                        
        except Exception as e:
            st.error(f"Error setting up OpenAI client: {str(e)}")
