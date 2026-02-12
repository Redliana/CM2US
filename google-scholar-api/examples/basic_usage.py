"""
Basic usage example - Direct function calls without LLM integration.
"""

import os

from scholar import get_author_profile, search_author, search_scholar, set_api_key

# Set your SerpAPI key (or use SERPAPI_KEY environment variable)
set_api_key(os.environ.get("SERPAPI_KEY", "your-api-key-here"))

# Example 1: Search for papers
print("=== Searching for papers on RAG ===")
results = search_scholar(
    query="retrieval augmented generation",
    year_from=2023,
    num_results=5,
)

if results.error:
    print(f"Error: {results.error}")
else:
    for paper in results.papers:
        print(f"\nTitle: {paper.title}")
        print(f"Authors: {paper.authors}")
        print(f"Venue: {paper.venue} ({paper.year})")
        print(f"Citations: {paper.citations}")
        print(f"URL: {paper.url}")

# Example 2: Search for arXiv preprints
print("\n\n=== Searching for arXiv preprints ===")
results = search_scholar(
    query="large language models arxiv",
    year_from=2024,
    num_results=3,
)

for paper in results.papers:
    print(f"\n{paper.title}")
    print(f"  {paper.venue} | {paper.citations} citations")

# Example 3: Find an author
print("\n\n=== Finding author ===")
author_results = search_author("Geoffrey Hinton")

for author in author_results.authors:
    print(f"\nName: {author.name}")
    print(f"ID: {author.author_id}")
    print(f"Affiliation: {author.affiliation}")
    print(f"Citations: {author.citations}")
    print(f"Interests: {', '.join(author.interests)}")

# Example 4: Get author profile with h-index
if author_results.authors:
    author_id = author_results.authors[0].author_id
    print(f"\n\n=== Getting profile for {author_id} ===")
    profile = get_author_profile(author_id)

    if profile.authors:
        author = profile.authors[0]
        print(f"Name: {author.name}")
        print(f"H-index: {profile.h_index}")
        print(f"i10-index: {profile.i10_index}")
        print(f"Total citations: {author.citations}")
        print("\nTop publications:")
        for pub in profile.publications[:5]:
            print(f"  - {pub['title']} ({pub['year']}) - {pub['citations']} citations")
