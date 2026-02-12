#!/usr/bin/env python3
"""
Google Scholar CLI - Search academic papers from the command line.

Usage:
    uv run python cli.py search "machine learning" --num 5
    uv run python cli.py search "RAG arxiv" --year-from 2023
    uv run python cli.py author "Geoffrey Hinton"
    uv run python cli.py profile JicYPdAAAAAJ
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from scholar import (
    get_author_profile,
    get_paper_citations,
    search_author,
    search_scholar,
    set_api_key,
)


def setup_api_key():
    """Set up API key from environment or prompt user."""
    key = os.environ.get("SERPAPI_KEY", "")
    if not key:
        print("Error: SERPAPI_KEY environment variable not set.")
        print("Set it with: export SERPAPI_KEY='your-key-here'")
        print("Get a free key at: https://serpapi.com")
        sys.exit(1)
    set_api_key(key)


def cmd_search(args):
    """Search for papers."""
    results = search_scholar(
        query=args.query,
        year_from=args.year_from,
        year_to=args.year_to,
        num_results=args.num,
    )

    if results.error:
        print(f"Error: {results.error}")
        return

    if args.json:
        print(json.dumps(results.to_dict(), indent=2))
        return

    print(f"\nFound {results.total_results} papers for: {results.query}\n")
    print("=" * 70)

    for i, paper in enumerate(results.papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {paper.authors}")
        print(f"   Venue: {paper.venue} ({paper.year})")
        print(f"   Citations: {paper.citations}")
        if paper.url:
            print(f"   URL: {paper.url}")
        if paper.pdf_url:
            print(f"   PDF: {paper.pdf_url}")


def cmd_author(args):
    """Search for an author."""
    results = search_author(args.name)

    if results.error:
        print(f"Error: {results.error}")
        return

    if args.json:
        print(json.dumps(results.to_dict(), indent=2))
        return

    print(f"\nAuthors matching: {args.name}\n")
    print("=" * 70)

    for author in results.authors:
        print(f"\nName: {author.name}")
        print(f"  ID: {author.author_id}")
        print(f"  Affiliation: {author.affiliation}")
        print(f"  Citations: {author.citations}")
        if author.interests:
            print(f"  Interests: {', '.join(author.interests[:5])}")


def cmd_profile(args):
    """Get author profile by ID."""
    results = get_author_profile(args.author_id)

    if results.error:
        print(f"Error: {results.error}")
        return

    if args.json:
        print(json.dumps(results.to_dict(), indent=2))
        return

    if not results.authors:
        print("Author not found.")
        return

    author = results.authors[0]
    print(f"\n{author.name}")
    print("=" * 70)
    print(f"Affiliation: {author.affiliation}")
    print(f"Total Citations: {author.citations}")
    print(f"h-index: {results.h_index}")
    print(f"i10-index: {results.i10_index}")

    if author.interests:
        print(f"Interests: {', '.join(author.interests[:5])}")

    if results.publications:
        print(f"\nTop Publications:")
        for pub in results.publications[:5]:
            print(f"  - {pub['title']} ({pub['year']}) - {pub['citations']} citations")


def cmd_citations(args):
    """Get papers citing a given paper."""
    results = get_paper_citations(args.citation_id, num_results=args.num)

    if results.error:
        print(f"Error: {results.error}")
        return

    if args.json:
        print(json.dumps(results.to_dict(), indent=2))
        return

    print(f"\nPapers citing: {args.citation_id}\n")
    print("=" * 70)

    for i, paper in enumerate(results.citing_papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {paper.authors}")
        print(f"   Venue: {paper.venue} ({paper.year})")


def main():
    parser = argparse.ArgumentParser(
        description="Search Google Scholar from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search "machine learning"
  %(prog)s search "RAG arxiv" --num 5 --year-from 2023
  %(prog)s author "Geoffrey Hinton"
  %(prog)s profile JicYPdAAAAAJ
  %(prog)s search "transformers" --json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for papers")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--num", "-n", type=int, default=10, help="Number of results (default: 10)"
    )
    search_parser.add_argument("--year-from", type=int, help="Filter from year")
    search_parser.add_argument("--year-to", type=int, help="Filter to year")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")
    search_parser.set_defaults(func=cmd_search)

    # Author search command
    author_parser = subparsers.add_parser("author", help="Search for an author")
    author_parser.add_argument("name", help="Author name")
    author_parser.add_argument("--json", action="store_true", help="Output as JSON")
    author_parser.set_defaults(func=cmd_author)

    # Profile command
    profile_parser = subparsers.add_parser("profile", help="Get author profile by ID")
    profile_parser.add_argument("author_id", help="Google Scholar author ID")
    profile_parser.add_argument("--json", action="store_true", help="Output as JSON")
    profile_parser.set_defaults(func=cmd_profile)

    # Citations command
    citations_parser = subparsers.add_parser("citations", help="Get citing papers")
    citations_parser.add_argument("citation_id", help="Citation ID from search results")
    citations_parser.add_argument("--num", "-n", type=int, default=10, help="Number of results")
    citations_parser.add_argument("--json", action="store_true", help="Output as JSON")
    citations_parser.set_defaults(func=cmd_citations)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    setup_api_key()
    args.func(args)


if __name__ == "__main__":
    main()
