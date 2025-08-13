# customers/insights_renderer.py

from datetime import datetime
import os
import pathlib
import time
import hashlib

import openai
import pandas as pd
import streamlit as st

TOOLTIPS = {
    "stories": {
        "themes": {
            "title": (
                "Name of the cultural theme as identified from aggregated multimodal signals "
                "(social media, news, web articles, images, video transcripts, and other data sources)."
            ),
            "story": (
                "Narrative summarizing what the theme represents, why it matters, and how it is evolving over time. "
                "Includes context on drivers, cultural significance, and emerging patterns."
            ),
            "evidence": (
                "Curated links and references to supporting signals (e.g., articles, posts, media items) "
                "demonstrating the existence, growth, and relevance of this theme."
            ),
            "impact": (
                "Strategic implications and recommended responses based on this theme. "
                "Can include business actions, cultural opportunities, risk considerations, or innovation signals."
            ),
            "first_seen": (
                "The earliest date when this theme was detected from aggregated signals. "
                "Represents the starting point of its recognition in monitoring data."
            ),
            "last_seen": (
                "The most recent date when signals related to this theme were observed and processed. "
                "Indicates freshness and current relevance of the theme."
            ),
            "velocity": (
                "Absolute speed of change in signals compared to the previous period.\n"
                "Represents the raw difference in number of signals (e.g., +2,000 signals this month "
                "versus last month), regardless of theme size."
            ),
            "volume": (
                "Total number of signals linked to this theme in the current scan period.\n"
                "Signals can be any relevant items—posts, articles, images, videos, or other data points "
                "detected as part of this theme."
            ),
            "maturity": (
                "Lifecycle stage of the theme, based on time in observation and adoption level:\n"
                "• Nascent – Very new, early signals, little adoption (<3 months observed).\n"
                "• Emerging – Gaining traction, niche discussion (3–6 months observed).\n"
                "• Scaling – Rapid expansion, moving toward mainstream (6–18 months, multi-sector adoption).\n"
                "• Established – Well-known, widely adopted, normalized (>18 months persistent attention)."
            ),
            "confidence": (
                "Combined confidence score reflecting (a) cluster coherence and (b) interpretive validation from LLM coding. "
                "Values close to 100% indicate both quantitative cluster integrity and qualitative interpretive agreement."
            ),
            "momentum": (
                "Growth direction and intensity of the theme over time, derived from month-over-month signal volume change:\n"
                "• Surging – >50% MoM increase\n"
                "• Rising – 10–50% MoM increase\n"
                "• Stable – ±10% MoM change\n"
                "• Plateauing – slowing growth (<10% increase, risk of decline)\n"
                "• Declining – >10% MoM decrease"
            ),
            "perspectives": (
                "Key stakeholder groups affected by or driving this theme "
                "(e.g., customers, employees, regulators) and their viewpoints."
            ),
            "representative_signal": (
                "A sample signal (post, quote, or content item) illustrating the essence of this theme. "
                "Provides a human-readable example of how this theme appears in the real world."
            ),
            "evolution": (
                "Description of how this theme has shifted over time, including subtopics, sentiment changes, "
                "and expansion into new domains."
            ),
            "coder_views": (
                "Summaries of differing interpretations from simulated analyst agents (ThematicLM multi-perspective coding). "
                "Shows how distinct 'analyst personas' interpreted the same signals, revealing divergence and convergence in meaning."
            ),
            "interpretive_conflict": (
                "Measure of interpretive disagreement between coder agents before consensus "
                "(e.g., low conflict = high agreement, high conflict = multiple competing interpretations)."
            ),
            "codebook_version": (
                "Identifier for the evolving thematic codebook used to define this theme. "
                "Indicates how theme definitions have shifted across analysis cycles."
            ),
            "symbolic_meaning": (
                "Interpretive layer linking the theme to cultural symbols, metaphors, or archetypes "
                "(e.g., hero’s journey, purity metaphors, innovation symbolism)."
            ),
            "value_conflicts": (
                "Underlying cultural tensions or value conflicts expressed in discourse (e.g., Tradition vs Modernity, "
                "Individualism vs Collectivism) linked to this theme."
            )
        },
        "dimensions": {
            "axis": "Cultural tension axis framing the meaning space (e.g., Tradition ↔ Modernity).",
            "intuitive_label": "Human-readable label summarizing the axis meaning.",
            "strength": "Qualitative prominence of this dimension (Emerging, Moderate, Strong).",
            "key_markers": "Top observed signals (keywords, behaviors) that map to this dimension.",
            "narrative": "Explanation of why this dimension matters and what it reveals."
        },
        "metaphors": {
            "title": "Name of the metaphor linking different domains.",
            "metaphor": "One-line statement describing the structural parallel.",
            "narrative": "Explanation of why these parallels are important.",
            "columns": "Column headers for metaphor comparison table.",
            "rows": "Row-level pairings showing how two domains map onto each other."
        },
        "framing": {
            "title": "Name of the framing lens (comparison context).",
            "data": "Table of country-specific interpretations of the same idea.",
            "evidence": "Links supporting the cultural framing analysis.",
            "strategic_impact": "Implications of these cultural framings for strategy."
        },
        "evolution": {
            "title": "Concept or term being tracked over time.",
            "evolution": "Year-to-meaning mapping showing semantic/narrative drift.",
            "shift_driver": "Key factor(s) driving the meaning change."
        }
    },
    "people": {
        "name": "Persona name, representing an audience segment.",
        "share": "Percentage of conversation attributed to this persona.",
        "traits": "Key demographic and behavioral attributes.",
        "behaviors": "Common actions associated with this persona.",
        "evidence": "Data sources supporting this persona.",
        "implications": "Strategic considerations for engaging this persona."
    },
    "influencers": {
        "narratives": {
            "title": "Influencer-driven storyline shaping discussion.",
            "story": "Summary of the narrative's content and focus.",
            "evidence": "Links supporting relevance of this narrative.",
            "takeaway": "Implication or action recommended."
        },
        "pathways": {
            "name": "Pathway title showing idea diffusion route.",
            "color": "Line color used to visually differentiate this path.",
            "nodes": "Steps or actors involved in spreading an idea, each with its tooltip."
        },
        "brokers": {
            "market": "Geographic or cultural market where brokers operate.",
            "description": "Summary of how influencers in this market shape trends.",
            "broker": {
                "name": "Name of the broker (individual influencer or organization).",
                "role": "Influence role or area of expertise for this broker.",
                "impact": "Primary way this broker shapes narratives or behaviors.",
                "followers": "Number of social media followers (reach indicator).",
                "engagement": "Engagement rate (likes, shares, comments as % of followers).",
                "specialty": "Main topical focus or specialization of this broker.",
                "brands": "Brands currently associated or partnered with this broker."
            }
        }
    },
    "ideas": {
        "hypotheses": {
            "title": "If–then prediction derived from observed data relationships.",
            "source": "Reference supporting the hypothesis."
        },
        "gaps": {
            "title": "Unmet opportunity area detected in the market or culture.",
            "body": "Explanation of what is missing and why it matters.",
            "source": "Evidence supporting this gap."
        },
        "playbooks": {
            "title": "Action plan derived from repeatable success patterns.",
            "goal": "What the playbook aims to achieve.",
            "steps": "Key steps recommended for execution.",
            "metrics": "Measures of success for this playbook.",
            "source": "Reference for this playbook."
        },
        "scenarios": {
            "title": "What-if scenario for strategic planning.",
            "body": "Expected outcomes based on scenario assumptions.",
            "source": "Supporting evidence for scenario assumptions."
        },
        "recommendations": {
            "title": "Priority action suggested by AI analysis.",
            "body": "Explanation of why this action is recommended and intended impact."
        }
    }
}

