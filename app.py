import streamlit as st
import datetime
import time  
import os
from dotenv import load_dotenv
from customers.puma import Puma
from customers.morinaga import Morinaga

load_dotenv()

is_dev_mode = os.getenv("DEV_MODE", "false").lower() == "true"

CUSTOMER_CLASSES = {
    "Puma": Puma,
    "Morinaga": Morinaga
}

st.set_page_config(layout="wide")

selected_customer_name = "Puma"  # Default selection

if not is_dev_mode:
    with st.sidebar:
        st.subheader("Select Customer Demo")
        selected_customer_name = st.selectbox(
            label=" ",
            options=list(CUSTOMER_CLASSES.keys()),
            index=0 
        )

customer = CUSTOMER_CLASSES[selected_customer_name]()

if "configured" not in st.session_state:
    st.session_state.configured = is_dev_mode  # True in dev, False in production

tab_config = [
    ("Space", "render_context"),      # Always accessible
    ("Stories", "render_stories"),
    ("People", "render_people"),
    ("Drivers", "render_influencers"),
    ("Trends", "render_trends"),
    ("Ideas", "render_ideas"),
    ("Ask", "render_ask"),
    ("Deep Dive", "render_deep_dive")
]

tabs = st.tabs([name for name, _ in tab_config])

for i, (_, method_name) in enumerate(tab_config):
    with tabs[i]:
        if i == 0 or st.session_state.configured:
            getattr(customer, method_name)()
        else:
            st.warning("🔒 Build cultural observatory to unlock this section.")
