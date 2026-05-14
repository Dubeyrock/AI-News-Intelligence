# AI News Intelligence – Real-Time News Summarizer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1+-green.svg)](https://www.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)

**Bridge the gap between static training data and live current events.**  
This project engineers a real‑time news summarizer using **LangChain**, **live RAG** (Retrieval-Augmented Generation), and high‑speed web search. It extracts insights from the latest news and delivers them through a responsive **Streamlit** application.

---

## 🚀 Features

- **Real‑Time News Fetching** – Integrates with high‑performance search APIs (Tavily / SerpAPI) to get up‑to‑the‑minute articles.
- **RAG Pipeline** – Uses LangChain to retrieve relevant chunks and feed them into an LLM for accurate, context‑aware summarization.
- **LLM Choice** – Works with Groq (for speed) or any OpenAI‑compatible endpoint (GPT, Mistral, Llama).
- **Clean UI** – Streamlit dashboard with search input, summarization, and history.
- **Privacy‑First** – No permanent storage of user queries; API keys managed via environment variables.

---

## 🧰 Tech Stack

| Component          | Technology |
|--------------------|------------|
| Web Search         | Tavily / Google SerpAPI |
| Orchestration      | LangChain |
| LLM (fast)         | Groq (Mixtral 8x7B) or OpenAI GPT‑3.5/4 |
| Vector Store       | FAISS (in‑memory for simplicity) |
| Frontend           | Streamlit |
| Deployment         | Local, Streamlit Cloud, or Docker |

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dubeyrock/AI-News-Intelligence.git
   cd AI-News-Intelligence
