# customers/insights_renderer.py

from datetime import datetime
import hashlib
import html
import os
from pathlib import Path
import re
import time

import bleach
from markdown import markdown
import openai
import pandas as pd
import streamlit as st

class ThemeCard:
    def __init__(self, data: dict):
        self.data = data or {}
        self._tooltips = {
            "caption": "Provides contextual framing for the displayed set of themes.\n\nIncludes:\n• Scope of observable cultural signals (e.g., social media, news, forums, videos, images)\n• Timeframe of data collection and processing\n• Last scan date for freshness assessment",
            "title": "Canonical identifier for the cultural theme, generated from aggregated multimodal signals:\n• Sources: social media, news, web articles, images, videos, transcripts\n• Optimized for cross-market recognition and longitudinal tracking\n• Serves as the primary key for analytical reference",
            "subtitle": "One-line narrative descriptor summarizing the cultural essence of the theme:\n• Expressed in accessible, non-technical language\n• Captures the interpretive framing analysts use in cultural intelligence outputs\n• Does not include quantitative or operational metadata",
            "momentum": "Growth velocity of the theme, based on month-over-month (MoM) change in total signal volume:\n• Surging: > 50% MoM increase\n• Rising: 10–50% MoM increase\n• Stable: ±10% MoM change\n• Plateauing: < 10% growth with signs of slowdown\n• Declining: > 10% MoM decrease\n\nCalculated from absolute signal volume difference between periods.",
            "also_emerging_in": "List of secondary geographies/markets where the theme shows statistically significant growth:\n• Identified by cross-market signal clustering\n• Requires both relative growth and minimum absolute signal volume threshold",
            "maturity": "Lifecycle stage of the theme, inferred from observation period length and adoption breadth:\n• Nascent – Very new; <3 months observed; early, niche attention\n• Emerging – 3–6 months observed; traction in early adopter segments\n• Scaling – 6–18 months; rapid adoption across multiple sectors or markets\n• Established – >18 months; normalized presence and mainstream adoption\n\nDerived from persistent detection in consecutive scans and breadth of category/market penetration.",
            "last_scan": "Date/time of most recent successful ingestion of signals linked to this theme:\n• Indicates currentness of insights\n• Used to assess risk of staleness in decision-making contexts\n• Always expressed in YYYY-MM-DD format for machine-readability",
            "summary_box": "Executive synthesis providing a high-level answer to *What is this theme and why does it matter?*:\n• Combines cultural meaning, key actors, and relevance drivers\n• Written for quick strategic consumption by non-technical stakeholders\n• Distills narrative without full technical context",
            "story": "Narrative core of the theme:\n• Explains what the theme represents\n• Describes its emergence and evolution over time\n• Links to broader cultural, economic, or technological shifts\n• Informed by aggregated qualitative coding of multimodal signals",
            "proof_points": "Evidence corpus showing the theme in action:\n• May include social posts, article excerpts, influencer content, product launches, campaign visuals\n• Selected for representativeness and clarity\n• Annotated with engagement metrics (e.g., views, likes, shares) where available",
            "quotes": "Direct verbatim statements from individuals or influencers illustrating the theme:\n• Captured from qualitative coding of social media, interviews, or content transcripts\n• Selected for diversity of voice and authenticity\n• May include demographic or contextual metadata (e.g., age, location, role)",
            "personas": "Consumer archetype definitions for segments engaging with the theme:\n• Label: human-readable segment name\n• Description: behavioral and attitudinal profile, supported by observed signals\n• Derived from thematic clustering of user behaviors and preferences",
            "drivers": "Underlying causal forces accelerating or enabling the theme:\n• Can be economic, cultural, technological, or regulatory\n• Each driver is supported by observed trend data or signal clusters\n• Used for forecasting and scenario planning",
            "other_markets": "Comparative market lens showing how the same cultural idea manifests elsewhere:\n• Includes similarities and divergences in expression\n• Drawn from localized signal pools per geography or culture\n• Supports cross-market strategy alignment",
            "language": "Linguistic fingerprint of the theme:\n• Keywords, hashtags, idioms, and phrases disproportionately associated with the theme in the selected market\n• Based on comparative frequency analysis against all other markets as a baseline\n• Includes both English terms and equivalent translations in local languages\n• Useful for content targeting, message localisation, and search optimisation",
            "evolution": "Temporal change map of the theme:\n• Past state: how it first appeared in cultural discourse\n• Present state: current dominant framing and behaviors\n• Next state: projected or emergent shifts based on recent signal patterns\n• Supports innovation timing and portfolio adaptation",
            "signals": "Leading indicators to monitor for theme trajectory changes:\n• Quantitative triggers (e.g., rapid MoM growth, cross-category adoption)\n• Qualitative triggers (e.g., new influencer adoption, media framing shift)\n• Each signal mapped to potential impact scenarios"
        }

    # ---------- Markdown -> HTML Helpers ----------
    def md(self, s: str) -> str:
        if not s:
            return ""
        html_out = markdown(
            s,
            extensions=["extra", "sane_lists", "nl2br", "smarty"]
        )
        cleaned = bleach.clean(
            html_out,
            tags=[
                "p","em","strong","a","ul","ol","li","br","blockquote","code","pre",
                "h1","h2","h3","h4","h5","h6","span","table","thead","tbody","tr","th","td"
            ],
            attributes={"a": ["href","title","rel","target"], "span": ["title"]},
            protocols=["http","https","mailto"],
            strip=True
        )
        # NEW: strip outer <p> or heading tags so text won't have default margins
        cleaned = re.sub(r'^\s*<(p|h[1-6])>(.*?)</\1>\s*$', r'\2', cleaned, flags=re.S)
        return cleaned

    def md_attr(self, s: str) -> str:
        # For HTML attributes like title=, never pass raw
        return html.escape("" if s is None else str(s), quote=True)

    def md_ul(self, items):
        if not items:
            return "<em>No data</em>"
        # Convert each item from MD to HTML, then wrap in <li>
        return "".join(f"<li>{self.md(i)}</li>" for i in items)

    def md_kv(self, d):
        if not d:
            return "<em>No data</em>"
        return "".join(f"<li><strong>{html.escape(str(k))}:</strong> {self.md(str(v))}</li>" for k, v in d.items())

    def md_quotes(self, quotes):
        if not quotes:
            return "<em>No quotes</em>"
        parts = []
        for q in quotes:
            if isinstance(q, (list, tuple)) and len(q) == 2:
                qt, au = q
                parts.append(
                    '<blockquote style="margin:0 0 8px;padding-left:12px;border-left:3px solid;">'
                    f'{self.md(qt)}<footer style="font-size:0.85em;margin-top:4px;">- {html.escape(str(au))}</footer></blockquote>'
                )
            else:
                parts.append(
                    '<blockquote style="margin:0 0 8px;padding-left:12px;border-left:3px solid;">'
                    f'{self.md(q)}</blockquote>'
                )
        return "\n".join(parts)

    # ---------- Other Helpers ----------
    def _pick_color(self, idx: int, palette=None):
        palette = palette or [
            "#F97316",  # Strong orange
            "#34D399",  # Teal green
            "#FF6B6B",  # Bright red
            "#60A5FA",  # Vivid blue
            "#FFD93D",  # Bright yellow
            "#8B5CF6",  # Deep violet
            "#22D3EE",  # Cyan
            "#C084FC"   # Light purple
        ]
        return palette[idx % len(palette)]

    def _safe(self, d, key, default=""):
        v = d.get(key, default)
        return v if v not in (None, "", []) else default

    def _fmt_num(self, n: int) -> str:
        try:
            n = int(n)
        except Exception:
            return str(n)
        if abs(n) >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if abs(n) >= 1_000:
            return f"{n/1_000:.0f}k"
        return str(n)

    def _derive_maturity(self, first_seen: str, last_scan: str) -> str:
        try:
            first_date = datetime.strptime(first_seen, "%Y-%m-%d")
            last_date = datetime.strptime(last_scan, "%Y-%m-%d")
            months = (last_date.year - first_date.year) * 12 + (last_date.month - first_date.month)
        except Exception:
            return "-"
        return "Nascent" if months < 3 else "Emerging" if months < 6 else "Scaling" if months < 18 else "Established"

    def _derive_momentum(self, current_volume: int, previous_volume: int):
        try:
            c = int(current_volume); p = int(previous_volume)
        except Exception:
            return "-", 0.0, 0
        velocity = c - p
        growth_pct = 100.0 if p <= 0 and velocity > 0 else (0.0 if p <= 0 else (velocity / p) * 100)
        if growth_pct > 50: label = "Surging"
        elif growth_pct > 10: label = "Rising"
        elif growth_pct > -10: label = "Stable"
        elif growth_pct > -50: label = "Plateauing"
        else: label = "Declining"
        return label, growth_pct, velocity

    # ---------- Public render ----------
    def render(self):
        themes = self.data

        last_scan_global = self._safe(themes[0], "last_scan", "-") if themes else "-"
        st.caption(f"Observable stories and behaviors shaping culture right now • Last scan: {last_scan_global}")
        title_size = 20
        
        for i, nar in enumerate(themes):
            trend_color = nar.get("trend_color", self._pick_color(i))
            title = self._safe(nar, "title", "Untitled Theme")
            subtitle = self._safe(nar, "subtitle")

            current_volume = int(nar.get("current_volume", 0))
            previous_volume = int(nar.get("previous_volume", 0))
            label, pct, vel = self._derive_momentum(current_volume, previous_volume)

            first_seen = self._safe(nar, "first_seen", "-")
            last_scan = self._safe(nar, "last_scan", "-")
            maturity = self._derive_maturity(first_seen, last_scan) if first_seen != "-" and last_scan != "-" else "-"

            story = self._safe(nar, "story")
            summary = self._safe(nar, "summary")
            proof_points = nar.get("proof_points", [])
            quotes = nar.get("quotes", [])
            personas = nar.get("personas", {})
            drivers = nar.get("drivers", [])
            also_emerging_in = nar.get("also_emerging_in", [])
            other_markets = nar.get("other_markets", {})
            language = self._safe(nar, "language")
            evolution = nar.get("evolution", {})
            signals = nar.get("signals", [])

            # Pre-render MD -> HTML once per field
            title_html = self.md(title)
            subtitle_html = self.md(subtitle) if subtitle else ""
            story_html = self.md(story) if story else "<em>No story provided</em>"
            summary_html = self.md(summary) if summary else ""
            language_html = self.md_kv(language) if language else "<em>No language notes</em>"
            proof_points_html = self.md_ul(proof_points) if proof_points else "<em>No proof points</em>"
            drivers_html = self.md_kv(drivers)
            signals_html = self.md_ul(signals) if signals else "<em>No data</em>"
            personas_html = self.md_kv(personas)
            other_markets_html = self.md_kv(other_markets)
            evolution_html = self.md_kv(evolution)
            quotes_html = self.md_quotes(quotes)

            card_html = f"""
                <div style="border:2px solid {trend_color};border-radius:10px;padding:16px;margin-bottom:16px;">
                    
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:8px;">
                        <div style="margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid #E0E0E0;">
                            <div style="border:2px solid {trend_color};padding:3px 10px;border-radius:6px;display:inline-flex;align-items:center;line-height:1;margin:1px;margin-bottom:4px;">
                                <strong style="font-size:{title_size}px;line-height:1;letter-spacing:.2px;" title="{self.md_attr(self._tooltips['title'])}">{title_html}</strong>
                            </div>
                            {"<div style='font-size:13px;line-height:1.45;opacity:.85;font-style:italic;'>" + subtitle_html + "</div>" if subtitle_html else ""}
                        </div>
                    </div>

                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;">
                        <div title="{self.md_attr(self._tooltips['momentum'])}"><strong>Growth:</strong> {html.escape(label)} ({pct:+.1f}% vs prior; {("+" if (current_volume-previous_volume)>0 else "")}{self._fmt_num(current_volume-previous_volume)} mentions)</div>
                        <div title="{self.md_attr(self._tooltips['also_emerging_in'])}"><strong>Also In:</strong> {html.escape(", ".join(also_emerging_in)) if also_emerging_in else "None"}</div>
                        <div title="{self.md_attr(self._tooltips['maturity'])}"><strong>Stage:</strong> {html.escape(maturity)}</div>
                        <div title="{self.md_attr(self._tooltips['last_scan'])}"><strong>Last Scan:</strong> {html.escape(last_scan)}</div>
                    </div>

                    {f"<div style='margin-top:12px;padding:8px 10px;border:1px solid #E0E0E0;border-radius:4px;font-size:14px;line-height:1.5;' title='{self.md_attr(self._toolips['summary_box']) if False else self.md_attr(self._tooltips['summary_box'])}'><strong style='display:block;margin-bottom:4px;font-size:15px;'>Summary</strong>{summary_html}</div>" if summary_html else ""}

                    <details style="margin-top:14px;border-radius:8px;overflow:hidden;">
                        <summary style="font-weight:bold;cursor:pointer;">Full Details</summary>
                        <div style="padding:10px 4px 0;border-top:1px solid #e5e7eb;line-height:1.6;">

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['story'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">What's happening?</h4>
                            <div>{story_html}</div>
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['proof_points'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">What is the proof?</h4>
                            <ul style="margin:0;padding-left:16px;">{proof_points_html}</ul>
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['quotes'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">What are people saying?</h4>
                            {quotes_html}
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['personas'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">Who is driving it?</h4>
                            <ul style="margin:0;padding-left:16px;">{personas_html}</ul>
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['drivers'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">Why now?</h4>
                            <ul style="margin:0;padding-left:16px;">{drivers_html}</ul>
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['other_markets'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">How is it different elsewhere?</h4>
                            <ul style="margin:0;padding-left:16px;">{other_markets_html}</ul>
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['language'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">How do people talk about it?</h4>
                            <div>{language_html}</div>
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['evolution'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">How is it changing?</h4>
                            <ul style="margin:0;padding-left:16px;">{evolution_html}</ul>
                        </section>

                        <section style="margin:12px 0;" title="{self.md_attr(self._tooltips['signals'])}">
                            <h4 style="margin:0 0 4px;font-size:{title_size}px;">What should we watch for?</h4>
                            <ul style="margin:0;padding-left:16px;">{signals_html}</ul>
                        </section>

                        </div>
                    </details>
                </div>
                """
            card_html = re.sub(r"\n\s*\n", "\n", card_html)
            st.markdown(card_html, unsafe_allow_html=True)

class InsightsRenderer:
    def __init__(self, data: dict):
        self.data = data

    def render(self):
        themes = self.data.get("themes", [])
        themes = ThemeCard(themes)
        themes.render()

    def _render_ask(self, ai_context):
        DEFAULT_SYSTEM_CONTEXT = (
            "You are Kultie, an assistant for exploring market and cultural insights. "
            "Provide clear, evidence-based recommendations."
        )

        system_context = ai_context.get("system_context") or DEFAULT_SYSTEM_CONTEXT
        research_file = ai_context.get("research_file")
        research_path = None
        if research_file:
            research_path = pathlib.Path("research") /pathlib.Path(research_file)


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
                        ("📚", "Analyzing 847 sources...", 2),
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
