# Local AI Email Summarizer (Powered by Ollama)

This project is a **local-running AI Agent** that connects to your Gmail inbox, fetches emails from the past week, and generates a **clear and organized summary** using a local **Ollama LLM model** (like `llama3.2`).

It’s built for **privacy, automation, and simplicity** — all data is processed locally, and no external AI APIs are used.

---

## Features

- **Runs entirely locally** — your emails never leave your machine.
- **Uses Ollama** (e.g., `llama3.2`) to summarize messages intelligently.
- **Fetches only the past week’s emails** from your Gmail inbox.
- **Cleans and normalizes** text before summarization.
- Easily extendable to email yourself the weekly summary automatically.

---

## 🧩 How It Works

1. The script authenticates with Gmail using OAuth2 (Google API).
2. It retrieves all emails from the past 7 days.
3. Email content (subject, sender, body) is extracted and cleaned.
4. The emails are structured and sent to a **local Ollama model** for summarization.
5. The AI returns a concise summary that you can print, log, or email to yourself.

