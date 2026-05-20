"""
AI Tutor - Smart Learning Assistant

A privacy-focused AI tutoring application that runs entirely on your local machine.
Provides personalized explanations and generates custom quizzes across multiple subjects.

Team: 404 Found
Repository: https://github.com/iayanbhunia/AI-Tutor
"""

import streamlit as st
import ollama
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── Prompt Builder ────────────────────────────────────────────────────────────

def build_prompt(
    mode: str,
    education_level: str,
    subject: str,
    user_input: str,
    num_questions: int = 1,
) -> str:
    """Build a subject/level-aware prompt based on the selected mode."""
    if mode == "Explain a Topic":
        return (
            f"You are a {education_level}-level {subject} tutor.\n"
            f"Explain the following in a structured, step-by-step manner: \"{user_input}\"\n"
            "- Break down complex concepts.\n"
            "- Use examples where helpful.\n"
            "- Keep explanations clear and concise."
        )
    else:  # Quiz mode
        return (
            f"Generate exactly {num_questions} unique {education_level}-level {subject} quiz questions.\n"
            "Format EACH question exactly like this (repeat for every question):\n\n"
            "Q<number>. <question text>\n"
            "A) <option>\n"
            "B) <option>\n"
            "C) <option>\n"
            "D) <option>\n"
            "[CORRECT] <correct letter>) <brief explanation>\n\n"
            f"Topic: {user_input}\n"
            f"- Generate all {num_questions} questions, no more, no less.\n"
            "- Make every question different from the others.\n"
            "- Vary the difficulty slightly across questions.\n"
            "- Do not repeat options or answers across questions."
        )


# ── Model Detection ───────────────────────────────────────────────────────────

@st.cache_data
def get_available_models() -> list[str]:
    """Auto-discover installed Ollama models and sort by preferred educational order."""
    try:
        models_response = ollama.list()
        model_names = []

        if hasattr(models_response, "models"):
            for model in models_response.models:
                if hasattr(model, "model"):
                    model_names.append(model.model)
                elif isinstance(model, dict):
                    name = model.get("name") or model.get("model") or model.get("id")
                    if name:
                        model_names.append(name)
                elif isinstance(model, str):
                    model_names.append(model)
        elif isinstance(models_response, dict) and "models" in models_response:
            for model in models_response["models"]:
                if isinstance(model, dict):
                    name = model.get("name") or model.get("model") or model.get("id")
                    if name:
                        model_names.append(name)
                elif isinstance(model, str):
                    model_names.append(model)

        preferred_order = [
            "gemma3:latest", "gemma3", "gemma2:2b", "gemma2",
            "llama3", "mistral", "deepseek-coder",
        ]
        ordered = [m for m in preferred_order if m in model_names]
        ordered += [m for m in model_names if m not in ordered]
        return ordered

    except Exception as e:
        st.error(f"Error connecting to Ollama: {str(e)}")
        st.info("Make sure Ollama is running: `ollama serve`")
        return []


# ── Session State ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []


# ── Page Title ────────────────────────────────────────────────────────────────

st.title("🎓 Smart Learning Assistant")


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("🎯 Learning Preferences")

    education_level = st.selectbox(
        "Select your education level",
        ["School", "High School", "UG", "PG", "PhD"],
        index=1,
    )

    # Free text subject — no hints, no specific names
    custom_subject = st.text_input(
        "Enter a subject",
        max_chars=50,
    )
    subject = custom_subject.strip() if custom_subject.strip() else "General"
    if not custom_subject.strip():
        st.caption("⚠️ No subject entered — using **General**.")

    mode = st.radio(
        "Select mode",
        ["Explain a Topic", "Generate a Quiz"],
        index=0,
    )

    # Quiz question count slider — only shown in quiz mode
    num_questions = 1
    if mode == "Generate a Quiz":
        num_questions = st.slider(
            "Number of questions",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="How many quiz questions to generate in one go",
        )
        st.caption(f"Will generate **{num_questions}** question{'s' if num_questions > 1 else ''}.")

    st.markdown("---")

    # Refresh models button
    if st.button("🔄 Refresh Models"):
        get_available_models.clear()
        st.rerun()

    available_models = get_available_models()

    if available_models:
        model_name = st.selectbox(
            "AI Model",
            available_models,
            index=0,
            help="Gemma3 is recommended for better performance",
        )
        if "gemma3" in model_name.lower():
            st.success("✅ Using Gemma3 - Excellent choice!")
        elif "deepseek-coder" in model_name.lower():
            st.success("✅ Using DeepSeek Coder - Great for coding tasks!")
        elif not any("gemma3" in m.lower() for m in available_models):
            st.info("💡 Install Gemma3 for best results: `ollama pull gemma3`")
    else:
        st.error("⚠️ No Ollama models found.")
        st.markdown("**Install Gemma3 (recommended):**")
        st.code("ollama pull gemma3", language="bash")
        st.markdown("**Or other models:**")
        st.code("ollama pull llama3\nollama pull deepseek-coder", language="bash")
        model_name = None

    # Clear conversation
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()


# ── Chat History Display ──────────────────────────────────────────────────────

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ── Chat Input & Response ─────────────────────────────────────────────────────

chat_placeholder = (
    f"Enter a topic to generate {num_questions} question{'s' if num_questions > 1 else ''}..."
    if mode == "Generate a Quiz"
    else "Ask a question..."
)

if prompt := st.chat_input(chat_placeholder):

    # Whitespace validation
    if not prompt.strip():
        st.warning("Please enter a question or topic.")
        st.stop()

    if not model_name:
        st.error("Please install an Ollama model first!")
        st.stop()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        if mode == "Generate a Quiz" and num_questions > 1:
            message_placeholder.markdown(f"⏳ Generating {num_questions} questions, please wait...")

        full_response = ""

        system_prompt = build_prompt(
            mode, education_level, subject, prompt, num_questions
        )

        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
        ]
        history.append({"role": "user", "content": system_prompt})

        try:
            response = ollama.chat(
                model=model_name,
                messages=history,
                stream=True,
            )

            for chunk in response:
                full_response += chunk["message"]["content"]
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except ollama.ResponseError:
            error_msg = (
                f"❌ Model `{model_name}` not found. "
                f"Install it with: `ollama pull {model_name}`"
            )
            message_placeholder.markdown(error_msg)
            full_response = error_msg

        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            message_placeholder.markdown(error_msg)
            full_response = error_msg

        st.session_state.messages.append({"role": "assistant", "content": full_response})
