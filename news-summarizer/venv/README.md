# 📰 Real-Time AI News Summarizer & Chat

An interactive, real-time news summarization and Q&A application built using **Streamlit**, **LangChain**, **Tavily Search**, and **Groq (Llama 3)**.

## 🚀 Features

- **Real-Time News Fetching:** Uses the Tavily API to fetch the latest, up-to-date news articles across the web on any given topic.
- **Smart Summarization:** Powered by Groq's blazing fast Llama 3 model, it generates a concise, professional summary of the fetched news.
- **Customizable Output:** Choose how you want your news delivered:
  - Executive Summary
  - Twitter Thread with Emojis
  - 5 Crisp Bullet Points
  - Detailed Analysis
- **Sentiment & Category Analysis:** Automatically detects the sentiment (e.g., Bullish/Bearish, Positive/Negative) and category (Tech, Finance, etc.) of the news.
- **Chat with the News:** A built-in ChatGPT-like interface allows you to ask follow-up questions directly related to the live news context.

## 🛠️ Tech Stack

- **UI Framework:** [Streamlit](https://streamlit.io/)
- **LLM Engine:** [Groq](https://groq.com/) (`llama3-8b-8192`)
- **Orchestration:** [LangChain](https://www.langchain.com/) (`langchain_core`)
- **Search API:** [Tavily Search API](https://tavily.com/)

## 📂 Project Structure

```text
news-summarizer/
├── venv/
│   ├── app.py              # Main Streamlit application and UI logic
│   ├── rag_pipeline.py     # LangChain RAG logic, Tavily Search, and Chat integration
│   ├── requirements.txt    # Python dependencies
│   ├── .env                # Environment variables (API Keys)
│   └── README.md           # Project Documentation
```

## ⚙️ Installation & Setup

1. **Clone the repository or navigate to the project folder:**
   ```bash
   cd news-summarizer/venv
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables:**
   Create a `.env` file in the same directory and add your API keys:
   ```env
   tavily_api_key=your_tavily_api_key_here
   groq_api_key=your_groq_api_key_here
   ```

## 🏃‍♂️ How to Run

Start the Streamlit development server by running:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## 💡 Usage

1. Enter a news topic in the search bar (e.g., "AI breakthroughs", "SpaceX").
2. Select your preferred output style from the sidebar.
3. Click **Summarize** to fetch and generate the news report.
4. Expand the **"View Raw Articles"** section to see the source content.
5. Use the **Chat Interface** at the bottom to ask specific follow-up questions about the fetched news.

---
*Built with ❤️ using AI*
