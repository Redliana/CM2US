"""
Google Scholar MCP Server

Provides tools for searching academic papers, getting citations,
and retrieving author profiles from Google Scholar via SerpAPI.
"""

import json
import logging
import os
import re
import sys
from typing import Optional

from mcp.server.fastmcp import FastMCP
from serpapi import GoogleScholarSearch

# Configure logging to stderr (NEVER stdout - it corrupts JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("google-scholar-mcp")

# Initialize the MCP server with instructions
SERVER_INSTRUCTIONS = """
Google Scholar MCP Server - Academic Literature Search

IMPORTANT: Always search comprehensively across ALL publication types:
- Peer-reviewed journal articles
- Conference proceedings (NeurIPS, ICML, ACL, CVPR, etc.)
- Preprints (arXiv, bioRxiv, medRxiv, SSRN, etc.)
- Technical reports and working papers
- Theses and dissertations
- Books and book chapters

Search Tips for Comprehensive Results:
1. Use "source:arxiv" in query to specifically find arXiv preprints
2. Include conference names (e.g., "NeurIPS 2023") to find proceedings
3. Search without year filters first to get the broadest results
4. Recent preprints may have fewer citations but contain cutting-edge research
5. For emerging topics, prioritize recent preprints over older journal articles

When presenting results, always note the publication venue/source so users
can identify preprints vs peer-reviewed articles.
"""

mcp = FastMCP("google-scholar", instructions=SERVER_INSTRUCTIONS)

# Get API key from environment
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")


def get_api_key() -> str:
    """Get SerpAPI key, raising error if not set."""
    if not SERPAPI_KEY:
        raise ValueError(
            "SERPAPI_KEY environment variable not set. "
            "Get a free API key at https://serpapi.com"
        )
    return SERPAPI_KEY


@mcp.tool()
def search_scholar(
    query: str,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    num_results: int = 10,
) -> str:
    """
    Search Google Scholar for academic literature across ALL publication types.

    This searches comprehensively across:
    - Peer-reviewed journal articles
    - Conference proceedings (NeurIPS, ICML, ACL, CVPR, AAAI, etc.)
    - Preprints (arXiv, bioRxiv, medRxiv, SSRN, etc.)
    - Technical reports and working papers
    - Theses and dissertations
    - Books and book chapters

    Search Tips:
    - Add "arxiv" or "source:arxiv" to query to find arXiv preprints
    - Add conference names like "NeurIPS" or "ICML" to find proceedings
    - For cutting-edge research, check recent preprints (may have low citations)
    - The venue/source in results indicates publication type

    Args:
        query: Search query. Examples:
            - "retrieval augmented generation" (general search)
            - "transformer architecture arxiv" (preprints)
            - "deep learning NeurIPS 2023" (conference proceedings)
        year_from: Filter papers published from this year (inclusive)
        year_to: Filter papers published until this year (inclusive)
        num_results: Maximum number of results to return (1-20, default 10)

    Returns:
        JSON string with search results including titles, authors, venue/source, and citations
    """
    try:
        logger.info(f"Searching Google Scholar for: {query}")
        api_key = get_api_key()
        num_results = max(1, min(num_results, 20))

        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": api_key,
            "num": num_results,
        }

        if year_from:
            params["as_ylo"] = year_from
        if year_to:
            params["as_yhi"] = year_to

        search = GoogleScholarSearch(params)
        results = search.get_dict()

        if "error" in results:
            return json.dumps({"error": results["error"], "query": query}, indent=2)

        organic_results = results.get("organic_results", [])
        formatted_results = []

        for result in organic_results[:num_results]:
            pub_info = result.get("publication_info", {})
            summary = pub_info.get("summary", "")

            # Parse venue/source from the summary (format: "Authors - Venue, Year")
            venue = "Unknown"
            year = "Unknown"
            if summary:
                parts = summary.split(" - ")
                if len(parts) > 1:
                    venue_year = parts[-1]
                    # Extract year (last 4-digit number)
                    year_match = re.search(r'\b(19|20)\d{2}\b', venue_year)
                    if year_match:
                        year = year_match.group()
                    # Venue is everything before the year
                    venue = venue_year.rsplit(",", 1)[0].strip() if "," in venue_year else venue_year.strip()

            formatted_results.append({
                "title": result.get("title", "Unknown"),
                "authors": summary.split(" - ")[0] if " - " in summary else summary,
                "venue": venue,  # Shows arxiv, conference name, journal, etc.
                "year": year,
                "snippet": result.get("snippet", ""),
                "citations": result.get("inline_links", {}).get("cited_by", {}).get("total", 0),
                "url": result.get("link", ""),
                "pdf_url": result.get("resources", [{}])[0].get("link", "") if result.get("resources") else "",
            })

        logger.info(f"Found {len(formatted_results)} results for query: {query}")
        return json.dumps(
            {"query": query, "total_results": len(formatted_results), "results": formatted_results},
            indent=2,
        )

    except Exception as e:
        logger.error(f"Error searching Scholar: {str(e)}")
        return json.dumps({"error": str(e), "query": query}, indent=2)