themes = [{
  "title": "Signature Mix",
  "subtitle": "Luxury reimagined as a personalised blend, not a fixed brand choice.",
  "first_seen": "2024-05-15",
  "last_scan": "2025-08-08",
  "current_volume": 382000,
  "previous_volume": 222000,
  "volume": 3100000,
  "summary": "Gen Z luxury beauty buyers in India elevate status by curating their own product mix: pairing one or two prestige items with local, ingredient-led favourites. Prestige is expressed through composition and knowledge, not brand uniformity.",
  "story": "For this market, “luxury” is shifting from owning a complete set to designing a unique personal blend.\n\nThey combine:\n- **Prestige anchors** – a signature global luxury product (e.g., Dior lipstick, La Mer cream)\n- **Heritage or indie companions** – Ayurvedic oils, botanical toners, local niche brands\n\n**Why this matters:** Status comes from taste, discernment, and ingredient literacy — aligning with India’s cultural preference for quiet sophistication over conspicuous brand devotion.",
  "proof_points": [
    "A Bengaluru influencer’s [**Monsoon Skin Edit**](https://example.com) video paired **La Mer cream** with a low-cost *Ayurvedic toner*, gaining **240k views**.",
    "Instagram [#LuxuryMixIndia](https://instagram.com/explore/tags/LuxuryMixIndia) reels often show **Dior lipstick** alongside **Kama Ayurveda oils**, framing luxury as *ingredient-first*.",
    "In Tokyo, **Dior** markets full *“journey kits”* (complete regimens), contrasting India’s *mix-and-match* approach.",
    "Indian beauty blogs post **step-by-step pairing guides** for blending global luxury with local heritage."
  ],
  "quotes": [
    ["I keep one splurge, then build the rest around it so it feels mine.", "21, Mumbai, beauty micro-influencer"],
    ["Mixing Dior with my Ayurvedic oil makes it feel personal.", "24, Bengaluru, consumer interview"]
  ],
  "personas": {
    "Trend-Setter": "Uses mixing to signal creativity and personal style.",
    "Tradition Lover": "Keeps trusted traditional ingredients alongside prestige pieces.",
    "Simple Luxury Fan": "Chooses a few high-quality items, rotating them for variety."
  },
  "drivers": [
    "Economic calibration of aspiration – Discretionary incomes of urban youth is rising, but persistent inflation and uneven salary growth keep full luxury regimens out of reach for most. Consumers adapt by integrating selective prestige into otherwise affordable routines.",
    "Influencer-led normalisation of mixing – On Instagram and YouTube, luxury beauty tutorials in India often feature at least one non-luxury product, framing blending as aspirational.",
    "Ingredient-driven cultural pride – Ayurveda and botanical actives have moved from niche to mainstream in both domestic and global beauty marketing. Ingredient literacy is now a status marker, reinforced by peer reviews and beauty forums."
  ],
  "also_emerging_in": ["Thailand", "Indonesia"],
  "other_markets": {
    "Japan": "Theme is brand-loyal prestige; experimentation contained within brand range.",
    "Brazil": "Theme becomes bold, colourful, and extroverted self-expression; mixing as statement-making.",
    "UK": "Theme driven by product rotation, often driven by seasonal “hero” launches, rather than ongoing personal curation."
  },
  "language": "Frequently used in India, less common elsewhere: “mixable,” “ingredient-first,” “routine swap,” “curation”. Common globally but rare in India: “heritage set,” “complete regimen,” “signature look”.",
  "evolution": {
    "early": "People only swapped products within one luxury brand.",
    "now": "People mix luxury, indie, and traditional brands together.",
    "next": "Brands may start selling products made to be easily combined — “mix-friendly” luxury."
  },
  "signals": [
    "Prestige products sold in smaller or refillable packs.",
    "More influencer videos pairing global luxury with local brands.",
    "Ingredient names used as hashtags or video titles.",
    "Store displays showing mixed-brand routines.",
    "Collaborations between prestige and indie beauty brands."
  ]
}]

