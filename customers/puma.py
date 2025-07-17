# customers/puma.py

import streamlit as st
from customers.base_customer import BaseCustomerRenderer

class Puma(BaseCustomerRenderer):
    def __init__(self):
        config = {
            "query_placeholder": (
                "I want to better understand what’s shaping Puma’s relevance and growth in SEA, based on recent campaigns, social media activity, and cultural signals. " +
                "Specifically, how does Puma balance global consistency with local authenticity? " +
                "Which emerging trends define Puma’s cultural relevance in Thailand, Malaysia, Indonesia?"
            ),
            "internal_url": "https://www.puma.com/",
            "default_geographies": ["Malaysia", "Thailand", "Indonesia"],
            "default_languages": ["Any"],
            "default_segments": ["Urban Millennials", "Gen Z"],
            "default_sources": [
                "Social: Media Posts",
                "Social: Forums & Communities",
                "Behavioral: Web & Trends"
            ],
            "default_modalities": ["Text", "Image"],
            "default_product_types": [
                "Footwear",
                "Athleisure & Activewear",
                "Streetwear & Urban Fashion"
            ],
            "default_industry": "Apparel & Fashion",
            "default_objective": "Identify emerging trends",
            "enable_network_analysis": True
        }
        super().__init__(name="Puma", config=config)
    
    def render_stories(self):
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

    def render_people(self):
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

    def render_influencers(self):
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
        st.markdown("### Strategic Hypotheses")

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


        st.markdown("### Strategic Recommendations (by Cultural Impact Priority)")

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

