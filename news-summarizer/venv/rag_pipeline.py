# (langchain +  tavily logic)
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

def build_rag_pipeline():
    search_tool = TavilySearchResults(
        max_results=10
    )

    ### 2. initialize groq llm (blazing fast interface.)
    llm = ChatGroq(
        model="gemma2-9b-it",
        api_key=os.getenv("groq_api_key"),
        temperature=0.3
    )

    # 3. prompts template
    prompt = ChatPromptTemplate.from_template("""
    You are a professional news analyst. Based on the following live news articles,
    provide a comprehensive, structured summary.

    Topic: {topic}
    Output Format: {format_style}

    Live News Data:
    {news_context}

    Please provide the output strictly structured as follows:
    1. **Category:** (e.g., Tech, Finance, Politics, Sports, General)
    2. **Sentiment Analysis:** (Positive/Negative/Neutral or Bullish/Bearish with a 1-sentence reason)
    3. **Main Summary:** (Write this in the requested '{format_style}' format)
    4. **Key Points:** (3-4 crisp bullet points)
    5. **Latest Developments:** (Any breaking updates from the context)
    6. **Sources Referenced:** (List them clearly)

    Keep it factual, concise, and highly professional.
    """)
    
    # 4. Output Parser
    parser = StrOutputParser()
    
    return search_tool, llm, prompt, parser


def fetch_and_summarize(topic: str, format_style: str = "Executive Summary") -> dict:
    search_tool, llm, prompt, parser = build_rag_pipeline()
    
    # Step A: Fetch live news via Tavily
    raw_results = search_tool.invoke({"query": f"{topic} latest news 2025"})
    
    # Step B: Format results into context
    news_context = ""
    sources = []
    for i, result in enumerate(raw_results):
        news_context += f"\n[Article {i+1}]\n"
        news_context += f"Title: {result.get('title', 'N/A')}\n"
        news_context += f"Content: {result.get('content', '')}\n"
        news_context += f"URL: {result.get('url', '')}\n"
        sources.append(result.get('url', ''))
    
    # Step C: Build LangChain chain and run
    chain = prompt | llm | parser
    
    # Run the chain
    summary = chain.invoke({
        "topic": topic,
        "format_style": format_style,
        "news_context": news_context
    })
    
    # Note: To enable streaming, you can use chain.stream(...) in your UI (e.g., Streamlit).
    # For now, it returns the complete response.

    return {
        "summary": summary,
        "sources": sources,
        "raw_articles": raw_results,
        "format_used": format_style
    }

def chat_with_news(question: str, news_context: str, chat_history: list) -> str:
    """
    ChatGPT-like Q&A feature based on the fetched news context.
    """
    llm = ChatGroq(
        model="gemma2-9b-it",
        api_key=os.getenv("groq_api_key"),
        temperature=0.3
    )
    
    prompt = ChatPromptTemplate.from_template("""
    You are an intelligent AI news assistant. Use the provided Live News Context to answer the user's question.
    If the answer is not available in the context, clearly state that the provided news doesn't mention it, but you can share your general knowledge if helpful.

    Live News Context:
    {news_context}

    Conversation History:
    {chat_history}

    User Question: {question}
    
    Provide a clear, helpful, and concise answer.
    """)
    
    parser = StrOutputParser()
    chain = prompt | llm | parser
    
    # Format chat history into a string
    history_str = ""
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "AI"
        history_str += f"{role}: {msg['content']}\n"
        
    answer = chain.invoke({
        "news_context": news_context,
        "chat_history": history_str,
        "question": question
    })
    
    return answer