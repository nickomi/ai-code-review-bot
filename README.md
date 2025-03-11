# AI Code Review Bot

## Overview
An AI-powered bot that automatically reviews GitHub pull requests, detects code issues, and provides feedback as comments.

## Features
- Analyzes pull request diffs using OpenAI GPT-4
- Posts AI-generated code reviews as GitHub comments
- GitHub Action to trigger automatic reviews on PR creation
- Web dashboard to track past reviews

## Tech Stack
- **Backend:** FastAPI, OpenAI API, GitHub API
- **Frontend:** React (Dashboard)
- **CI/CD:** GitHub Actions
- **Database:** PostgreSQL (optional for logging reviews)

## Setup

### 1️⃣ Backend Setup
```bash
# Clone repository
git clone https://github.com/your-repo/ai-code-review-bot.git
cd ai-code-review-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GITHUB_TOKEN=your_github_token
export OPENAI_API_KEY=your_openai_key

# Run the server
uvicorn main:app --reload
```

### 2️⃣ GitHub Action Setup
1. Copy `.github/workflows/code-review.yml` to your repo.
2. Update the API endpoint in the workflow.

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm start
```

## Usage
- Open a pull request on GitHub.
- The bot automatically reviews it and comments with feedback.
- Check the web dashboard for historical reviews.

## License
MIT

