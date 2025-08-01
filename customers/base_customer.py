# customers/base_customer.py

import streamlit as st
import time
import json
import pathlib

default_config = {
            "query_placeholder": "What do you want to explore?",
            "internal_url": "https://example.com/internal-assets",
            "default_geographies": ["Global"],
            "default_objective": "Understand consumer behavior",
            "default_segments": ["Urban Millennials"],
            "default_industry": "Consumer Packaged Goods",
            "default_product_types": ["Luxury Couture & Designer Apparel"],
            "default_sources": ["Social: Media Posts", "Behavioral: Web & Trends"],
            "default_modalities": ["Text", "Image"],
            "enable_network_analysis": True
        }

class BaseCustomerRenderer:
    def __init__(self, name, data_path):
        self.name = name
        raw = pathlib.Path(data_path).read_text()
        self.data = json.loads(raw)

    def render_stories(self):
        pass

    def render_people(self):
        pass

    def render_influencers(self):
        pass

    def render_trends(self):
        pass

    def render_ideas(self):
        pass

    def render_ask(self):
        pass

    def render_deep_dive(self):
        pass