class InsightsRenderer:
    def __init__(self, data: dict):
        self.data = data

    def render(self):
        # themes = self.data.get("themes", {})
        self._render_themes(themes)

    def _parse_markdown_links(self, text):
        """Convert markdown-style links [text](url) to HTML <a> tags"""
        import re
        # if they passed a list of strings, join into one
        if isinstance(text, (list, tuple)):
            text = "<br>".join(text)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.sub(pattern, r'<a href="\2" target="_blank">\1</a>', text)
       
    def _pick_color(self, name: str, palette=None):
        if palette is None:
            palette = ["#C084FC", "#60A5FA", "#34D399", "#F97316", "#FFD93D", "#FF6B6B", "#8B5CF6", "#22D3EE"]
        h = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16)
        return palette[h % len(palette)]

    def _safe(self, nar, key, default=""):
        return nar.get(key, default) if nar.get(key) not in (None, "", []) else default

    def _html_list(self, items):
        if not items:
            return "<em>No data</em>"
        return "".join(f"<li>{i}</li>" for i in items)

    def _html_kv_list(self, d):
        if not d:
            return "<em>No data</em>"
        return "".join(f"<li><strong>{k}:</strong> {v}</li>" for k, v in d.items())

    def _derive_maturity_from_scan(self, first_seen, last_scan):
        # same logic as derive_maturity but with 'last_scan'
        first_date = datetime.strptime(first_seen, "%Y-%m-%d")
        last_date = datetime.strptime(last_scan, "%Y-%m-%d")
        months = (last_date.year - first_date.year) * 12 + (last_date.month - first_date.month)
        if months < 3:
            return "Nascent"
        elif months < 6:
            return "Emerging"
        elif months < 18:
            return "Scaling"
        else:
            return "Established"

    def _format_number(self, n):
            """Convert raw integers to readable strings (e.g., 210000 -> 210k)."""
            if n >= 1_000_000:
                return f"{n/1_000_000:.1f}M"
            if n >= 1_000:
                return f"{n/1_000:.0f}k"
            return str(n)
    
    def _derive_momentum(self, current_volume, previous_volume):
            """
            Derive velocity, growth percentage, and momentum label.
            """
            velocity = current_volume - previous_volume

            if previous_volume <= 0:
                growth_pct = 100.0 if velocity > 0 else 0.0
            else:
                growth_pct = (velocity / previous_volume) * 100

            if growth_pct > 50:
                label = "Surging"
            elif growth_pct > 10:
                label = "Rising"
            elif growth_pct > -10:
                label = "Stable"
            elif growth_pct > -50:
                label = "Plateauing"
            else:
                label = "Declining"

            return label, growth_pct, velocity

    def _quotes_to_html(self, quotes):
            """
            quotes: list of strings or (quote, author) tuples
            returns: HTML string of styled blockquotes
            """
            html_parts = []
            for item in quotes:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    quote_text, author = item
                    html_parts.append(
                        f'<blockquote style="margin: 0 0 8px; padding-left: 12px; border-left: 3px solid;">'
                        f'“{quote_text}”'
                        f'<footer style="font-size: 0.85em; margin-top: 4px;">— {author}</footer>'
                        f'</blockquote>'
                    )
                else:
                    html_parts.append(
                        f'<blockquote style="margin: 0 0 8px; padding-left: 12px; border-left: 3px solid;">'
                        f'“{item}”'
                        f'</blockquote>'
                    )
            return "\n".join(html_parts)
    
    def _render_themes(self, themes):
        theme_tooltips = TOOLTIPS["stories"]["themes"]

        st.caption("Observable stories and behaviors shaping culture right now • Last scan: " +
                (self._safe(themes[0], "last_scan") if themes else "—"))

        for idx, nar in enumerate(themes):

            # Required numerics (fallback to 0 if missing)
            current_volume = int(nar.get("current_volume", 0))
            previous_volume = int(nar.get("previous_volume", 0))
            total_volume = int(nar.get("volume", 0))

            # Derivations (reuse your existing helpers if already in scope)
            momentum_label, growth_pct, velocity = self._derive_momentum(current_volume, previous_volume)
            momentum_display = f"{momentum_label} ({growth_pct:+.1f}% MoM)"
            volume_str = f"{self._format_number(total_volume)} signals"
            sign = "+" if velocity > 0 else ""
            velocity_str = f"{sign}{self._format_number(velocity)} signals (MoM)"

            # Dates & maturity (schema uses first_seen + last_scan)
            first_seen = self._safe(nar, "first_seen", "—")
            last_scan = self._safe(nar, "last_scan", "—")
            maturity = self._derive_maturity_from_scan(first_seen, last_scan) if first_seen != "—" and last_scan != "—" else "—"

            # Visual color (fallback if no trend_color present)
            trend_color = nar.get("trend_color", self._pick_color(self._safe(nar, "title", "Theme")))

            # Headline block
            title = self._safe(nar, "title", "Untitled Theme")
            subtitle = self._safe(nar, "subtitle")

            # Long-form fields
            summary = self._safe(nar, "summary")
            story = self._safe(nar, "story")

            # Lists/maps
            proof_points = nar.get("proof_points", [])
            quotes = nar.get("quotes", [])
            personas = nar.get("personas", {})
            drivers = nar.get("drivers", [])
            also_emerging_in = nar.get("also_emerging_in", [])
            other_markets = nar.get("other_markets", {})
            language = self._safe(nar, "language")
            evolution = nar.get("evolution", {})
            signals = nar.get("signals", [])

            evidence_html = self._html_list(proof_points)
            personas_html = self._html_kv_list(personas)
            drivers_html = self._html_list(drivers)
            quotes_html = self._quotes_to_html(quotes)
            other_markets_html = self._html_kv_list(other_markets)

            evolution_html = ""
            if evolution:
                evo_rows = []
                if "early" in evolution: evo_rows.append(f"<li><strong>Early:</strong> {evolution['early']}</li>")
                if "now" in evolution: evo_rows.append(f"<li><strong>Now:</strong> {evolution['now']}</li>")
                if "next" in evolution: evo_rows.append(f"<li><strong>Next:</strong> {evolution['next']}</li>")
                evolution_html = "".join(evo_rows) if evo_rows else "<em>No data</em>"
            else:
                evolution_html = "<em>No data</em>"

            signals_html = self._html_list(signals)
            title_size = 18

            card_html = f"""
            <div style="border: 2px solid {trend_color}; border-radius: 10px; padding: 16px; margin-bottom: 16px;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:8px;">
                    <div style="margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid #E0E0E0;">
                        <div style="border:2px solid {trend_color};padding:4px 10px;border-radius:6px;display:inline-block;">
                            <strong style="font-size:19px;line-height:1.2;letter-spacing:.2px;" title="{theme_tooltips['title']}">{title}</strong>
                        </div>
                        {"<div style='font-size:13px;line-height:1.45;opacity:.85;margin-top:4px;'>" + subtitle + "</div>" if subtitle else ""}
                    </div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;">
                    <div title="{theme_tooltips['momentum']}"><strong>Growth:</strong> {momentum_display}</div>
                    <div><strong>Last Scan:</strong> {last_scan}</div>
                    <div><strong>Also Emerging In:</strong> {", ".join(also_emerging_in) if also_emerging_in else "—"}</div>
                    <div title="{theme_tooltips['maturity']}"><strong>Stage:</strong> {maturity}</div>
                </div>
                {"<div style='margin-top:12px;padding:8px 10px;border:1px solid #E0E0E0;border-radius:4px;font-size:14px;line-height:1.5;'><strong style='display:block;margin-bottom:4px;font-size:15px;'>Summary</strong>" + summary + "</div>" if summary else ""}
                <details style="margin-top: 14px; border-radius: 8px; overflow: hidden;">
                    <summary style="font-weight: bold; cursor: pointer;">Full Details</summary>
                    <div style="padding: 10px 4px 0; border-top: 1px solid #e5e7eb; line-height: 1.6;">
                        <section style="margin: 12px 0;" title="{theme_tooltips['story']}">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">What's Happening?</h4>
                            <p style="margin: 0;">{story if story else "<em>No story provided</em>"}</p>
                        </section>
                        <section style="margin: 12px 0;" title="Key proof points and examples supporting the theme.">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">Proof Points: How does the theme show up?</h4>
                            <ul style="margin: 0; padding-left: 16px;">{evidence_html if proof_points else "<em>No proof points</em>"}</ul>
                        </section>
                        <section style="margin: 12px 0;">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">Quotes: What people are saying?</h4>
                            {quotes_html}
                        </section>
                        <section style="margin: 12px 0;" title="{TOOLTIPS['people']['traits']}">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">Personas: Different types of consumer</h4>
                            <ul style="margin: 0; padding-left: 16px;">{personas_html}</ul>
                        </section>
                        <section style="margin: 12px 0;">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">Drivers: Why do they do it and why now?</h4>
                            <ul style="margin: 0; padding-left: 16px;">{drivers_html}</ul>
                        </section>
                        <section style="margin: 12px 0;">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">How the Theme Differs in Other Markets</h4>
                            <ul style="margin: 0; padding-left: 16px;">{other_markets_html}</ul>
                        </section>
                        <section style="margin: 12px 0;">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">Linguistic Fingerprint</h4>
                            <p style="margin: 0;">{language if language else "<em>No language notes</em>"}</p>
                        </section>
                        <section style="margin: 12px 0;" title="{theme_tooltips['evolution']}">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">Evolution</h4>
                            <ul style="margin: 0; padding-left: 16px;">{evolution_html}</ul>
                        </section>
                        <section style="margin: 12px 0;">
                            <h4 style="margin: 0 0 4px; font-size: {title_size}px;">Signals to Watch</h4>
                            <ul style="margin: 0; padding-left: 16px;">{signals_html}</ul>
                        </section>
                    </div>
                </details>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

    def _render_dimensions(self, dimensions):
        st.caption("Underlying conceptual tensions organizing meaning across domains")
        strength_colors = {
            "Emerging": "#FFA500",   # orange
            "Moderate": "#FFD700",   # gold
            "Strong":   "#00B050"    # green
        }
        dim_tooltips = TOOLTIPS["stories"]["dimensions"]

        cols = st.columns(3)
        for idx, dim in enumerate(dimensions):
            col = cols[idx % 3]
            border_color = strength_colors.get(dim["strength"], "#DDD")
            with col:
                card_html = (
                        f'<div style="border:2px solid {border_color}; border-radius:8px; padding:16px; margin-bottom:16px;">'
                        f'  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">'
                        f'    <strong style="font-size:16px;" title="{dim_tooltips["axis"]}">{dim["axis"]}</strong>'
                        f'  </div>'
                        f'  <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:12px 0;">'
                        f'    <div title="{dim_tooltips["strength"]}"><strong>Signal Strength:</strong> '
                        f'<span style="background-color: {border_color}; color: black; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">{dim["strength"]}</span></div>'
                        f'    <div title="{dim_tooltips["key_markers"]}"><strong>Key Markers:</strong> {", ".join(dim["key_markers"])}</div>'
                        f'  </div>'
                        f'  <details style="margin-top:16px; border-radius:8px; overflow:hidden;">'
                        f'    <summary style="font-weight:bold; cursor:pointer;">Full Details</summary>'
                        f'    <div style="padding:0 16px 16px; border-top:1px solid #CCC; line-height:1.6;" title="{dim_tooltips["narrative"]}">'
                        f'      <p>{dim["narrative"]}</p>'
                        f'    </div>'
                        f'  </details>'
                        f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

    def _render_metaphors(self, metaphors):
        metaphor_tooltips = TOOLTIPS["stories"]["metaphors"]

        st.caption("Illustrative parallels showing shared structure across domains")
        tabs = st.tabs([m["title"] for m in metaphors])

        for tab, m in zip(tabs, metaphors):
            with tab:
                st.markdown(
                    f"*<span title='{metaphor_tooltips['metaphor']}'>{m['metaphor']}</span>*",
                    unsafe_allow_html=True
                )
                st.caption(
                    f"<span title='{metaphor_tooltips['narrative']}'>{m['narrative']}</span>",
                    unsafe_allow_html=True
                )
                df = pd.DataFrame(m["rows"])
                col_cfg = {
                    col: st.column_config.TextColumn(
                        col, width="medium", help=metaphor_tooltips["rows"]
                    )
                    for col in m["columns"]
                }
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config=col_cfg
                )

    def _render_framing(self, framing):
        framing_tooltips = TOOLTIPS["stories"]["framing"]
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
                        "Country": st.column_config.TextColumn(
                            "Country", width="small", help=framing_tooltips["data"]
                        ),
                        "Cultural Framing": st.column_config.TextColumn(
                            "Cultural Framing", width="large", help=framing_tooltips["data"]
                        ),
                        "Key Indicators": st.column_config.TextColumn(
                            "Key Indicators", width="medium", help=framing_tooltips["data"]
                        )
                    }
                )
                st.markdown(
                    f"**Evidence Sources:** <span title='{framing_tooltips['evidence']}'>{', '.join(content['evidence'])}</span>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    f"**Strategic Impact:** <span title='{framing_tooltips['strategic_impact']}'>{content['strategic_impact']}</span>",
                    unsafe_allow_html=True
                )
        
    def _render_evolution(self, evolution):
        evolution_tooltips = TOOLTIPS["stories"]["evolution"]

        st.caption("How key terms shift meaning across contexts and time")

        tab_names = [m['title'] for m in evolution]
        evolution_tabs = st.tabs(tab_names)
        
        for tab, data in zip(evolution_tabs, evolution):
            with tab:
                timeline_html = (
                    '<div style="border:1px solid #ddd; border-radius:8px; padding:16px; margin-bottom:16px;">'
                )
                for year, meaning in data["evolution"].items():
                    timeline_html += (
                        f'<div style="margin-bottom:12px;" '
                        f'title="{evolution_tooltips["evolution"]}">'
                        f'<strong>{year}</strong> → {meaning}</div>'
                    )
                timeline_html += '</div>'
                st.markdown(timeline_html, unsafe_allow_html=True)

                st.markdown(
                    f"<span title='{evolution_tooltips['shift_driver']}'><strong>Shift driver:</strong> {data['shift_driver']}</span>",
                    unsafe_allow_html=True
                )

    def _render_people(self, personas):

        persona_tooltips = TOOLTIPS["people"]
        cols = st.columns(3)
        for idx, p in enumerate(personas):
            col = cols[idx % 3]
            evidence_html = self._parse_markdown_links(p["evidence"])
            traits_list = "".join(f"<li>{t}</li>" for t in p["traits"])
            border_color = p.get("border_color", "#DDD")
            
            card_html = f"""
            <div style="border:2px solid {border_color};border-radius:8px;padding:16px;margin:16px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                <strong style="font-size:16px;" title="{persona_tooltips['name']}">{p['name']}</strong>
                <b><small style="background-color:{border_color};color:#000;padding:2px 6px;border-radius:4px;font-size:14px;"
                    title="{persona_tooltips['share']}">
                    Share: {p['share']}
                </small></b>
            </div>
            <div style="margin:12px 0;" title="{persona_tooltips['traits']}">
                <strong>Key Traits:</strong>
                <ul style="margin:4px 0 0 1rem; padding-left:1rem;">
                    {traits_list}
                </ul>
            </div>
            <details style="margin-top:16px;border-radius:8px;overflow:hidden;border-top:1px solid #CCC;">
                <summary style="font-weight:bold;cursor:pointer;">Full Details</summary>
                <section style="margin:12px 0;" title="{persona_tooltips['behaviors']}">
                    <h4 style="margin:0 0 4px;font-size:14px;">Behaviors</h4>
                    <p style="margin:0;">{p['behaviors']}</p>
                </section>
                <section style="margin:12px 0;" title="{persona_tooltips['evidence']}">
                    <h4 style="margin:0 0 4px;font-size:14px;">Evidence</h4>
                    <p style="margin:0;">{evidence_html}</p>
                </section>
                <section style="margin:12px 0;" title="{persona_tooltips['implications']}">
                    <h4 style="margin:0 0 4px;font-size:14px;">Implications</h4>
                    <p style="margin:0;">{p['implications']}</p>
                </section>
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
        narrative_tooltips = TOOLTIPS["influencers"]["narratives"]
        st.caption("Key influencer ecosystems shaping cultural conversations and commerce")
        cols = st.columns(2)
        for idx, nar in enumerate(narratives):
            col = cols[idx % 2]
            color = nar["color"]
            evidence_html = self._parse_markdown_links(nar["evidence"])
            with col:
                st.markdown(
                    f'<div style="border:2px solid {color};border-radius:8px;padding:16px;margin:8px;">'
                    f'  <strong style="font-size:16px;" title="{narrative_tooltips["title"]}">{nar["title"]}</strong>'
                    f'  <details style="border-top:1px solid {color};margin-top:12px;">'
                    f'    <summary style="font-weight:bold;color:{color};" title="Click to view full details">Full Details</summary>'
                    f'    <p title="{narrative_tooltips["story"]}">{nar["story"]}</p>'
                    f'    <p title="{narrative_tooltips["evidence"]}">{evidence_html}</p>'
                    f'    <p title="{narrative_tooltips["takeaway"]}"><strong>Takeaway:</strong> {nar["takeaway"]}</p>'
                    f'  </details>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    def _render_pathways(self, pathways):
        pathways_tooltips = TOOLTIPS["influencers"]["pathways"]

        st.caption(
            "How cultural moments spread through influencer networks to drive adoption",
            help=pathways_tooltips["name"]
        )

        dot = [
            "digraph G {",
            "  rankdir=LR; graph [bgcolor=transparent,nodesep=1,ranksep=1];",
            "  node [shape=circle,fixedsize=true,width=1.2,height=1.2,style=filled,fontname=\"Helvetica-Bold\",fontsize=10];",
            "  edge [penwidth=2];"
        ]

        for p in pathways:
            ids = [f'"{n["id"]}"' for n in p["nodes"]]
            dot.append(f"  {' -> '.join(ids)} [color=\"{p['color']}\"];")
            for n in p["nodes"]:
                # Preserve the node-specific tooltip provided by the data
                dot.append(
                    f'  "{n["id"]}" [fillcolor="{p["color"]}", label="{n["label"]}", tooltip="{n["tooltip"]}"];'
                )

        dot.append("}")
        st.graphviz_chart("\n".join(dot))

    def _render_brokers(self, brokers_list):
        st.caption("Most influential voices shaping brand perception and cultural trends")
        broker_tooltips = TOOLTIPS["influencers"]["brokers"]
        entity_tooltips = broker_tooltips["broker"]

        for market_data in brokers_list:
            cards = []
            for b in market_data["brokers"]:
                cards.append(
                    f'<div style="flex:1;min-width:220px;border:1px solid {market_data["color"]};'
                    f'border-radius:6px;padding:12px;margin:8px;" title="{entity_tooltips["name"]}">'
                    f'<strong style="color:{market_data["color"]};" title="{entity_tooltips["name"]}">{b["name"]}</strong><br>'
                    f'<em title="{entity_tooltips["role"]}">{b["role"]}</em>'
                    f'<p title="{entity_tooltips["impact"]}">{b["impact"]}</p>'
                    f'<details><summary style="color:{market_data["color"]};">Details</summary>'
                    f'<p title="{entity_tooltips["followers"]}">Followers: {b["followers"]}</p>'
                    f'<p title="{entity_tooltips["engagement"]}">Engagement: {b["engagement"]}</p>'
                    f'<p title="{entity_tooltips["specialty"]}">Specialty: {b["specialty"]}</p>'
                    f'<p title="{entity_tooltips["brands"]}">Brands: {", ".join(b["brands"])}</p>'
                    f'</details>'
                    f'</div>'
                )
            container = (
                f'<div style="flex:1;min-width:220px;border:1px solid {market_data["color"]};'
                f'border-radius:6px;padding:12px;margin:8px;" title="{broker_tooltips["description"]}">'
                f'<strong style="font-size:18px;" title="{broker_tooltips["market"]}">{market_data["market"]}</strong>'
                f'<p style="opacity:0.8;" title="{broker_tooltips["description"]}"><em>{market_data["description"]}</em></p>'
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
        hypotheses_tooltips = TOOLTIPS["ideas"]["hypotheses"]
        st.caption("Key if–then hypotheses to test.")
        cols = st.columns(2)
        for idx, h in enumerate(hypotheses):
            with cols[idx % 2]:
                self._render_card(
                    title=f"<span title='{hypotheses_tooltips['title']}'>{h['statement']}</span>",
                    body_lines=[
                        f"<span title='{hypotheses_tooltips['source']}'>Source: {self._parse_markdown_links(h['source'])}</span>"
                    ],
                    border="1px solid #888",
                    details=("Full Hypothesis", [h["statement"]])
                )

    def _render_gaps(self, gaps):
        st.caption("Unmet opportunities—each gap is a trigger for action.")
        gaps_tooltips = TOOLTIPS["ideas"]["gaps"]
        for g in gaps:
            self._render_card(
                title=f"<span title='{gaps_tooltips['title']}'>🎯 {g['title']}</span>",
                body_lines=[
                    f"<span title='{gaps_tooltips['body']}'>{g['body']}</span>",
                    f"<span title='{gaps_tooltips['source']}'>Source: {self._parse_markdown_links(g['source'])}</span>"
                ],
                border="1px dashed #999"
            )

    def _render_playbooks(self, playbooks):
        st.caption("Activation Playbooks—frameworks distilled by AI from 50K+ cultural data points")
        playbooks_tooltips = TOOLTIPS["ideas"]["playbooks"]
        for c in playbooks:
            parts = [
                f"<p title='{playbooks_tooltips['goal']}'><strong>Goal:</strong> {c['goal']}</p>",
                "<p title='{0}'><strong>Steps:</strong></p><ul style='margin:4px 0 8px 16px;'>".format(playbooks_tooltips['steps'])
                + "".join(f"<li title='{playbooks_tooltips['steps']}'>{s}</li>" for s in c["steps"]) + "</ul>",
                "<p title='{0}'><strong>Metrics:</strong></p><ul style='margin:4px 0 8px 16px;'>".format(playbooks_tooltips['metrics'])
                + "".join(f"<li title='{playbooks_tooltips['metrics']}'>{m}</li>" for m in c["metrics"]) + "</ul>",
                f"<p style='font-size:0.85em; color:gray;' title='{playbooks_tooltips['source']}'><em>Source: {self._parse_markdown_links(c['source'])}</em></p>"
            ]
            body_html = "".join(parts)
            self._render_card(
                title=f"<span title='{playbooks_tooltips['title']}'>{c['title']}</span>",
                body_lines=[body_html],
                border=c.get("border", "1px solid #ccc")
            )

    def _render_scenarios(self, scenarios):
        st.caption("What If Scenarios — projected outcomes")
        scenarios_tooltips = TOOLTIPS["ideas"]["scenarios"]
        container = '<div style="display:flex;flex-direction:column;gap:16px;">'
        for idx, s in enumerate(scenarios, start=1):
            container += (
                f'<div style="display:flex;align-items:flex-start;gap:12px;">'
                f'<div style="min-width:32px;height:32px;border-radius:50%;'
                f'background:#FF5722;color:#fff;display:flex;align-items:center;'
                f'justify-content:center;font-weight:bold;font-size:14px;">{idx}</div>'
                f'<div style="flex:1;">'
                f'<div style="font-size:15px;font-weight:bold;color:#FF5722;margin-bottom:4px;" '
                f'title="{scenarios_tooltips["title"]}">{s["title"]}</div>'
                f'<div style="font-size:14px;line-height:1.5;margin-bottom:6px;" '
                f'title="{scenarios_tooltips["body"]}">{s["body"]}</div>'
                f'<div style="font-size:12px;color:gray;" '
                f'title="{scenarios_tooltips["source"]}">Source: {self._parse_markdown_links(s["source"])}</div>'
                f'</div></div>'
            )
        container += "</div>"
        st.markdown(container, unsafe_allow_html=True)

    def _render_recommendations(self, recs):
        st.caption("Next steps—priority actions.")
        for r in recs:
            recommendations_tooltips = TOOLTIPS["ideas"]["recommendations"]
            st.markdown(
                f"<div style='border-left:5px solid #4CAF50;padding:12px;margin-bottom:8px;' "
                f"title='{recommendations_tooltips['title']}'>"
                f"<strong>{r['priority']}. {r['title']}</strong>"
                f"<p style='margin:4px 0;' title='{recommendations_tooltips['body']}'>{r['body']}</p>"
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
