import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from research_pipeline import run_research_pipeline

# Configure Streamlit page for a clean, minimal UI
st.set_page_config(
    page_title="Agentic Research Lab",
    page_icon="🔬",
    layout="wide"
)

# App Title
st.title("🔬 Agentic Research Lab")
st.markdown("An **Autonomous Research Assistant** that plans, searches ArXiv, stores papers, and synthesizes insights using RAG.")

# Section 1: Research Query
st.header("1. Research Query")
query = st.text_input("Enter your complex research question or topic:", placeholder="e.g., How does multi-agent reinforcement learning improve swarm robotics?")
start_button = st.button("Initialize Autonomous Agent")

if start_button:
    if not query.strip():
        st.warning("Please enter a research query to start.")
    else:
        with st.spinner("🤖 Agent is Planning, Searching, Reading, and Analyzing..."):
            try:
                # Run the updated agentic pipeline (now returns papers, report, and the plan)
                papers, report, plan = run_research_pipeline(user_query=query)
                
                st.divider()
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Section: Planner's Thoughts
                    st.header("🧠 Agentic Planner")
                    st.info(f"**Understanding:**\n{plan.get('understanding', 'N/A')}")
                    st.markdown("**Generated Search Queries:**")
                    for q in plan.get('search_queries', []):
                        st.markdown(f"- `{q}`")
                        
                    st.divider()
                    
                    # Section: Retrieved Papers
                    st.header("📚 Sourced Literature")
                    if papers:
                        st.caption(f"Retrieved {len(papers)} unique papers based on planner queries.")
                        for i, paper in enumerate(papers, 1):
                            with st.expander(f"{i}. {paper['title']}"):
                                st.markdown(f"**Authors:** {', '.join(paper['authors'])}")
                                st.markdown(f"**Link:** [{paper['pdf_link']}]({paper['pdf_link']})")
                                st.markdown(f"**Abstract:** {paper['abstract']}")
                    else:
                        st.warning("No papers were retrieved.")

                with col2:
                    # Section: AI Insights and Research Opportunities
                    st.header("💡 Final Synthesis")
                    st.markdown("### 🔍 Analysis Report")
                    
                    # Render the Gemini markdown response directly
                    st.markdown(report)
                
            except Exception as e:
                st.error(f"An error occurred during the research process: {e}")
                st.info("Ensure that 'GOOGLE_API_KEY' is correctly configured in your environment vars.")
