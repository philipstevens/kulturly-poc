# customers/morinaga.py

from customers.base_customer import BaseCustomerRenderer
import streamlit as st

class Morinaga(BaseCustomerRenderer):
    def __init__(self):
        config = {
            "query_placeholder": (
                "I want to understand why Morinaga's probiotic infant formula is underperforming in Malaysia—"
                "explore consumer perception, campaign effectiveness, social or parenting media signals."
            ),
            "internal_url": "https://www.morinagamilk.co.jp/english/",
            "default_geographies": ["Malaysia"],
            "default_languages": ["Any"],
            "default_segments": ["New Parents", "Health-conscious consumers"],
            "default_sources": [
                "Social: Media Posts",
                "Behavioral: Reviews & Ratings",
                "Research & Reports: Academic Papers & White Papers"
            ],
            "default_modalities": ["Text", "Audio"],
            "default_product_types": [
                "Infant Formula",
                "Probiotic Supplements",
                "Health & Wellness Food"
            ],
            "default_industry": "Consumer Packaged Goods",
            "default_objective": "Understand consumer behavior",
            "enable_network_analysis": True
        }
        super().__init__(name="Morinaga", config=config)

    def render_stories(self):
        narratives = [
            {
                "title": "Probiotic Awareness Gap",
                "story": "Despite clinical evidence, many Malaysian parents aren't aware of BB536’s health benefits.",
                "evidence": "[NutraIngredients BB536 science](https://www.nutraingredients-asia.com/Article/2019/08/01/Mimicking-mother-s-milk-Morinaga-Milk-Industry-to-focus-on-probiotic-applications-in-infant-formula)",
                "impact": "Deploy pediatric-led education campaigns and translate probiotic science into visual content."
            },
            {
                "title": "Old Brand, Young Doubts",
                "story": "Morinaga has legacy trust but feels outdated vs. competitors like Enfa or Friso.",
                "evidence": "[Morinaga Malaysia heritage](https://morinagamilk.com.my/story.php)",
                "impact": "Modernize packaging and refresh influencer-facing brand kit."
            },
            {
                "title": "Invisible in E‑Commerce",
                "story": "Morinaga probiotic SKUs often look identical to standard formulas online.",
                "evidence": "[HealthLane Morinaga Listings](https://estore.healthlane.com.my/Morinaga)",
                "impact": "Fix product detail pages and emphasize BB536 in visuals and naming."
            }
        ]
        for n in narratives:
            with st.expander(n["title"]):
                st.markdown(f"**Story:** {n['story']}")
                st.markdown(f"**Evidence:** {n['evidence']}")
                st.markdown(f"**Strategic Impact:** {n['impact']}")

    def render_people(self):
        personas = [
            {
                "name": "Millennial Urban Mothers",
                "share": "40%",
                "traits": ["Age 28–38", "Working professional", "Concerned with gut health", "Trust online reviews"],
                "behaviors": "Explore parenting forums, follow pediatrician creators, value science-backed products.",
                "evidence": '<a href="https://www.nutraingredients-asia.com/Trends/Infant-childhood-nutrition" target="_blank">Infant Nutrition Trends</a>',
                "implications": "Feature reviews and science summaries in e-commerce PDPs and mom groups."
            },
            {
                "name": "Health-First Fathers",
                "share": "20%",
                "traits": ["Age 30–45", "Fitness-focused", "Often decision-maker for supplements"],
                "behaviors": "Skim clinical evidence and compare nutritional labels before purchase.",
                "evidence": '<a href="https://www.statista.com/outlook/hmo/dairy-products/milk/infant-formula/malaysia" target="_blank">Infant formula consumption Malaysia</a>',
                "implications": "Build comparisons and authority-driven copy into landing pages and videos."
            }
        ]
        cols = st.columns(2)
        for idx, p in enumerate(personas):
            col = cols[idx % 2]
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

    def render_influencers(self):
        st.markdown("### Cultural Brokers & Influence Hubs")
        influencers = [
            {
                "title": "Parenting Community Leaders",
                "story": "Momfluencers and pediatricians shape infant formula opinions through YouTube, IG, and WhatsApp groups.",
                "evidence": "[YouTube search: BB536 reviews Malaysia](https://www.youtube.com/results?search_query=morinaga+bb536+malaysia)",
                "takeaway": "Engage local pediatric experts and multilingual momfluencers for regional relevance."
            },
            {
                "title": "Pharmacist Educators",
                "story": "Malaysian pharmacists often advise on formula at the point of sale—especially in HealthLane or Caring chains.",
                "evidence": "[Retail channel review – HealthLane Malaysia](https://estore.healthlane.com.my/Morinaga)",
                "takeaway": "Offer shelf‑talkers and QR code training tools to improve pharmacy-led recommendations."
            }
        ]
        for i in influencers:
            with st.expander(i["title"]):
                st.markdown(f"**Story:** {i['story']}")
                st.markdown(f"**Evidence:** {i['evidence']}")
                st.markdown(f"**Strategic Takeaway:** {i['takeaway']}")

    def render_trends(self):
        trends = [
            {
                "title": "Probiotic Formula Boom in SEA",
                "likelihood": "High",
                "metrics": [
                    "Probiotic infant formula CAGR: 11.6% (SEA, 2023–2026)",
                    "BB536 shown to reduce gut infections and eczema risk (RCT 2022)",
                    "Malaysia keyword search rise: +42% for ‘immune boosting milk’"
                ],
                "story": "SEA parents are shifting to gut-health-focused formulas, driven by immunity concerns post-pandemic.",
                "evidence": "[NutraIngredients BB536 trials](https://www.nutraingredients-asia.com/Trends/Infant-childhood-nutrition)",
                "forecast": "By 2026, 1 in 3 infant formulas in Malaysia will market probiotic support prominently.",
                "impact": "Morinaga must lead with BB536 brand education and formulation storytelling."
            }
        ]
        for t in trends:
            with st.expander(f"{t['title']} ({t['likelihood']} Likelihood)"):
                st.markdown(f"**Story:** {t['story']}")
                st.markdown("**Key Metrics:**")
                for m in t["metrics"]:
                    m_safe = m.replace("$", "\\$")
                    st.markdown(f"- {m_safe}")
                st.markdown(f"**Evidence:** {t['evidence']}")
                st.markdown(f"**Forecast:** {t['forecast']}")
                st.markdown(f"**Strategic Impact:** {t['impact']}")

    def render_ideas(self):
        st.markdown("### Strategic Hypotheses")

        hypotheses = [
            {
                "statement": "Emphasizing BB536 on packaging and in digital channels will increase trust and trial conversion by 25% among Malaysian urban mothers.",
                "source": '<a href="https://www.nutraingredients-asia.com/Trends/Infant-childhood-nutrition" target="_blank">Infant nutrition clinical reports</a>'
            },
            {
                "statement": "Partnering with pediatricians and multilingual momfluencers will increase engagement by 40% versus traditional brand ads.",
                "source": '<a href="https://www.youtube.com/results?search_query=morinaga+bb536+malaysia" target="_blank">YouTube influencer content</a>'
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

        st.markdown("### Strategic Recommendations")
        recommendations = [
            {
                "priority": 1,
                "title": "Rebrand BB536 Probiotic SKU",
                "body": "Redesign e-commerce and in-store messaging to clearly spotlight probiotic function and gut health story."
            },
            {
                "priority": 2,
                "title": "Activate Pediatrician & Influencer Network",
                "body": "Equip doctors and trusted momfluencers with content kits to explain BB536’s science in simple, relatable ways."
            },
            {
                "priority": 3,
                "title": "Multilingual Education Campaigns",
                "body": "Run content in Malay, English, and Chinese across parenting forums and video channels to close probiotic awareness gaps."
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
