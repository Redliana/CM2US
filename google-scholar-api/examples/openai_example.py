"""
OpenAI integration example - Using Google Scholar tools with GPT-4.

Install: pip install openai
"""

import os
from openai import OpenAI
from scholar import set_api_key, get_openai_tools, process_openai_tool_call

# Set API keys
set_api_key(os.environ.get("SERPAPI_KEY", "your-serpapi-key"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Get the tool definitions in OpenAI format
tools = get_openai_tools()


def chat_with_scholar(user_message: str) -> str:
    """
    Chat with GPT-4 with Google Scholar tool access.
    """
    messages = [
        {
            "role": "system",
            "content": """You are a helpful research assistant with access to Google Scholar.
When searching for papers, always include preprints and conference proceedings.
Provide comprehensive literature reviews when asked.""",
        },
        {"role": "user", "content": user_message},
    ]

    # Initial request
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process tool calls if any
    while response.choices[0].message.tool_calls:
        # Add assistant's response with tool calls
        messages.append(response.choices[0].message)

        # Execute each tool call
        for tool_call in response.choices[0].message.tool_calls:
            tool_response = process_openai_tool_call(tool_call)
            messages.append(tool_response)

        # Get next response
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

    return response.choices[0].message.content


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
        "Find information about Ilya Sutskever on Google Scholar, "
        "including his h-index and top cited papers."
    )
    print(response)
