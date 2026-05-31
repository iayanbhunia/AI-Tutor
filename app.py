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
            f"Generate exactly {num_questions} {education_level}-level {subject} quiz questions about: {user_input}\n\n"
            "STRICT RULES - follow exactly:\n"
            "1. Each question MUST be on its own line starting with Q1. Q2. etc.\n"
            "2. Each option MUST be on its own separate line.\n"
            "3. The correct answer line MUST be on its own line.\n"
            "4. Do NOT put multiple items on the same line.\n\n"
            "Use EXACTLY this format for every question, with each part on a new line:\n\n"
            "Q1. <question text here>\n"
            "A) <first option>\n"
            "B) <second option>\n"
            "C) <third option>\n"
            "D) <fourth option>\n"
            "[CORRECT] A) <brief explanation why A is correct>\n\n"
            "Q2. <next question>\n"
            "A) ...\n"
            "B) ...\n"
            "C) ...\n"
            "D) ...\n"
            "[CORRECT] B) <brief explanation>\n\n"
            f"Now generate all {num_questions} questions following this exact format. "
            "Every option on its own line. No combining lines."
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

if "quiz_answers" not in st.session_state:
    # Stores user's selected answer per question key
    # key: "{message_index}_{question_index}", value: selected letter e.g. "A"
    st.session_state.quiz_answers = {}


# ── Quiz Parser ───────────────────────────────────────────────────────────────

import re

def parse_quiz(text: str) -> list[dict]:
    """
    Parse a quiz response into structured question blocks.
    Handles both multiline format and inline format as fallback.
    """
    questions = []

    # Normalise — replace common inline separators the model might use
    text = text.replace(" A) ", "\nA) ").replace(" B) ", "\nB) ")
    text = text.replace(" C) ", "\nC) ").replace(" D) ", "\nD) ")
    text = text.replace(" [CORRECT]", "\n[CORRECT]")

    # Split into question blocks on Q1. Q2. etc.
    blocks = re.split(r'(?=Q\d+\.)', text.strip())

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        q_match = re.match(r'Q\d+\.\s*(.+)', block)
        if not q_match:
            continue

        question_text = q_match.group(1).strip()

        # Extract [CORRECT] line first before option parsing
        correct_match = re.search(r'\[CORRECT\]\s*([A-D])\)\s*(.+)', block)
        correct_letter = correct_match.group(1).strip() if correct_match else None
        explanation = correct_match.group(2).strip() if correct_match else None

        # Remove [CORRECT] line so it doesn't pollute option parsing
        block_clean = re.sub(r'\[CORRECT\].*', '', block)

        # Parse options — anchored to start of line
        options = {}
        for letter in ["A", "B", "C", "D"]:
            opt_match = re.search(rf'^{letter}\)\s*(.+)', block_clean, re.MULTILINE)
            if opt_match:
                options[letter] = opt_match.group(1).strip()

        if question_text and len(options) >= 2 and correct_letter:
            questions.append({
                "question": question_text,
                "options": options,
                "correct": correct_letter,
                "explanation": explanation,
            })

    return questions


def render_quiz(questions: list[dict], msg_index: int):
    """Render interactive quiz questions with hidden answers."""
    for q_index, q in enumerate(questions):
        key = f"{msg_index}_{q_index}"
        st.markdown(f"**Q{q_index + 1}. {q['question']}**")

        selected = st.session_state.quiz_answers.get(key)

        if selected is None:
            # Show option buttons
            cols = st.columns(4)
            for i, letter in enumerate(["A", "B", "C", "D"]):
                if letter in q["options"]:
                    if cols[i].button(
                        f"{letter}) {q['options'][letter]}",
                        key=f"btn_{key}_{letter}",
                        use_container_width=True,
                    ):
                        st.session_state.quiz_answers[key] = letter
                        st.rerun()
        else:
            # Show result banner
            if selected == q["correct"]:
                st.success("🎉 Correct!")
            else:
                st.error(f"❌ Wrong! The correct answer is **{q['correct']}**.")

            # Show all options with correct/wrong highlighting
            for letter in ["A", "B", "C", "D"]:
                if letter not in q["options"]:
                    continue
                option_text = f"{letter}) {q['options'][letter]}"
                if letter == q["correct"]:
                    st.success(f"✅ {option_text}")
                elif letter == selected:
                    st.error(f"❌ {option_text}")
                else:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{option_text}")

            # Show explanation
            if q["explanation"]:
                st.info(f"💡 **Explanation:** {q['explanation']}")

        st.markdown("---")


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

    # FREE TEXT subject input — type anything
    custom_subject = st.text_input(
        "Enter a subject",
        placeholder="e.g. Math, Physics, Economics, Law...",
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
        st.session_state.quiz_answers = {}
        st.rerun()


# ── Chat History Display ──────────────────────────────────────────────────────

for msg_index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and message.get("is_quiz"):
            questions = parse_quiz(message["content"])
            if questions:
                render_quiz(questions, msg_index)
            else:
                st.markdown(message["content"])
        else:
            st.markdown(message["content"])


# ── Chat Input & Response ─────────────────────────────────────────────────────

chat_placeholder = (
    f"Enter a topic to generate {num_questions} question{'s' if num_questions > 1 else ''}..."
    if mode == "Generate a Quiz"
    else f"Ask a {subject} question..."
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

        # Show a loading hint for multi-question quizzes
        if mode == "Generate a Quiz" and num_questions > 1:
            message_placeholder.markdown(f"⏳ Generating {num_questions} questions, please wait...")

        full_response = ""

        # Build prompt via extracted function
        system_prompt = build_prompt(
            mode, education_level, subject, prompt, num_questions
        )

        # Pass full conversation history so the model has context
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

            message_placeholder.empty()

            # Render quiz interactively, or show plain text for explain mode
            if mode == "Generate a Quiz":
                questions = parse_quiz(full_response)
                if questions:
                    render_quiz(questions, len(st.session_state.messages))
                else:
                    message_placeholder.markdown(full_response)
            else:
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

        # Save assistant reply to session history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "is_quiz": mode == "Generate a Quiz",
        })
