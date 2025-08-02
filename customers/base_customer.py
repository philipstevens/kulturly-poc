# customers/base_customer.py

import json
import os
import pathlib
import time

import openai
import pandas as pd
import streamlit as st

class BaseCustomerRenderer:
    def __init__(self, name, data_path):
        self.name = name
        raw = pathlib.Path(data_path).read_text()
        self.data = json.loads(raw)

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
        
        stories = self.data.get("stories", {})

        themes = stories.get("themes", [])
        dimensions = stories.get("dimensions", [])
        metaphors = stories.get("metaphors", [])
        framing = stories.get("framing", [])
        evolution = stories.get("evolution", [])

        # Tab 1: Cultural Narratives
        with main_tabs[0]:
            st.caption("Observable stories and behaviors shaping culture right now • Last scan: 2 hours ago")
                    
            cols = st.columns(2)
            for idx, nar in enumerate(themes):
                col = cols[idx % 2]
                confidence_pct = int(nar["confidence"] * 100)
                evidence_html = self._parse_markdown_links(nar["evidence"])
                
                with col:
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
  
        # Tab 2: Hidden Dimensions     
        with main_tabs[1]:
            st.caption("Underlying conceptual tensions organizing meaning across domains")
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

        # Tab 3: Cross-Domain Analogies
        with main_tabs[2]:
            st.caption("Illustrative parallels showing shared structure across domains")
            tabs = st.tabs([m["title"] for m in metaphors])

            for tab, m in zip(tabs, metaphors):
                with tab:
                    st.markdown(f"*{m['metaphor']}*")
                    st.caption(m["narrative"])
                    df = pd.DataFrame(m["rows"])
                    col_cfg = {
                        col: st.column_config.TextColumn(col, width="medium")
                        for col in m["columns"]
                    }
                    st.dataframe(df, use_container_width=True, hide_index=True, column_config=col_cfg)

        # Tab 4: Regional Framings
        with main_tabs[3]:
            st.caption("How core ideas are locally interpreted and emphasized across cultures")
            
            titles = [item["title"] for item in framing]
            framing_tabs = st.tabs(titles)

            for tab, content in zip(framing_tabs, framing):
                with tab:
                    df = pd.DataFrame(content["data"])
                    
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
                    st.markdown(f"**Evidence Sources:** {', '.join(content['evidence'])}")
                    st.markdown(f"**Strategic Impact:** {content['strategic_impact']}")

        # Tab 5: Semantic Evolution
        with main_tabs[4]:
            st.caption("How key terms shift meaning across contexts and time")

            tab_names = [m['title'] for m in evolution]
            evolution_tabs = st.tabs(tab_names)
            
            for tab, data in zip(evolution_tabs, evolution):
                with tab:              
                    timeline_html = '<div style="border:1px solid #ddd; border-radius:8px; padding:16px; margin-bottom:16px;">'
                    for year, meaning in data["evolution"].items():
                        timeline_html += f'<div style="margin-bottom:12px;"><strong>{year}</strong> → {meaning}</div>'
                    timeline_html += '</div>'               
                    st.markdown(timeline_html, unsafe_allow_html=True)              
                    st.info(f"**Shift driver:** {data['shift_driver']}")

    def render_people(self):
        personas = self.data.get("people", [])

        # Display as styled cards with inline details
        cols = st.columns(3)
        for idx, p in enumerate(personas):
            col = cols[idx % 3]
            evidence_html = self._parse_markdown_links(p["evidence"])
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
                <section style="margin:12px 0;"><h4 style="margin:0 0 4px;font-size:14px;">Evidence</h4><p style="margin:0;">{evidence_html}</p></section>
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

        influencers = self.data.get("influencers", {})

        narratives = influencers.get("narratives", [])
        pathways = influencers.get("pathways", [])
        brokers = influencers.get("brokers", [])
        
        # Tab 1: Core Influence Narratives
        with influencer_tabs[0]:
            st.caption("Key influencer ecosystems shaping cultural conversations and commerce")
            
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
 
    def render_ideas(self):
        tabs = st.tabs([
            "🧪 Hypotheses", 
            "🔍 Opportunity Gaps",
            "🎨 Culture Creation",
            "❓ What If",
            "🚀 Actions"
        ])

        ideas = self.data.get("ideas", {})

        hypotheses = ideas.get("hypotheses", [])
        gaps = ideas.get("gaps", [])
        playbooks = ideas.get("playbooks", [])
        scenarios = ideas.get("scenarios", [])
        recommendations = ideas.get("recommendations", [])

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

            for c in playbooks:
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
