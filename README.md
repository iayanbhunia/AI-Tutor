# 🎓 AI Tutor - Smart Learning Assistant

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-green.svg)](https://ollama.ai/)

A powerful, privacy-focused AI tutoring application that runs entirely on your local machine. Get personalized explanations and generate custom quizzes across multiple subjects without sending any data to external servers.


## ✨ Features

### 🎯 **Personalized Learning**
- **Multiple Education Levels**: School, High School, UG, PG, PhD
- **Any Subject**: Type any subject freely — Math, History, Law, Economics, and more
- **Adaptive Explanations**: Content complexity adjusts to your education level

### 🤖 **Dual Learning Modes**
- **Explain a Topic**: Get detailed, step-by-step explanations with examples
- **Generate a Quiz**: Create interactive multiple-choice quizzes — options appear as clickable buttons, correct answer and explanation are revealed only after you select an option

### 🔒 **100% Privacy**
- **Local Processing**: All AI computations happen on your device
- **No Data Transfer**: Your questions and conversations never leave your machine
- **Offline Capable**: Works without internet once models are downloaded

### 🧠 **Multiple AI Models**
- **Gemma3**: Google's latest model, optimized for educational content (recommended)
- **Gemma2**: Lightweight alternative, good for lower-resource machines
- **Llama3**: Meta's powerful general-purpose model
- **Mistral**: Fast and efficient general-purpose model
- **DeepSeek Coder**: Specialized for programming and computer science
- **Auto-Detection**: Automatically discovers all installed Ollama models and prioritizes by educational performance

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running ([Download Ollama](https://ollama.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/iayanbhunia/AI-Tutor.git
   cd AI-Tutor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install AI models** (choose one or more)
   ```bash
   # Recommended: Gemma3 (best for general education)
   ollama pull gemma3
   
   # For coding and computer science
   ollama pull deepseek-coder
   
   # Alternative general-purpose model
   ollama pull llama3
   ```

4. **Start Ollama server** (if not already running)
   ```bash
   ollama serve
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and navigate to `http://localhost:8501`

## 🎮 How to Use

### 1. Configure Your Learning Preferences
- **Education Level**: Select your current academic level (defaults to **High School**)
- **Subject**: Type any subject you want to study (e.g. Math, Physics, Economics, Law) — defaults to **General** if left blank
- **Mode**: Pick between explanation or quiz generation
- **Number of Questions**: In quiz mode, choose 1–10 questions (defaults to **3**)
- **AI Model**: The app will automatically detect and list available models

### 2. Ask Questions or Request Topics
- **Explanation Mode**: "Explain photosynthesis" or "How does machine learning work?"
- **Quiz Mode**: Type a topic and get an interactive quiz:
  - A, B, C, D appear as **clickable buttons**
  - After selecting, buttons are replaced with ✅ correct / ❌ wrong highlights
  - 🎉 or ❌ result banner shown instantly
  - 💡 Explanation revealed only after answering

### 3. Interactive Learning
- Get detailed explanations with examples
- Answer quiz questions interactively with instant feedback
- Correct answers and explanations are hidden until you choose
- Build on previous conversations for deeper understanding

## 📁 Project Structure

```
AI-Tutor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── .gitignore           # Git ignore rules
├── assets/              # Images and media
│   └── demo.gif         # Application demo
├── docs/                # Additional documentation
│   ├── installation.md  # Detailed installation guide
│   ├── usage.md         # Usage examples and tips
│   └── troubleshooting.md # Common issues and solutions
├── config/              # Configuration files
│   └── models.yaml      # Model configuration
└── tests/               # Test files
    └── test_app.py      # Unit tests
```

## 🧩 Core Modules

### 1. **Model Detection (`get_available_models()`)**
- Automatically discovers installed Ollama models
- Handles different API response formats
- Prioritizes models based on educational performance
- Provides fallback options and error handling

### 2. **Education Level Adaptation**
- Adjusts explanation complexity based on selected level
- Customizes vocabulary and examples
- Scales problem difficulty appropriately

### 3. **Subject-Specific Prompting**
- Accepts any subject typed freely by the user
- Incorporates subject context into AI prompts
- Provides relevant examples and analogies for any topic

### 4. **Streaming Response Handler**
- Real-time response display with a live `▌` cursor while generating
- Handles connection errors gracefully
- Provides visual feedback during generation
- Shows a loading message for multi-question quizzes

### 5. **Quiz Parser (`parse_quiz()`)**
- Parses AI response into structured question blocks
- Handles both multiline and inline response formats as fallback
- Extracts question, A–D options, correct letter, and explanation separately
- Strips `[CORRECT]` from view until the user answers

### 6. **Interactive Quiz Renderer (`render_quiz()`)**
- Renders each question with four clickable option buttons
- Reveals ✅ correct / ❌ wrong highlights after selection
- Shows 💡 explanation only after an answer is chosen
- Tracks answers per question in session state so they persist across reruns

### 7. **Session Management**
- Maintains conversation history across turns
- Tracks quiz answers per question (`quiz_answers` state)
- Preserves context across interactions
- Enables follow-up questions and clarifications
- Clearing conversation also resets all quiz answer state

## 🔧 Configuration

### Model Priority
The application prioritizes models in the following order:
1. `gemma3:latest` - Best for general education
2. `gemma3`
3. `gemma2:2b` - Lightweight alternative
4. `gemma2`
5. `llama3` - Reliable general-purpose alternative
6. `mistral` - Fast general-purpose model
7. `deepseek-coder` - Optimal for programming topics

### Custom Model Configuration
Edit `config/models.yaml` to customize model preferences:

```yaml
preferred_models:
  - "gemma3:latest"
  - "deepseek-coder"
  - "llama3"
```

## 🛠️ Development

### Setting up Development Environment

1. **Fork the repository**
2. **Create a virtual environment**
   ```bash
   python -m venv ai-tutor-env
   source ai-tutor-env/bin/activate  # On Windows: ai-tutor-env\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run tests**
   ```bash
   pytest tests/
   ```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Maintain test coverage above 80%

## 🐛 Troubleshooting

### Common Issues

**"No Ollama models found"**
- Ensure Ollama is running: `ollama serve`
- Check installed models: `ollama list`
- Install a model: `ollama pull gemma3`

**Connection errors**
- Verify Ollama is accessible on default port (11434)
- Check firewall settings
- Restart Ollama service

**Performance issues**
- Use smaller models for better speed
- Ensure sufficient RAM (8GB+ recommended)
- Close unnecessary applications

See [docs/troubleshooting.md](docs/troubleshooting.md) for detailed solutions.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📖 Improve documentation
- 🧪 Add test cases
- 🎨 Enhance UI/UX

## 📊 Performance Metrics

| Model | Size | Speed | Education Quality |
|-------|------|-------|------------------|
| Gemma3 | 3.3GB | Fast | ⭐⭐⭐⭐⭐ |
| DeepSeek Coder | 776MB | Very Fast | ⭐⭐⭐⭐ (CS Topics) |
| Llama3 | 4.7GB | Medium | ⭐⭐⭐⭐ |

## 🗺️ Roadmap

- [ ] **Multi-language Support** - Add support for multiple languages
- [ ] **Voice Integration** - Voice-to-text and text-to-voice
- [ ] **Progress Tracking** - Learning progress and analytics
- [ ] **Study Plans** - Automated curriculum generation
- [ ] **Collaborative Learning** - Share sessions with classmates
- [ ] **Mobile App** - Native mobile applications

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for providing the local AI infrastructure
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Google](https://ai.google.dev/) for the Gemma model family
- [DeepSeek](https://deepseek.com/) for the specialized coding model

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/iayanbhunia/AI-Tutor/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/iayanbhunia/AI-Tutor/discussions)
- 📧 **Email**: [Contact Us](mailto:imayan0904@gmail.com)

---

<div align="center">
  <p>Made with ❤️ for learners everywhere</p>
  <p>⭐ Star this repo if you find it helpful!</p>
</div>
