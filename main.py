import time
import argparse
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding

from curator_agent import curate_articles_with_llm

console = Console()


def print_cli_digest(articles):
    if not articles:
        console.print(
            "\n[bold yellow]No articles of interest found today by the LLM.[/bold yellow]\n")
        return

    console.print(
        Panel(
            "[bold green]--- Your LLM-Curated Hacker News Digest ---[/bold green]",
            expand=False,
            border_style="green",
            padding=(1, 2)
        ),
        justify="center"
    )

    for i, article in enumerate(articles):
        title = article.get('title', 'No Title')
        url = article.get('url', '#')
        hn_score = article.get('score', 'N/A')
        llm_score = article.get('llm_relevance_score', 'N/A')
        llm_summary = article.get('llm_summary', 'No summary provided.')
        llm_reasoning = article.get(
            'llm_reasoning', 'No specific reasoning provided.')

        article_title = Text(f"{i+1}. {title}", style="bold cyan")
        article_url = Text(f"URL: {url}", style="link blue", justify="left")

        summary_text = Text(f"Summary: {llm_summary}", style="italic")
        reasoning_text = Text(f"Reasoning: {llm_reasoning}", style="dim grey")
        scores_text = Text(f"Scores: HN=[bold]{
                           hn_score}[/bold], LLM=[bold]{llm_score}/10[/bold]", style="white")

        panel_content = Text()
        panel_content.append(article_title)
        panel_content.append("\n")
        panel_content.append(article_url)
        panel_content.append("\n")
        panel_content.append(scores_text)
        panel_content.append("\n\n")
        panel_content.append(summary_text)
        panel_content.append("\n\n")
        panel_content.append(reasoning_text)

        console.print(
            Padding(
                Panel(
                    panel_content,
                    title=f"[dim blue]Article {
                        i+1}[/dim blue]",  # Title for the panel
                    title_align="left",
                    border_style="dim blue",
                    padding=(1, 2)
                ),
                (0, 0, 1, 0)
            )
        )

    console.print(
        Panel(
            "[bold green]--- End of Digest ---[/bold green]",
            expand=False,
            border_style="green",
            padding=(1, 2)
        ),
        justify="center"
    )
    console.print("\n")


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
