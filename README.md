# Claude Repo Chat 💬

A lightweight CLI tool built to index local codebases and chat with them using the Anthropic API. 

## Why I built this
As a developer, context-switching between large files is a productivity killer. I built this tool to quickly query my local directories to understand complex functions, find bugs, and generate documentation without leaving the terminal. 

## How I used Claude Code
I used Claude Code to scaffold the entire file-walking logic (`os.walk` implementation) and to quickly generate the error-handling for the API requests. It cut my development time down from a few days to a couple of hours. It is currently helping me refactor the text-chunking logic to handle larger context windows.

## Features
- Recursively scans local directories for `.py`, `.js`, and `.md` files.
- Chunks and sends relevant code context to the Anthropic API.
- Interactive CLI prompt for asking questions about the codebase.

## Tech Stack
- Python 3.10+
- Anthropic SDK
- `rich` (for CLI formatting)
- `python-dotenv`

## Setup
1. Clone the repo: `git clone https://github.com/llero8496-svg/claude-repo-chat.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API key to a `.env` file: `ANTHROPIC_API_KEY=your_key_here`
4. Run the tool: `python main.py`
