# Google Scholar API

A standalone Python library for searching Google Scholar, designed for easy integration with any LLM via their tool/function calling APIs.

## Features

- **search_scholar** - Search papers by query, filter by year
- **get_paper_citations** - Find papers citing a given work
- **Command-line interface** - Search directly from terminal

Built-in support for:
- **OpenAI** function calling (GPT-4, GPT-3.5)
- **Anthropic** tool use (Claude)
- **Ollama** local models (Phi-4, Llama, Mistral, etc.)
- **Generic** tool schemas (adaptable to any LLM)

Searches comprehensively across all publication types:
- Peer-reviewed journal articles
- Conference proceedings (NeurIPS, ICML, ACL, CVPR, etc.)
- Preprints (arXiv, bioRxiv, medRxiv, SSRN, etc.)
- Technical reports, theses, and books

## Installation

```bash
cd google-scholar-api
uv sync

# For OpenAI integration
uv sync --extra openai

# For Anthropic integration
uv sync --extra anthropic

# For Ollama integration (local models)
uv sync --extra ollama

# For all integrations
uv sync --extra all
```

## Prerequisites

Get a free SerpAPI key at https://serpapi.com (100 searches/month free)

## Quick Start

### Direct Usage (No LLM)

```python
from scholar import search_scholar, set_api_key

# Set your API key
set_api_key("your-serpapi-key")
# Or use environment variable: export SERPAPI_KEY=your-key

# Search for papers
results = search_scholar("retrieval augmented generation", year_from=2023)
for paper in results.papers:
    print(f"{paper.title} ({paper.year}) - {paper.citations} citations")
    print(f"  Venue: {paper.venue}")
    print(f"  URL: {paper.url}")
```

### OpenAI Integration

```python
from openai import OpenAI
from scholar import set_api_key, get_openai_tools, process_openai_tool_call

set_api_key("your-serpapi-key")
client = OpenAI()

# Get tools in OpenAI format
tools = get_openai_tools()

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "Find papers on RAG from 2024"}],
    tools=tools,
)

# Process tool calls
for tool_call in response.choices[0].message.tool_calls:
    result = process_openai_tool_call(tool_call)
    print(result)
```

### Anthropic Integration

```python
from anthropic import Anthropic
from scholar import set_api_key, get_anthropic_tools, process_anthropic_tool_use

set_api_key("your-serpapi-key")
client = Anthropic()

# Get tools in Anthropic format
tools = get_anthropic_tools()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=tools,
    messages=[{"role": "user", "content": "Find papers on RAG from 2024"}],
)

# Process tool use
for block in response.content:
    if block.type == "tool_use":
        result = process_anthropic_tool_use(block)
        print(result)
```

### Ollama Integration (Local Models)

Works with Phi-4, Llama, Mistral, Qwen, and any other Ollama model.

```python
from examples.ollama_example import chat_with_scholar

# Search with Phi-4 (default)
response = chat_with_scholar("Find recent papers on retrieval augmented generation")
print(response)

# Use a different model
response = chat_with_scholar("Find papers on transformers", model="llama3")
```

Or run the example directly:
```bash
export SERPAPI_KEY="your-serpapi-key"
uv run python examples/ollama_example.py
```

**How it works:**
1. The model receives a system prompt explaining how to request searches
2. When it needs papers, it outputs JSON: `{"action": "search", "query": "..."}`
3. We execute the search and return results
4. The model summarizes the findings

This prompt-based approach works with **any Ollama model** - no native tool calling required.

### Generic LLM Integration

```python
from scholar import get_tool_schemas, execute_tool

# Get tool schemas (adapt to your LLM's format)
schemas = get_tool_schemas()

# Execute a tool by name
result = execute_tool("search_scholar", {
    "query": "machine learning",
    "year_from": 2023,
    "num_results": 5,
})
print(result)
```

## Command-Line Interface

Search Google Scholar directly from the terminal without writing any code.

### Setup

Set your API key (once per terminal session):
```bash
export SERPAPI_KEY="your-serpapi-key"
```

### Usage

```bash
cd google-scholar-api

# Basic search
uv run python cli.py search "machine learning"

# Search with options
uv run python cli.py search "retrieval augmented generation" --num 5 --year-from 2023

# Search for arXiv preprints
uv run python cli.py search "transformers arxiv" --num 10

# Output as JSON (for scripting)
uv run python cli.py search "neural networks" --json

# Show help
uv run python cli.py --help
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `search <query>` | Search for papers |
| `--num, -n` | Number of results (default: 10) |
| `--year-from` | Filter papers from this year |
| `--year-to` | Filter papers until this year |
| `--json` | Output results as JSON |

### Example Output

```
Found 3 papers for: retrieval augmented generation

1. Retrieval-augmented generation for knowledge-intensive nlp tasks
   Authors: P Lewis, E Perez, A Piktus, F Petroni…
   Venue: proceedings.neurips.cc
   Citations: 14596
   URL: https://proceedings.neurips.cc/paper/...
   PDF: https://proceedings.neurips.cc/paper/.../Paper.pdf
```

## API Reference

### Search Functions

#### `search_scholar(query, year_from=None, year_to=None, num_results=10)`
Search for papers. Returns `ScholarResult` with list of `Paper` objects.

#### `get_paper_citations(citation_id, num_results=10)`
Get papers citing a given paper. Returns `CitationResult`.

### Tool Helpers

#### `get_openai_tools()`
Returns tool definitions in OpenAI function calling format.

#### `get_anthropic_tools()`
Returns tool definitions in Anthropic Claude format.

#### `get_tool_schemas()`
Returns generic tool schemas (adapt to any LLM).

#### `execute_tool(tool_name, arguments)`
Execute a tool by name with given arguments.

#### `process_openai_tool_call(tool_call)`
Process an OpenAI tool call and return formatted result.

#### `process_anthropic_tool_use(tool_use_block)`
Process an Anthropic tool use block and return formatted result.

## Examples

See the `examples/` directory:
- `basic_usage.py` - Direct function calls
- `openai_example.py` - GPT-4 integration
- `anthropic_example.py` - Claude API integration
- `ollama_example.py` - Phi-4, Llama, and other local models

## License

MIT
