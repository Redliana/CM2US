#!/usr/bin/env python3
"""
Interactive Google Scholar Chat with Phi-4

An interactive chat where Phi-4 helps you search Google Scholar.
The model will ask what you want to search for and guide you on search format.

Usage:
    uv run python chat.py
"""

from __future__ import annotations

import json
import re

from ollama import chat
from scholar import search_scholar

SYSTEM_PROMPT = """You are a helpful research assistant with access to Google Scholar search.

START by greeting the user and asking what academic topic they'd like to search for. Explain the search format options:

**Search Format Guide:**
- Basic search: Just type your topic (e.g., "machine learning")
- Find preprints: Add "arxiv" (e.g., "transformer models arxiv")
- Conference papers: Add conference name (e.g., "attention mechanism NeurIPS")
- Recent papers: Mention the year (e.g., "RAG papers from 2024")
- Specific field: Add field terms (e.g., "protein folding deep learning")

When the user provides a search request, output a JSON block to execute the search:

```json
{"action": "search", "query": "search terms", "num_results": 5, "year_from": 2023}
```

Parameters:
- query: The search terms (required)
- num_results: Number of papers to return (optional, default 5)
- year_from: Only papers from this year onwards (optional)
- year_to: Only papers until this year (optional)

After receiving results, summarize them clearly and ask if they want to:
- Search for something else
- Refine the search
- Get more details about a specific paper

Be conversational and helpful."""


def extract_json_block(text: str) -> dict | None:
    """Extract JSON block from model response."""
    json_match = re.search(r"```(?:json)?\s*(\{[^`]+\})\s*```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

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
        if paper.snippet:
            output.append(f"   Summary: {paper.snippet[:200]}...")
        output.append("")

    return "\n".join(output)


def main():
    print("=" * 60)
    print("  Google Scholar Chat with Phi-4")
    print("  type 'quit' or 'exit' to end the conversation")
    print("=" * 60)
    print()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Get initial greeting from Phi-4
    print("Phi-4: ", end="", flush=True)
    response = chat(model="phi4", messages=messages)
    assistant_message = response.message.content
    print(assistant_message)
    messages.append({"role": "assistant", "content": assistant_message})
    print()

    while True:
        # Get user input
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye", "q"):
            print("\nPhi-4: Goodbye! Happy researching!")
            break

        # Add user message
        messages.append({"role": "user", "content": user_input})

        # Get response
        print("\nPhi-4: ", end="", flush=True)
        response = chat(model="phi4", messages=messages)
        assistant_message = response.message.content

        # Check if model wants to search
        action = extract_json_block(assistant_message)

        if action and action.get("action") == "search":
            # Show that we're searching
            query = action.get("query", "")
            print(f"[Searching Google Scholar for: {query}...]")
            print()

            # Execute search
            results = search_scholar(
                query=query,
                year_from=action.get("year_from"),
                year_to=action.get("year_to"),
                num_results=action.get("num_results", 5),
            )

            # Add assistant's search request to messages
            messages.append({"role": "assistant", "content": assistant_message})

            # Format results and get summary
            formatted = format_results(results)
            messages.append(
                {
                    "role": "user",
                    "content": f"Here are the search results:\n\n{formatted}\n\nPlease summarize these findings for me.",
                }
            )

            # Get summary from Phi-4
            print("Phi-4: ", end="", flush=True)
            summary_response = chat(model="phi4", messages=messages)
            summary = summary_response.message.content
            print(summary)
            messages.append({"role": "assistant", "content": summary})
        else:
            print(assistant_message)
            messages.append({"role": "assistant", "content": assistant_message})

        print()


if __name__ == "__main__":
    main()
