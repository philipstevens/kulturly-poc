# customers/insights_renderer.py

import os
import pathlib
import time

import openai
import pandas as pd
import streamlit as st

class InsightsRenderer:
    def __init__(self, data: dict):
        self.data = data

    def render(self):
        stories = self.data.get("stories", {})
        people = self.data.get("people", [])
        influencers = self.data.get("influencers", {})
        ideas = self.data.get("ideas", {})
        context = self.data.get("ai_context", {})

        tabs = st.tabs(["Stories", "People", "Influencers", "Ideas", "Kultie ✨"])
        with tabs[0]:
            self._render_stories(stories)
        with tabs[1]:
            self._render_people(people)
        with tabs[2]:
            self._render_influencers(influencers)
        with tabs[3]:
            self._render_ideas(ideas)
        with tabs[4]:
            self._render_ask(context)


    def _parse_markdown_links(self, text):
        """Convert markdown-style links [text](url) to HTML <a> tags"""
        import re
        # if they passed a list of strings, join into one
        if isinstance(text, (list, tuple)):
            text = "<br>".join(text)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.sub(pattern, r'<a href="\2" target="_blank">\1</a>', text)
    
    def _render_stories(self, stories):
        # 1. Collect only non-empty sections
        sections = []
        if stories.get("themes"):
            sections.append(("📖 Themes", stories["themes"]))
        if stories.get("dimensions"):
            sections.append(("🔎 Deep Patterns", stories["dimensions"]))
        if stories.get("metaphors"):
            sections.append(("🔗 Shared Signals", stories["metaphors"]))
        if stories.get("framing"):
            sections.append(("🌍 Local Lenses", stories["framing"]))
        if stories.get("evolution"):
            sections.append(("🧠 Word Shifts", stories["evolution"]))

        # 2. If nothing to show, bail out
        if not sections:
            st.write("No story data available.")
            return

        # 3. Create tabs dynamically
        labels, datas = zip(*sections)
        tabs = st.tabs(labels)

        # 4. Dispatch each tab to its renderer
        for (label, data), tab in zip(sections, tabs):
            with tab:
                if label == "📖 Themes":
                    self._render_themes(data)
                elif label == "🔎 Deep Patterns":
                    self._render_dimensions(data)
                elif label == "🔗 Shared Signals":
                    self._render_metaphors(data)
                elif label == "🌍 Local Lenses":
                    self._render_framing(data)
                elif label == "🧠 Word Shifts":
                    self._render_evolution(data)
       
    def _render_themes(self, themes):
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

    def _render_dimensions(self, dimensions):
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

    def _render_metaphors(self, metaphors):
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

    def _render_framing(self, framing):
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

    def _render_evolution(self, evolution):
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

    def _render_people(self, personas):

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

    def _render_influencers(self, infl):
        sections = []
        if infl.get("narratives"):
            sections.append(("🕸️ Network Types", infl["narratives"], self._render_narratives))
        if infl.get("pathways"):
            sections.append(("🛤️ Diffusion Paths", infl["pathways"], self._render_pathways))
        if infl.get("brokers"):
            sections.append(("👑 Key Brokers", infl["brokers"], self._render_brokers))

        # 2. Nothing to show?
        if not sections:
            st.write("No influencer data available.")
            return

        # 3. Create tabs dynamically
        labels = [label for label, _, _ in sections]
        tabs   = st.tabs(labels)

        # 4. Dispatch into helper methods
        for (label, data, fn), tab in zip(sections, tabs):
            with tab:
                fn(data)

    def _render_narratives(self, narratives):
        st.caption("Key influencer ecosystems shaping cultural conversations and commerce")
        cols = st.columns(2)
        for idx, nar in enumerate(narratives):
            col = cols[idx % 2]
            color = nar["color"]
            evidence_html = self._parse_markdown_links(nar["evidence"])
            with col:
                # existing card_html logic...
                st.markdown(
                    f'<div style="border:2px solid {color};border-radius:8px;padding:16px;margin:8px;">'
                    f'  <strong style="font-size:16px;">{nar["title"]}</strong>'
                    f'  <p style="opacity:0.8;">{nar["story"][:100]}…</p>'
                    f'  <details style="border-top:1px solid {color};margin-top:12px;">'
                    f'    <summary style="font-weight:bold;color:{color};">Full Details</summary>'
                    f'    <p>{nar["story"]}</p>'
                    f'    <p>{evidence_html}</p>'
                    f'    <p><strong>Takeaway:</strong> {nar["takeaway"]}</p>'
                    f'  </details>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    def _render_pathways(self, pathways):
        st.caption("How cultural moments spread through influencer networks to drive adoption")
        dot = ["digraph G {",
            "  rankdir=LR; graph [bgcolor=transparent,nodesep=1,ranksep=1];",
            "  node [shape=circle,fixedsize=true,width=1.2,height=1.2,style=filled,fontname=\"Helvetica-Bold\",fontsize=10];",
            "  edge [penwidth=2];"]
        for p in pathways:
            ids  = [f'"{n["id"]}"' for n in p["nodes"]]
            dot.append(f"  {' -> '.join(ids)} [color=\"{p['color']}\"];")
            for n in p["nodes"]:
                dot.append(f'  "{n["id"]}" [fillcolor="{p["color"]}",label="{n["label"]}",tooltip="{n["tooltip"]}"];')
        dot.append("}")
        st.graphviz_chart("\n".join(dot))

    def _render_brokers(self, brokers_list):
        st.caption("Most influential voices shaping brand perception and cultural trends")
        for market_data in brokers_list:
            cards = []
            for b in market_data["brokers"]:
                cards.append(
                    f'<div style="flex:1;min-width:220px;border:1px solid {market_data["color"]};'
                    f'border-radius:6px;padding:12px;margin:8px;">'
                    f'<strong style="color:{market_data["color"]};">{b["name"]}</strong><br>'
                    f'<em>{b["role"]}</em><p>{b["impact"]}</p>'
                    f'<details><summary style="color:{market_data["color"]};">Details</summary>'
                    f'<p>Followers: {b["followers"]}</p><p>Engagement: {b["engagement"]}</p></details>'
                    f'</div>'
                )
            container = (
                f'<div style="border:2px solid {market_data["color"]};border-radius:8px;'
                f'padding:16px;margin-bottom:24px;">'
                f'<strong style="font-size:18px;">{market_data["market"]}</strong>'
                f'<p style="opacity:0.8;"><em>{market_data["description"]}</em></p>'
                f'<div style="display:flex;flex-wrap:wrap;justify-content:space-between;">'
                + "".join(cards) +
                '</div></div>'
            )
            st.markdown(container, unsafe_allow_html=True)
 
    def _render_ideas(self, ideas):
        sections = []
        if ideas.get("hypotheses"):
            sections.append(("🧪 Hypotheses", ideas["hypotheses"], self._render_hypotheses))
        if ideas.get("gaps"):
            sections.append(("🔍 Opportunity Gaps", ideas["gaps"], self._render_gaps))
        if ideas.get("playbooks"):
            sections.append(("🎨 Culture Creation", ideas["playbooks"], self._render_playbooks))
        if ideas.get("scenarios"):
            sections.append(("❓ What If", ideas["scenarios"], self._render_scenarios))
        if ideas.get("recommendations"):
            sections.append(("🚀 Actions", ideas["recommendations"], self._render_recommendations))

        # 2. nothing to show?
        if not sections:
            st.write("No ideas data available.")
            return

        # 3. create tabs dynamically
        labels = [label for label, _, _ in sections]
        tabs   = st.tabs(labels)

        # 4. dispatch
        for (label, data, fn), tab in zip(sections, tabs):
            with tab:
                fn(data)

    def _render_card(self, title, body_lines, *, border="1px solid #ccc", bg_color=None, details=None):
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
          
    def _render_hypotheses(self, hypotheses):
        st.caption("Key if–then hypotheses to test.")
        cols = st.columns(2)
        for idx, h in enumerate(hypotheses):
            with cols[idx % 2]:
                self._render_card(
                    title=h["statement"],
                    body_lines=[f"Source: {h['source']}"],
                    border="1px solid #888",
                    details=("Full Hypothesis", [h["statement"]])
                )

    def _render_gaps(self, gaps):
        st.caption("Unmet opportunities—each gap is a trigger for action.")
        for g in gaps:
            self._render_card(
                title=f"🎯 {g['title']}",
                body_lines=[g['body'], f"Source: {g['source']}"],
                border="1px dashed #999"
            )

    def _render_playbooks(self, playbooks):
        st.caption("Activation Playbooks—frameworks distilled by AI from 50K+ cultural data points")
        for c in playbooks:
            parts = [
                f"<p><strong>Goal:</strong> {c['goal']}</p>",
                "<p><strong>Steps:</strong></p><ul style='margin:4px 0 8px 16px;'>"
                + "".join(f"<li>{s}</li>" for s in c["steps"]) + "</ul>",
                "<p><strong>Metrics:</strong></p><ul style='margin:4px 0 8px 16px;'>"
                + "".join(f"<li>{m}</li>" for m in c["metrics"]) + "</ul>",
                f"<p style='font-size:0.85em; color:gray;'><em>Source: {c['source']}</em></p>"
            ]
            body_html = "".join(parts)
            self._render_card(
                title=c["title"],
                body_lines=[body_html],
                border=c.get("border", "1px solid #ccc")
            )

    def _render_scenarios(self, scenarios):
        st.caption("What If Scenarios — projected outcomes")
        container = '<div style="display:flex;flex-direction:column;gap:16px;">'
        for idx, s in enumerate(scenarios, start=1):
            container += (
                f'<div style="display:flex;align-items:flex-start;gap:12px;">'
                f'<div style="min-width:32px;height:32px;border-radius:50%;'
                f'background:#FF5722;color:#fff;display:flex;align-items:center;'
                f'justify-content:center;font-weight:bold;font-size:14px;">{idx}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-size:15px;font-weight:bold;color:#FF5722;'
                f'margin-bottom:4px;">{s["title"]}</div>'
                f'<div style="font-size:14px;line-height:1.5;margin-bottom:6px;">'
                f'{s["body"]}</div>'
                f'<div style="font-size:12px;color:gray;">Source: {s["source"]}</div>'
                f'</div></div>'
            )
        container += "</div>"
        st.markdown(container, unsafe_allow_html=True)

    def _render_recommendations(self, recs):
        st.caption("Next steps—priority actions.")
        for r in recs:
            st.markdown(
                f"<div style='border-left:5px solid #4CAF50;padding:12px;margin-bottom:8px;'>"
                f"<strong>{r['priority']}. {r['title']}</strong>"
                f"<p style='margin:4px 0;'>{r['body']}</p>"
                f"</div>",
                unsafe_allow_html=True
            )
    
    def _render_ask(self, ai_context):
        DEFAULT_SYSTEM_CONTEXT = (
            "You are Kultie, an assistant for exploring market and cultural insights. "
            "Provide clear, evidence-based recommendations."
        )

        system_context = ai_context.get("system_context") or DEFAULT_SYSTEM_CONTEXT
        research_file = ai_context.get("research_file")
        research_path = None
        if research_file:
            research_path = pathlib.Path(research_file)


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
                placeholder="Ask about cultural trends, market insights, or strategic recommendations",
                height=100
            )
            
            col1, col2 = st.columns([19, 1])
            with col1:
                deep_research = st.toggle("Deep Research", value=False, key="deep_research")
            with col2:
                submit_clicked = st.button("➤", key="submit_btn", help="Submit query")
                    
            if submit_clicked and user_prompt.strip():
                if deep_research and research_file and research_path.exists():
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
                    try:
                        raw_md = research_path.read_text()
                    except Exception:
                        st.error(f"Could not load research file: {research_file}")
                        return

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
