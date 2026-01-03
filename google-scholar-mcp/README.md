# Google Scholar MCP Server

An MCP (Model Context Protocol) server that enables Claude Desktop to search Google Scholar for academic literature.

## Features

- **search_scholar** - Search papers by query, filter by year range
- **search_author** - Find authors by name
- **get_author_profile** - Get author details, h-index, publications
- **get_paper_citations** - Find papers citing a given work

Searches comprehensively across:
- Peer-reviewed journal articles
- Conference proceedings (NeurIPS, ICML, ACL, CVPR, etc.)
- Preprints (arXiv, bioRxiv, medRxiv, SSRN, etc.)
- Technical reports, theses, and books

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- [SerpAPI](https://serpapi.com) account (free tier: 100 searches/month)

## Installation

1. **Install dependencies:**
   ```bash
   cd google-scholar-mcp
   uv sync
   ```

2. **Get a SerpAPI key** at https://serpapi.com

3. **Configure Claude Desktop** - Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "google-scholar": {
         "command": "uv",
         "args": [
           "--directory",
           "/ABSOLUTE/PATH/TO/google-scholar-mcp",
           "run",
           "server.py"
         ],
         "env": {
           "SERPAPI_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

4. **Restart Claude Desktop** (Cmd+Q, then reopen)

## Usage Examples

Once configured, ask Claude Desktop:
- "Search Google Scholar for papers on retrieval augmented generation"
- "Find recent arXiv preprints on transformer architectures"
- "Get the author profile for Geoffrey Hinton"
- "Search for NeurIPS 2023 papers on large language models"

## License

MIT
