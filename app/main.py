
import streamlit as st

st.set_page_config(page_title="Healthcare Prior Auth Agent", page_icon="🏥", layout="wide")

st.title("🏥 Multimodal Prior Authorization Agent")

with st.sidebar:
    st.header("Upload Medical Records")
    uploaded_file = st.file_uploader("Upload Prescription/X-Ray", type=['png', 'jpg', 'pdf'])
    
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Medical Record")
    st.info("Agent starting analysis...")
    # TODO: Connect to Agent Workflow here
