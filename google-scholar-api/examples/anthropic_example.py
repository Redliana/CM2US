"""
Anthropic Claude integration example - Using Google Scholar tools with Claude.

Install: pip install anthropic
"""

import os
from anthropic import Anthropic
from scholar import set_api_key, get_anthropic_tools, process_anthropic_tool_use

# Set API keys
set_api_key(os.environ.get("SERPAPI_KEY", "your-serpapi-key"))
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Get the tool definitions in Anthropic format
tools = get_anthropic_tools()


def chat_with_scholar(user_message: str) -> str:
    """
    Chat with Claude with Google Scholar tool access.
    """
    messages = [{"role": "user", "content": user_message}]

    system_prompt = """You are a helpful research assistant with access to Google Scholar.
When searching for papers, always include preprints and conference proceedings.
Search tips:
- Add "arxiv" to queries to find preprints
- Add conference names like "NeurIPS" or "ICML" for proceedings
- Recent preprints may have low citations but contain cutting-edge research
Provide comprehensive literature reviews when asked."""

    # Initial request
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system_prompt,
        tools=tools,
        messages=messages,
    )

    # Process tool use if any
    while response.stop_reason == "tool_use":
        # Find all tool use blocks
        tool_use_blocks = [block for block in response.content if block.type == "tool_use"]

        # Add assistant's response
        messages.append({"role": "assistant", "content": response.content})

        # Execute each tool and collect results
        tool_results = []
        for tool_use in tool_use_blocks:
            result = process_anthropic_tool_use(tool_use)
            tool_results.append(result)

        # Add tool results
        messages.append({"role": "user", "content": tool_results})

        # Get next response
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages,
        )

    # Extract text from final response
    text_blocks = [block.text for block in response.content if hasattr(block, "text")]
    return "\n".join(text_blocks)


# Example usage
if __name__ == "__main__":
    # Example 1: Literature search
    print("=== Literature Search ===")
    response = chat_with_scholar(
        "Find recent papers on retrieval augmented generation from 2023-2024. "
        "Include both arXiv preprints and peer-reviewed papers."
    )
    print(response)

    print("\n" + "=" * 50 + "\n")

    # Example 2: Author lookup
    print("=== Author Lookup ===")
    response = chat_with_scholar(
        "Find information about Yann LeCun on Google Scholar, "
        "including his h-index and most cited papers."
    )
    print(response)
