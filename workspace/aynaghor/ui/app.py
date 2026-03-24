
import streamlit as st
import sys
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.engine import Engine

# Page configuration
st.set_page_config(
    page_title="AYNAGH0R - Dark Fantasy AI",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #8B4513;
        font-family: 'Serif';
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .story-container {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #8B4513;
        margin: 10px 0;
    }
    .status-indicator {
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
    }
    .status-healthy { background-color: #2d5a2d; color: #90EE90; }
    .status-warning { background-color: #5a4d2d; color: #FFD700; }
    .status-error { background-color: #5a2d2d; color: #FF6B6B; }
</style>
""", unsafe_allow_html=True)

# Initialize the engine
@st.cache_resource
def get_engine():
    return Engine()

# Main title
st.markdown('<h1 class="main-header">🌙 AYNAGH0R 🌙</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="main-header">Dark Fantasy AI Storyteller</h3>', unsafe_allow_html=True)

# Sidebar for configuration and status
with st.sidebar:
    st.header("⚙️ Configuration")

    # Engine status
    engine = get_engine()
    health_status = engine.health_check()

    st.subheader("🔮 Engine Status")

    if health_status["clients"]["gemini"]["initialized"]:
        if health_status["clients"]["gemini"]["healthy"]:
            st.markdown('<div class="status-indicator status-healthy">🟢 Gemini: Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-warning">🟡 Gemini: Initialized</div>', unsafe_allow_html=True)
    elif health_status["use_gemini"]:
        st.markdown('<div class="status-indicator status-error">🔴 Gemini: Not Configured</div>', unsafe_allow_html=True)

    if health_status["clients"]["localai"]["initialized"]:
        if health_status["clients"]["localai"]["healthy"]:
            st.markdown('<div class="status-indicator status-healthy">🟢 LocalAI: Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-warning">🟡 LocalAI: Initialized</div>', unsafe_allow_html=True)
    elif not health_status["use_gemini"]:
        st.markdown('<div class="status-indicator status-error">🔴 LocalAI: Not Configured</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Story settings
    st.subheader("📖 Story Settings")
    story_length = st.selectbox(
        "Story Length",
        ["Short (100-200 words)", "Medium (300-500 words)", "Long (500-800 words)"],
        index=1
    )

    story_mood = st.selectbox(
        "Mood & Atmosphere",
        ["Mysterious", "Gothic Horror", "Epic Fantasy", "Cosmic Horror", "Medieval Dark", "Supernatural"],
        index=0
    )

    include_dialogue = st.checkbox("Include Dialogue", value=True)
    include_description = st.checkbox("Rich Descriptions", value=True)

    st.markdown("---")

    # Quick prompts
    st.subheader("⚡ Quick Prompts")
    if st.button("🏰 Haunted Castle"):
        st.session_state.quick_prompt = "A traveler approaches an ancient, haunted castle on a stormy night"
    if st.button("🌲 Dark Forest"):
        st.session_state.quick_prompt = "Lost in a dark enchanted forest where shadows whisper secrets"
    if st.button("🗡️ Cursed Artifact"):
        st.session_state.quick_prompt = "An archaeologist discovers a cursed artifact with terrible power"
    if st.button("👻 Ghostly Encounter"):
        st.session_state.quick_prompt = "A medium encounters a restless spirit seeking justice"

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("✍️ Your Story Request")

    # Use quick prompt if selected
    default_prompt = st.session_state.get('quick_prompt', '')
    if default_prompt:
        st.session_state.quick_prompt = ''  # Clear after use

    prompt = st.text_area(
        "Describe the dark fantasy tale you wish to hear...",
        value=default_prompt,
        height=120,
        placeholder="Enter your story prompt here. Be as detailed or as brief as you like - AYNAGH0R will weave your vision into a dark fantasy tale..."
    )

    # Generation controls
    col_gen1, col_gen2, col_gen3 = st.columns([1, 1, 2])

    with col_gen1:
        generate_btn = st.button("🌙 Generate Story", type="primary", use_container_width=True)

    with col_gen2:
        if st.button("🔄 Clear", use_container_width=True):
            st.rerun()

    with col_gen3:
        st.caption(f"Using: {'Gemini API' if health_status['use_gemini'] else 'Local AI'}")

with col2:
    st.subheader("📚 Story History")

    # Initialize story history
    if 'story_history' not in st.session_state:
        st.session_state.story_history = []

    if st.session_state.story_history:
        for i, (timestamp, prompt_text, story_text) in enumerate(reversed(st.session_state.story_history[-5:])):
            with st.expander(f"Story {len(st.session_state.story_history) - i}: {timestamp}"):
                st.write(f"**Prompt:** {prompt_text[:100]}...")
                st.write(f"**Length:** {len(story_text)} characters")
    else:
        st.info("Your generated stories will appear here")

# Story generation
if generate_btn and prompt:
    with st.spinner("🌙 The dark muses are weaving your tale..."):
        try:
            # Add story settings to prompt context
            enhanced_prompt = f"""
            Story Request: {prompt}

            Preferences:
            - Length: {story_length}
            - Mood: {story_mood}
            - Include Dialogue: {include_dialogue}
            - Rich Descriptions: {include_description}
            """

            story = engine.route(enhanced_prompt.strip())

            # Display the story
            st.markdown("---")
            st.subheader("📖 Your Dark Fantasy Tale")
            st.markdown(f'<div class="story-container">{story}</div>', unsafe_allow_html=True)

            # Add to history
            timestamp = datetime.now().strftime("%H:%M")
            st.session_state.story_history.append((timestamp, prompt, story))

            # Keep only last 10 stories
            if len(st.session_state.story_history) > 10:
                st.session_state.story_history = st.session_state.story_history[-10:]

        except Exception as e:
            st.error(f"⚠️ The storytelling spirits encountered an error: {str(e)}")
            logger.error(f"Story generation error: {e}")

elif generate_btn and not prompt:
    st.warning("🌙 Please whisper your story request to AYNAGH0R...")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px;'>
    🌙 AYNAGH0R - Where darkness meets imagination 🌙<br>
    Powered by AI • Built with Streamlit • Created for storytellers
    </div>
    """,
    unsafe_allow_html=True
)
