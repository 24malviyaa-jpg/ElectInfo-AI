import os
import google.generativeai as genai
from tavily import TavilyClient

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def search_web(query: str) -> dict:
    """Use Tavily to search for election and candidate information."""
    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5,
        include_answer=True,
        topic="news"  # prioritize news sources for election data
    )
    return response


def synthesize_answer(query: str, search_results: dict) -> str:
    """Use Gemini to synthesize a clear, neutral answer from election search results."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    context_parts = []
    for result in search_results.get("results", []):
        context_parts.append(
            f"Source: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n"
        )
    context = "\n---\n".join(context_parts)

    prompt = f"""You are a neutral, factual election information assistant. Using the search results below, provide a comprehensive and balanced answer to the user's question about elections or candidates.

User question: {query}

Search results:
{context}

Instructions:
- Be strictly factual and politically neutral — do not favor any party or candidate
- Include key facts: vote shares, seat counts, candidate backgrounds, policy positions as relevant
- Organize your response clearly with sections if needed
- Cite specific figures and data where available
- Keep the answer informative but concise (200-400 words)
- If the question is about India, use Indian electoral terminology (Lok Sabha, Rajya Sabha, ECI, etc.)

Answer:"""

    response = model.generate_content(prompt)
    return response.text


def run_agent(query: str) -> dict:
    """Main agent pipeline: search → synthesize → return results."""
    search_results = search_web(query)
    answer = synthesize_answer(query, search_results)

    sources = [
        {"title": r.get("title", "Source"), "url": r.get("url", "")}
        for r in search_results.get("results", [])
    ]

    return {
        "answer": answer,
        "sources": sources,
        "raw_search": search_results
    }