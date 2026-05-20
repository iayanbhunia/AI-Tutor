# 🤝 Contributing to AI Tutor

Thank you for being part of the AI Tutor project! This guide helps every team member work consistently and avoid conflicts.

---

## 📋 Table of Contents

- [Getting Started](#-getting-started)
- [Branch Naming Rules](#-branch-naming-rules)
- [Making Changes](#-making-changes)
- [Running the Project Locally](#-running-the-project-locally)
- [Running Tests](#-running-tests)
- [Opening a Pull Request](#-opening-a-pull-request)
- [Code Style Guidelines](#-code-style-guidelines)
- [Commit Message Format](#-commit-message-format)
- [Reporting Bugs](#-reporting-bugs)

---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/iayanbhunia/AI-Tutor.git
   cd AI-Tutor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama and pull a model**
   ```bash
   ollama pull gemma3
   ollama serve
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🌿 Branch Naming Rules

Always create a new branch before making changes. **Never push directly to `main`.**

| Type | Format | Example |
|------|--------|---------|
| New feature | `feature/short-description` | `feature/score-tracker` |
| Bug fix | `fix/short-description` | `fix/empty-prompt-crash` |
| Documentation | `docs/short-description` | `docs/update-readme` |
| Tests | `test/short-description` | `test/quiz-prompt-cases` |
| Refactor | `refactor/short-description` | `refactor/build-prompt` |

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name
```

---

## ✏️ Making Changes

1. Make sure you are on your own branch, not `main`
2. Make small, focused commits — one change per commit
3. Test your changes locally before pushing
4. Pull the latest `main` before opening a PR to avoid conflicts:
   ```bash
   git pull origin main
   ```

---

## 🖥️ Running the Project Locally

```bash
# Activate virtual environment
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# Start Ollama
ollama serve

# Run the app
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🧪 Running Tests

Always run tests before opening a pull request:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

Make sure **all tests pass** and coverage stays **above 80%**.

If you add a new feature, add tests for it in `tests/test_app.py`.

---

## 🔀 Opening a Pull Request

1. Push your branch to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to the repository on GitHub and click **"Compare & pull request"**

3. Fill in the PR description:
   - **What did you change?**
   - **Why did you change it?**
   - **How was it tested?**

4. Request a review from at least **one team member**

5. Do not merge your own PR — let another team member review and merge

---

## 🎨 Code Style Guidelines

- Follow **PEP 8** — use `flake8` to check:
  ```bash
  pip install flake8
  flake8 app.py
  ```
- Use **meaningful variable names** — `subject`, `education_level` not `s`, `el`
- Add **docstrings** to every function:
  ```python
  def build_prompt(mode, education_level, subject, user_input, num_questions=1):
      """Build a subject/level-aware prompt based on the selected mode."""
  ```
- Keep functions **small and focused** — one function, one job
- Remove **unused imports** before committing

---

## 📝 Commit Message Format

Use clear, consistent commit messages:

```
type: short description
```

| Type | When to use |
|------|-------------|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug |
| `docs` | Documentation changes |
| `test` | Adding or updating tests |
| `refactor` | Code cleanup without changing behaviour |
| `chore` | Minor tasks (removing files, updating deps) |

**Examples:**
```bash
git commit -m "feat: add quiz question count slider"
git commit -m "fix: handle empty subject input"
git commit -m "docs: update README with new subject input"
git commit -m "test: add edge cases for build_prompt"
git commit -m "chore: remove unused imports"
```

---

## 🐛 Reporting Bugs

If you find a bug:

1. Check if it's already reported in [GitHub Issues](https://github.com/iayanbhunia/AI-Tutor/issues)
2. If not, open a new issue with:
   - **What happened?**
   - **What did you expect?**
   - **Steps to reproduce**
   - **Your OS and Python version**

---

## 📞 Questions?

Reach out to the team via:
- 📧 Email: [imayan0904@gmail.com](mailto:imayan0904@gmail.com)
- 💬 [GitHub Discussions](https://github.com/iayanbhunia/AI-Tutor/discussions)
