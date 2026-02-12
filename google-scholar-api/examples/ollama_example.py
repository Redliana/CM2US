"""
Ollama integration example - Using Google Scholar with Phi-4 or other local models.

This uses a prompt-based approach that works with any Ollama model,
including those without native tool calling support.

Install: pip install ollama
Requires: Ollama running locally with phi4 model pulled

Usage:
    export SERPAPI_KEY="your-key"
    uv run python examples/ollama_example.py
"""

import json
import os
import re

from ollama import chat
from scholar import search_scholar, set_api_key

# Set SerpAPI key
set_api_key(os.environ.get("SERPAPI_KEY", "your-serpapi-key"))

SYSTEM_PROMPT = """You are a helpful research assistant with access to Google Scholar search.

When the user asks about academic papers or research, you should request a search by outputting a JSON block like this:

```json
{"action": "search", "query": "your search terms", "num_results": 5, "year_from": 2023}
```

Parameters:
- query: The search terms (required)
- num_results: Number of papers to return (optional, default 5)
- year_from: Only papers from this year onwards (optional)
- year_to: Only papers until this year (optional)

After receiving search results, summarize them helpfully for the user.
If the user's question doesn't require a search, just respond normally."""


def extract_json_block(text: str) -> dict | None:
    """Extract JSON block from model response."""
    # Try to find JSON in code blocks
    json_match = re.search(r"```(?:json)?\s*(\{[^`]+\})\s*```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find raw JSON
    json_match = re.search(r'\{[^{}]*"action"[^{}]*\}', text)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def format_results(results) -> str:
    """Format search results for the model."""
    if results.error:
        return f"Search error: {results.error}"

    output = [f"Found {results.total_results} papers:\n"]
    for i, paper in enumerate(results.papers, 1):
        output.append(f"{i}. {paper.title}")
        output.append(f"   Authors: {paper.authors}")
        output.append(f"   Venue: {paper.venue} ({paper.year})")
        output.append(f"   Citations: {paper.citations}")
        if paper.url:
            output.append(f"   URL: {paper.url}")
        output.append("")

    return "\n".join(output)


def chat_with_scholar(user_message: str, model: str = "phi4") -> str:
    """
    Chat with a local LLM with Google Scholar access.

    Args:
        user_message: The user's question
        model: Ollama model to use (default: phi4)

    Returns:
        The model's response
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    print(f"Sending to {model}...")

    # Get initial response
    response = chat(model=model, messages=messages)
    response_text = response.message.content

    # Check if model wants to search
    action = extract_json_block(response_text)

    if action and action.get("action") == "search":
        print(f"Model requested search: {action.get('query')}")

        # Execute search
        results = search_scholar(
            query=action.get("query", ""),
            year_from=action.get("year_from"),
            year_to=action.get("year_to"),
            num_results=action.get("num_results", 5),
        )

        print(f"Found {results.total_results} papers")

        # Format results and get final response
        formatted = format_results(results)

        messages.append({"role": "assistant", "content": response_text})
        messages.append(
            {
                "role": "user",
                "content": f"Here are the search results:\n\n{formatted}\n\nPlease summarize these findings for the user.",
            }
        )

        print("Getting summary from model...")
        final_response = chat(model=model, messages=messages)
        return final_response.message.content

    return response_text


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Google Scholar + Phi-4 via Ollama")
    print("=" * 60)

    # Example 1: Search for papers
    print("\n--- Query: Recent RAG papers ---\n")
    response = chat_with_scholar("Find recent papers on retrieval augmented generation from 2023")
    print("\n--- Response ---")
    print(response)

    print("\n" + "=" * 60)

    # Example 2: More specific query
    print("\n--- Query: arXiv preprints ---\n")
    response = chat_with_scholar("Search for 3 arXiv preprints about large language models")
    print("\n--- Response ---")
    print(response)
