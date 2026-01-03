"""
Google Scholar API - A standalone library for searching Google Scholar.

Works with any LLM via their tool/function calling APIs.
"""

from .search import (
    search_scholar,
    search_author,
    get_author_profile,
    get_paper_citations,
    set_api_key,
    ScholarResult,
    AuthorResult,
    CitationResult,
)
from .tools import (
    get_openai_tools,
    get_anthropic_tools,
    get_tool_schemas,
    execute_tool,
    process_openai_tool_call,
    process_anthropic_tool_use,
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
