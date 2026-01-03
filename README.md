# CM2US

Research tools and utilities for the CMM project.

## Modules

### google-scholar-api

A standalone Python library for searching Google Scholar, designed for integration with **any LLM** via their tool/function calling APIs.

**Features:**
- Search academic papers across all publication types (journals, conferences, preprints)
- Find author profiles and publications
- Get citation information
- Built-in support for OpenAI, Anthropic, and generic LLM integrations

**Setup:** See [google-scholar-api/README.md](google-scholar-api/README.md)

### google-scholar-mcp

An MCP (Model Context Protocol) server for searching Google Scholar from **Claude Desktop** specifically.

**Features:**
- Same search capabilities as google-scholar-api
- Configured specifically for Claude Desktop's MCP protocol

**Setup:** See [google-scholar-mcp/README.md](google-scholar-mcp/README.md)

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- [SerpAPI](https://serpapi.com) account (free tier: 100 searches/month)
- [Claude Desktop](https://claude.ai/download) (only for MCP server)
