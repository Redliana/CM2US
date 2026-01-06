# Google Scholar + Phi-4 Cheat Sheet

## Quick Start

```bash
cd /Users/wash198/Library/CloudStorage/OneDrive-PNNL/Documents/Projects/Science_Projects/MPII_CMM/RAG/google-scholar-api
```

## Interactive Chat (Recommended)

```bash
uv run python chat.py
```
- Phi-4 asks what you want to search
- Type your query, get results, ask follow-ups
- Type `quit` to exit

## Command Line Search

```bash
uv run python cli.py search "your query"
```

### Options
```bash
uv run python cli.py search "machine learning" --num 5
uv run python cli.py search "RAG" --year-from 2023
uv run python cli.py search "transformers" --year-from 2023 --year-to 2024
uv run python cli.py search "neural networks" --json
```

## Search Tips

| Want | Search |
|------|--------|
| Preprints | `"transformers arxiv"` |
| Conference papers | `"attention NeurIPS"` or `"BERT ICML"` |
| Recent papers | Use `--year-from 2023` |
| Specific journal | `"cancer Nature"` |
| Multiple terms | `"retrieval augmented generation LLM"` |

## Example Searches

```bash
# Recent RAG papers
uv run python cli.py search "retrieval augmented generation" --year-from 2023 --num 5

# arXiv preprints on LLMs
uv run python cli.py search "large language models arxiv" --num 10

# NeurIPS papers on transformers
uv run python cli.py search "transformer architecture NeurIPS" --num 5

# Climate change ML papers
uv run python cli.py search "climate change machine learning" --year-from 2020
```

## Python Usage

```python
from scholar import search_scholar

results = search_scholar("machine learning", year_from=2023, num_results=5)
for p in results.papers:
    print(f"{p.title} - {p.citations} citations")
```

## Files

| File | Purpose |
|------|---------|
| `chat.py` | Interactive Phi-4 chat |
| `cli.py` | Command line searches |
| `.env` | Your API key (don't share!) |

## Troubleshooting

**"SerpAPI key not set"**
- Check `.env` file exists with `SERPAPI_KEY=your-key`

**Ollama errors**
- Make sure Ollama is running: `ollama serve`
- Check Phi-4 is installed: `ollama list`

**No results**
- Try broader search terms
- Remove year filters
- Check spelling
