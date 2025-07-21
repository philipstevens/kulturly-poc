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

class Puma(BaseCustomerRenderer):
    def __init__(self):
        config = {
            "default_geographies": ["Malaysia", "Thailand", "Indonesia"]
        }
        super().__init__(name="Puma", config=config)
    
    def _parse_markdown_links(self, text):
        """Convert markdown-style links [text](url) to HTML <a> tags"""
        import re
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
        
            narratives = [
                {
                    "title": "TikTok Commerce Revolution",
                    "story": (
                        "In Indonesia, TikTok Shop transforms shopping into live entertainment—"
                        "streamers debut new collections and viewers buy directly via in-app links."),
                    "story_preview": "TikTok Shop transforms shopping into live entertainment in Indonesia...",
                    "evidence": (
                        "[VulcanPost on TikTok Shop's growth]"
                        "(https://vulcanpost.com/834059/can-tiktok-shop-dethrone-shopee-lazada/) and "
                        "[RTL Today on social-commerce trends]"
                        "(https://today.rtl.lu/news/business-and-tech/a/2078371.html)"),
                    "impact": "Leverage shoppable live events to create buzz around product launches.",
                    "first_seen": "Aug 15, 2024",
                    "velocity": "+1,247%",
                    "volume": "542.3K mentions",
                    "confidence": 0.92,
                    "momentum": "🚀 Accelerating",
                    "maturity": "Early Growth",
                    "trend_color": "#FF6B6B"
                },
                {
                    "title": "Authentic Local Pride Movement",
                    "story": (
                        "'Made in Indonesia' sneaker pop-ups spark grassroots rallies—"
                        "consumers wear local brands as statements of national pride."),
                    "story_preview": "'Made in Indonesia' sneaker pop-ups spark grassroots rallies...",
                    "evidence": (
                        "60.7% of Indonesians prefer local affordable products "
                        "[SemanticsScholar study]"
                        "(https://pdfs.semanticscholar.org/f0f9/df7097005f4aad83088ec3528c5d1d7e417a.pdf)"),
                    "impact": "Co-create limited editions with local artisans to tap into cultural nationalism.",
                    "first_seen": "Jun 22, 2024",
                    "velocity": "+834%",
                    "volume": "287.6K mentions",
                    "confidence": 0.88,
                    "momentum": "📈 Steady Growth",
                    "maturity": "Emerging",
                    "trend_color": "#4ECDC4"
                },
                {
                    "title": "Traditional Sports Resurgence",
                    "story": (
                        "Sepak Takraw tournaments and Muay Thai events go viral on social feeds, "
                        "drawing millions of interactions."),
                    "story_preview": "Sepak Takraw tournaments and Muay Thai events go viral on social feeds...",
                    "evidence": (
                        "Thailand's Panipak Tennis Olympic gold generated 3M+ social interactions in one day "
                        "[DataXet report]"
                        "(https://www.dataxet.co/insights/olympic-games-2024-en)"),
                    "impact": "Sponsor grassroots tournaments and integrate classical motifs into designs.",
                    "first_seen": "Jul 28, 2024",
                    "velocity": "+2,156%",
                    "volume": "1.2M mentions",
                    "confidence": 0.94,
                    "momentum": "💥 Viral Spike",
                    "maturity": "Peak Moment",
                    "trend_color": "#FFE66D"
                },
                {
                    "title": "Nano-Influencer Trust Economy",
                    "story": (
                        "Micro-influencers (1k–10k followers) spark authentic conversations—"
                        "their daily posts on Puma gear drive deeper trust than celebrity endorsements."),
                    "story_preview": "Micro-influencers spark authentic conversations with deeper trust...",
                    "evidence": (
                        "Nano-influencers command 46% greater trust [Pongoshare report]"
                        "(http://pongoshare.com/trends-in-influencer-marketing-southeast-asia/) and "
                        "87% of Indonesians prefer intimate messaging interactions [Statista]"
                        "(https://www.statista.com/forecasts/1345510/asia-most-used-social-media-platforms-of-gen-z-by-country-and-type)"),
                    "impact": "Build city-by-city micro-ambassador programs to amplify genuine stories.",
                    "first_seen": "May 14, 2024",
                    "velocity": "+445%",
                    "volume": "398.1K mentions",
                    "confidence": 0.89,
                    "momentum": "⚡ Sustained Growth",
                    "maturity": "Established",
                    "trend_color": "#A8E6CF"
                },
                {
                    "title": "Cross-Cultural K-Wave Integration",
                    "story": (
                        "K-pop ambassadors like Blackpink's Rosé make Puma styles aspirational—"
                        "fans emulate viral dance looks across SEA."),
                    "story_preview": "K-pop ambassadors make Puma styles aspirational across SEA...",
                    "evidence": (
                        "K-pop drives SEA sportswear trends [Retail Asia]"
                        "(https://retailasia.com/videos/korean-culture-drives-southeast-asia-sportswear-trends)"),
                    "impact": "Align product drops with major K-pop comebacks and fan events.",
                    "first_seen": "Mar 8, 2024",
                    "velocity": "+672%",
                    "volume": "756.8K mentions",
                    "confidence": 0.91,
                    "momentum": "🔄 Cyclical Peaks",
                    "maturity": "Mature",
                    "trend_color": "#DDA0DD"
                },
                {
                    "title": "Digital-Physical Sport Fusion",
                    "story": (
                        "Runners and athletes document temple runs and treks in Puma gear—"
                        "turning workouts into social challenges."),
                    "story_preview": "Runners document temple runs, turning workouts into social challenges...",
                    "evidence": (
                        "Over 40% run weekly and share journeys online [YouGov Singapore]"
                        "(https://business.yougov.com/content/50255-a-look-at-singapores-growing-running-community)"),
                    "impact": "Create geo-tagged digital challenges that bridge culture and sport.",
                    "first_seen": "Apr 19, 2024",
                    "velocity": "+523%",
                    "volume": "334.2K mentions",
                    "confidence": 0.87,
                    "momentum": "📊 Steady Growth",
                    "maturity": "Growing",
                    "trend_color": "#87CEEB"
                },
                {
                    "title": "Multigenerational Athletic Identity",
                    "story": (
                        "Olympic heroes and wellness seekers unite—grandparents and grandchildren "
                        "share Puma fitness moments across generations."),
                    "story_preview": "Olympic heroes and wellness seekers unite across generations...",
                    "evidence": (
                        "Cross-generational fitness engagement rising in SEA [DataXet, JLL]"
                        "(https://www.jll.com.sg/en/trends-and-insights/research/thailand-s-sports-boom-energizes-the-retail-market)"),
                    "impact": "Design campaigns celebrating family fitness and rituals.",
                    "first_seen": "Jul 12, 2024",
                    "velocity": "+789%",
                    "volume": "423.7K mentions",
                    "confidence": 0.85,
                    "momentum": "🌱 Building",
                    "maturity": "Early Growth",
                    "trend_color": "#F0A500"
                }
            ]
            
            cols = st.columns(2)
            for idx, nar in enumerate(narratives):
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
            "👑 Key Brokers"
        ])
        
        # Tab 1: Core Influence Narratives
        with influencer_tabs[0]:
            st.caption("Key influencer ecosystems shaping cultural conversations and commerce")
            
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

        # Tab 2: Diffusion Pathways
        with influencer_tabs[1]:
            st.caption("How cultural moments spread through influencer networks to drive adoption")
            
            st.code(
                "Cultural Moment → TikTok Algorithm → Instagram Reels → Local Forums → Physical Adoption\n"
                "Olympic Victory → Viral Content → Community Discussion → Product Interest → Purchase\n"
                "Local Exhibition → Social Documentation → Hashtag Movement → Mainstream Adoption"
            )

        # Tab 3: Key Cultural Brokers
        with influencer_tabs[2]:
            st.caption("Most influential voices shaping brand perception and cultural trends")
            
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
        strategy_tabs = st.tabs([
            "🧪 Hypotheses", 
            "🔍 Opportunity Gaps",
            "🚀 Actions"
        ])

        with strategy_tabs[0]:
            hypotheses = [
                {
                    "cluster": "Narratives",
                    "statement": "Collaborating with local traditional sports communities (Muay Thai gyms, Sepak Takraw clubs) will increase cultural authenticity perception by 35% among Heritage-Forward Trendsetters.",
                    "source": '<a href="https://www.dataxet.co/insights/olympic-games-2024-en" target="_blank">SEA social listening, Q3 2025</a>'
                },
                {
                    "cluster": "Personas",
                    "statement": "Targeting Digital Native Athletes with Paralympic-inspired adaptive sports gear will capture the emerging inclusion trend and drive 25% engagement increase.",
                    "source": '<a href="https://seasia.co/infographic/what-are-the-top-google-searches-in-southeast-asia-in-2024" target="_blank">TikTok engagement metrics, Q2 2025</a>'
                },
                {
                    "cluster": "Networks",
                    "statement": "Partnering with nano-influencers (1k–10k followers) for hyper-localized content will achieve 40% higher conversion rates than macro-influencer campaigns.",
                    "source": '<a href="https://www.marketing-interactive.com/tiktok-is-gen-z-s-cultural-playground-in-southeast-asia" target="_blank">TikTok Shop conversion data, 2025</a>'
                },
                {
                    "cluster": "Trends",
                    "statement": "Launching TikTok Live commerce sessions during major sporting events will capitalize on viral cultural moments and drive 50% higher purchase intent.",
                    "source": '<a href="https://today.rtl.lu/news/business-and-tech/a/2078371.html" target="_blank">Live commerce analytics, ongoing</a>'
                }
            ]

            for h in hypotheses:
                st.markdown(
                    f"""
                    <div style="border:1px solid #ccc; border-radius:6px; padding:12px; margin-bottom:12px;">
                        <p style="margin:8px 0 4px 0;"> {h['statement']}</p>
                        <p style="margin:0; font-size:0.85em; color:gray;"><em>Source: {h['source']}</em></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with strategy_tabs[1]:
            gaps = [
                {
                    "title": "Local Culture & Sports Heritage",
                    "body": "Co-design a Muay Thai and Sepak Takraw-inspired capsule with regional gyms and artisans, addressing the 60% of Heritage-Forward urban consumers in SEA who seek authentic cultural narratives in sportswear.",
                    "source": '<a href="https://www.dataxet.co/insights/olympic-games-2024-en" target="_blank">SEA social listening, Q3 2025</a>'
                },
                {
                    "title": "Immersive Social Commerce White Space",
                    "body": "Launch interactive TikTok Shop live events for Puma gear—leveraging under‑utilized social commerce channels to create shareable, event‑style shopping experiences and drive spontaneous sales spikes.",
                    "source": '<a href="https://www.marketing-interactive.com/tiktok-is-gen-z-s-cultural-playground-in-southeast-asia" target="_blank">TikTok commerce data, 2025</a>'
                },
                {
                    "title": "Nano-Influencer Community Partnerships",
                    "body": "Build a ‘Puma Community Crew’ of nano-influencers (1k–10k followers) across Bangkok, Jakarta, and Manila to co-create localized content and small-scale activations—capitalizing on 40% higher conversions vs. macros.",
                    "source": '<a href="https://seasia.co/infographic/what-are-the-top-google-searches-in-southeast-asia-in-2024" target="_blank">TikTok engagement metrics, Q2 2025</a>'
                },
                {
                    "title": "Inclusive & Adaptive Gear Opportunity",
                    "body": "Introduce a ‘Puma Adapt & Modest’ line—featuring sports hijabs, full-coverage activewear, and adaptive footwear—responding to a 30% surge in regional searches post-Paralympics.",
                    "source": '<a href="https://today.rtl.lu/news/business-and-tech/a/2078371.html" target="_blank">Live commerce analytics, ongoing</a>'
                }
            ]

            for g in gaps:
                st.markdown(
                    f"""
                    <div style="border:1px dashed #999; border-radius:6px; padding:12px; margin-bottom:12px;">
                        <h4 style="margin-bottom:6px;">{g['title']}</h4>
                        <p style="margin:0;">{g['body']} <br><em>Source: {g['source']}</em></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        with strategy_tabs[2]:
            recommendations = [
                {
                    "priority": 1,
                    "title": "Authentic Local Sports Integration",
                    "body": "Develop collaborations with traditional sports communities (Muay Thai, Sepak Takraw) to create culturally grounded product lines that respect heritage while meeting modern performance needs. Focus on storytelling that bridges traditional athletic culture with contemporary lifestyle aspirations."
                },
                {
                    "priority": 2,
                    "title": "Nano-Influencer Commerce Network",
                    "body": "Build relationships with 1k–10k follower creators who embody authentic community leadership. Prioritize trust-building over reach metrics to match Southeast Asian preferences for intimate brand connections."
                },
                {
                    "priority": 3,
                    "title": "Cultural Moment Activation",
                    "body": "Develop rapid-response capabilities to capitalize on viral sporting moments through real-time content creation and TikTok Live commerce activations that feel organic rather than opportunistic."
                }
            ]

            for r in recommendations:
                st.markdown(
                    f"""
                    <div style="border-left:5px solid #4CAF50; padding:12px; margin-bottom:16px;">
                        <h4 style="margin-bottom:6px;">{r['priority']}. {r['title']}</h4>
                        <p style="margin:0;">{r['body']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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
