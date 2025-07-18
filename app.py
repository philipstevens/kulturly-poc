import streamlit as st
import datetime
import time  
from customers.puma import Puma
from customers.morinaga import Morinaga

CUSTOMER_CLASSES = {
    "Puma": Puma,
    "Morinaga": Morinaga
}


# ― Page layout ―
st.set_page_config(layout="wide")

# Place this in sidebar, keep discrete and unstyled
with st.sidebar:
    st.subheader("Select Customer Demo")
    selected_customer_name = st.selectbox(
        label=" ",  # Empty label to minimize visual presence
        options=list(CUSTOMER_CLASSES.keys()),
        index=0  # Default to Puma
    )

customer = CUSTOMER_CLASSES[selected_customer_name]()

# ― State initialization ―
st.session_state.configured = True # default to True for demo purposes, remove for deployment
if "configured" not in st.session_state:
    st.session_state.configured = False


tabs = st.tabs([
    "Space",
    "Stories",
    "People",
    "Drivers",
    "Trends",
    "Ideas"
])

# ― Tab 1: Search & Context Setup ―
with tabs[0]:
    customer.render_context()

# ― Tab 2: Cultural Narratives ―
with tabs[1]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        customer.render_stories()

# ― Tab 3: Personas & Cohorts ―
with tabs[2]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        customer.render_people()

# ― Tab 4: Networks & Influencers ―
with tabs[3]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        customer.render_influencers()

# ― Tab 5: Trends & Forecasts ―
with tabs[4]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        customer.render_trends()

# ― Tab 6: Hypotheses & Recommendations ―
with tabs[5]:
    if not st.session_state.configured:
        st.warning("🔒 Add context and generate insights to unlock this section.")
    else:
        customer.render_ideas()