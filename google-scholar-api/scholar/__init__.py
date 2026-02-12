"""
Google Scholar API - A standalone library for searching Google Scholar.

Works with any LLM via their tool/function calling APIs.
"""

from __future__ import annotations

from .search import (
    AuthorResult,
    CitationResult,
    ScholarResult,
    get_author_profile,
    get_paper_citations,
    search_author,
    search_scholar,
    set_api_key,
)
from .tools import (
    execute_tool,
    get_anthropic_tools,
    get_openai_tools,
    get_tool_schemas,
    process_anthropic_tool_use,
    process_openai_tool_call,
)

__version__ = "1.0.0"
__all__ = [
    # Search functions
    "search_scholar",
    "search_author",
    "get_author_profile",
    "get_paper_citations",
    "set_api_key",
    # Result types
    "ScholarResult",
    "AuthorResult",
    "CitationResult",
    # Tool helpers
    "get_openai_tools",
    "get_anthropic_tools",
    "get_tool_schemas",
    "execute_tool",
    "process_openai_tool_call",
    "process_anthropic_tool_use",
]