@mcp.tool()
def get_paper_citations(
    citation_id: str,
    num_results: int = 10,
) -> str:
    """
    Get papers that cite a given paper using its citation ID.

    Args:
        citation_id: The citation ID from a previous search result (e.g., "1234567890")
        num_results: Maximum number of citing papers to return (1-20, default 10)

    Returns:
        JSON string with list of papers that cite the given paper
    """
    try:
        logger.info(f"Getting citations for ID: {citation_id}")
        api_key = get_api_key()
        num_results = max(1, min(num_results, 20))

        params = {
            "engine": "google_scholar",
            "cites": citation_id,
            "api_key": api_key,
            "num": num_results,
        }

        search = GoogleScholarSearch(params)
        results = search.get_dict()

        if "error" in results:
            return json.dumps({"error": results["error"], "citation_id": citation_id}, indent=2)

        organic_results = results.get("organic_results", [])
        formatted_results = []

        for result in organic_results[:num_results]:
            pub_info = result.get("publication_info", {})
            formatted_results.append({
                "title": result.get("title", "Unknown"),
                "authors": pub_info.get("summary", "Unknown"),
                "snippet": result.get("snippet", ""),
                "url": result.get("link", ""),
            })

        logger.info(f"Found {len(formatted_results)} citing papers")
        return json.dumps(
            {
                "citation_id": citation_id,
                "citing_papers_count": len(formatted_results),
                "citing_papers": formatted_results,
            },
            indent=2,
        )

    except Exception as e:
        logger.error(f"Error getting citations: {str(e)}")
        return json.dumps({"error": str(e), "citation_id": citation_id}, indent=2)


@mcp.tool()
def get_author_profile(author_id: str) -> str:
    """
    Get an author's profile from Google Scholar using their author ID.

    To find an author ID, search for papers by the author and look for
    author links in the results, or search Google Scholar directly.

    Args:
        author_id: Google Scholar author ID (e.g., "JicYPdAAAAAJ")

    Returns:
        JSON string with author profile including name, affiliation, citations, and publications
    """
    try:
        logger.info(f"Getting author profile for ID: {author_id}")
        api_key = get_api_key()

        params = {
            "engine": "google_scholar_author",
            "author_id": author_id,
            "api_key": api_key,
        }

        search = GoogleScholarSearch(params)
        results = search.get_dict()

        if "error" in results:
            return json.dumps({"error": results["error"], "author_id": author_id}, indent=2)

        author = results.get("author", {})
        cited_by = results.get("cited_by", {})
        articles = results.get("articles", [])

        formatted_articles = []
        for article in articles[:10]:
            formatted_articles.append({
                "title": article.get("title", "Unknown"),
                "year": article.get("year", "Unknown"),
                "citations": article.get("cited_by", {}).get("value", 0),
            })

        result = {
            "name": author.get("name", "Unknown"),
            "affiliation": author.get("affiliations", "Unknown"),
            "email_domain": author.get("email", "Unknown"),
            "interests": author.get("interests", []),
            "citations_all": cited_by.get("table", [{}])[0].get("citations", {}).get("all", 0) if cited_by.get("table") else 0,
            "h_index": cited_by.get("table", [{}])[0].get("h_index", {}).get("all", 0) if cited_by.get("table") else 0,
            "i10_index": cited_by.get("table", [{}])[0].get("i10_index", {}).get("all", 0) if cited_by.get("table") else 0,
            "publications": formatted_articles,
        }

        logger.info(f"Found author: {result['name']}")
        return json.dumps(result, indent=2)

    except Exception as e:
        logger.error(f"Error getting author profile: {str(e)}")
        return json.dumps({"error": str(e), "author_id": author_id}, indent=2)


@mcp.tool()
def search_author(
    author_name: str,
) -> str:
    """
    Search for an author on Google Scholar to find their author ID and basic info.

    Args:
        author_name: Name of the author to search for (e.g., "Geoffrey Hinton")

    Returns:
        JSON string with matching authors and their IDs
    """
    try:
        logger.info(f"Searching for author: {author_name}")
        api_key = get_api_key()

        params = {
            "engine": "google_scholar_profiles",
            "mauthors": author_name,
            "api_key": api_key,
        }

        search = GoogleScholarSearch(params)
        results = search.get_dict()

        if "error" in results:
            return json.dumps({"error": results["error"], "author_name": author_name}, indent=2)

        profiles = results.get("profiles", [])
        formatted_profiles = []

        for profile in profiles[:5]:
            formatted_profiles.append({
                "name": profile.get("name", "Unknown"),
                "author_id": profile.get("author_id", ""),
                "affiliation": profile.get("affiliations", "Unknown"),
                "email_domain": profile.get("email", ""),
                "citations": profile.get("cited_by", 0),
                "interests": [i.get("title", "") for i in profile.get("interests", [])],
            })

        logger.info(f"Found {len(formatted_profiles)} matching authors")
        return json.dumps(
            {"author_name": author_name, "matching_authors": formatted_profiles},
            indent=2,
        )

    except Exception as e:
        logger.error(f"Error searching for author: {str(e)}")
        return json.dumps({"error": str(e), "author_name": author_name}, indent=2)


def main():
    """Run the MCP server."""
    logger.info("Starting Google Scholar MCP Server (SerpAPI)")
    if not SERPAPI_KEY:
        logger.warning("SERPAPI_KEY not set - tools will fail until configured")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
