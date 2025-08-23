import streamlit as st
import os
from src.helper import run_gemini_workflow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Multi-Agent Blog Writer", layout="wide")
st.title("Multi-Agent Blog Content Writer")
st.markdown("This application uses a team of AI agents to write and review a blog post.")

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in .env file. Please add it.")
    st.stop()

with st.form("blog_topic_form"):
    topic = st.text_input("Enter the blog topic:", placeholder="e.g., The Future of Space Exploration")
    word_limit = st.number_input("Enter word limit:", min_value=50, value=100)
    # Add a checkbox to control the visibility of the conversation log
    show_conversation = st.checkbox("Show agent conversation log", value=True)
    submitted = st.form_submit_button("Generate Blog Post")

if submitted:
    if not topic:
        st.warning("Please enter a topic.")
    else:
        task = f"""
        Write a concise yet engaging blog post about "{topic}".
        The blog post should be under {word_limit} words.
        """
        with st.spinner("Agents are collaborating... Please wait."):
            try:
                # The workflow now returns the final post and the conversation log
                final_post, conversation_log = run_gemini_workflow(task, word_limit, api_key)
                
                st.subheader("Final Blog Post:")
                st.markdown(final_post)

                # If the checkbox is ticked, display the conversation log
                if show_conversation:
                    st.subheader("Agent Conversation Log:")
                    with st.expander("Click to view the full conversation"):
                        st.markdown(conversation_log, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.sidebar.header("About")
st.sidebar.info(
    "This application uses a team of AI agents to automate the blog writing process."
)