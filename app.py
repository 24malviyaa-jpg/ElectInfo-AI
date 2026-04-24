import streamlit as st
from agent import run_agent
from judge import evaluate_response

st.set_page_config(
    page_title="ElectInfo — Election & Candidate Guide",
    page_icon="🗳️",
    layout="centered"
)

st.title("🗳️ ElectInfo")
st.caption("Your AI-powered guide to elections, candidates, and voting information. Ask anything.")

st.divider()

st.markdown("**Try asking:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("🇮🇳 2024 Indian general election results", use_container_width=True):
        st.session_state["query"] = "What were the results of the 2024 Indian general election?"
    if st.button("👤 Who is Narendra Modi?", use_container_width=True):
        st.session_state["query"] = "Who is Narendra Modi and what are his key policies?"
with col2:
    if st.button("🇺🇸 US 2024 presidential candidates", use_container_width=True):
        st.session_state["query"] = "Who were the main candidates in the 2024 US presidential election?"
    if st.button("🗓️ Upcoming elections 2025", use_container_width=True):
        st.session_state["query"] = "What are the major upcoming elections in 2025?"

st.divider()

query = st.text_area(
    "Ask your election or candidate question",
    value=st.session_state.get("query", ""),
    placeholder="e.g. Who won the Maharashtra state elections? / What are BJP's key policies?",
    height=100
)

if st.button("🔍 Search & Analyze", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a question about elections or candidates.")
    else:
        with st.spinner("🌐 Searching election databases and news sources..."):
            result = run_agent(query)

        st.subheader("📋 Answer")
        st.markdown(result["answer"])

        with st.expander("📎 Sources used"):
            for i, src in enumerate(result.get("sources", []), 1):
                st.markdown(f"{i}. [{src['title']}]({src['url']})")

        st.divider()

        with st.spinner("🧑‍⚖️ Evaluating answer quality..."):
            judgment = evaluate_response(query, result["answer"])

        st.subheader("🧑‍⚖️ LLM-as-Judge Evaluation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Relevance", f"{judgment['relevance']}/10")
        with col2:
            st.metric("Accuracy", f"{judgment['accuracy']}/10")
        with col3:
            st.metric("Clarity", f"{judgment['clarity']}/10")

        st.info(f"**Overall Score:** {judgment['overall']}/10\n\n**Feedback:** {judgment['feedback']}")

        st.caption("⚠️ For informational purposes only. Always verify from official election commission sources.")