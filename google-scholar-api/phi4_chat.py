#!/usr/bin/env python3
"""
Simple Phi-4 Chat - No Google Scholar, just direct conversation.

Usage:
    uv run python phi4_chat.py
"""

from __future__ import annotations

from ollama import chat


def main():
    print("=" * 50)
    print("  Phi-4 Chat")
    print("  type 'quit' to exit")
    print("=" * 50)
    print()

    messages = []

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "bye", "q"):
            print("\nGoodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        print("\nPhi-4: ", end="", flush=True)
        response = chat(model="phi4", messages=messages)
        assistant_message = response.message.content
        print(assistant_message)
        print()

        messages.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    main()
