import time
import argparse
from loguru import logger

from curator_agent import curate_articles_with_llm


def print_cli_digest(articles):
    """logger.infos the curated articles to the console."""
    if not articles:
        logger.info("\nNo articles of interest found today by the LLM.")
        return

    logger.info("\n--- Your LLM-Curated Hacker News Digest ---")
    for i, article in enumerate(articles):
        title = article.get('title', 'No Title')
        url = article.get('url', '#')
        hn_score = article.get('score', 'N/A')
        llm_score = article.get('llm_relevance_score', 'N/A')
        llm_summary = article.get('llm_summary', 'No summary provided.')
        llm_reasoning = article.get(
            'llm_reasoning', 'No specific reasoning provided.')

        print(f"\n{i+1}. {title}")
        print(f"   URL: {url}")
        print(f"   Scores: HN={hn_score}, LLM={llm_score}/10")
        print(f"   Summary: {llm_summary}")
        print(f"   Reasoning: {llm_reasoning}")
        print("---")
    print("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LLM-Powered Hacker News Curator Agent.")
    parser.add_argument('--cli-digest', action='store_true',
                        help='Fetch and logger.info today\'s digest to the command line, then exit.')
    args = parser.parse_args()

    if args.cli_digest:
        # Run the curation once and logger.info to CLI, then exit
        logger.info(f"[{time.ctime()}] Fetching CLI digest...")
        articles = curate_articles_with_llm()
        print_cli_digest(articles)
        logger.success(f"[{time.ctime()}] CLI digest job finished.")
    else:
        logger.error("Invalid Argument")
