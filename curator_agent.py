import google.generativeai as genai
import json
import time
import re
from loguru import logger
from hn_scraper import fetch_hn_articles
from config import GOOGLE_API_KEY, USER_INTEREST_PROFILE, MIN_HN_SCORE, MIN_LLM_RELEVANCE_SCORE

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemma-3-4b-it')


def get_llm_evaluation(article_title, article_url):
    """
    Sends an article's title to the LLM for relevance evaluation and summary.
    """
    prompt = f"""
    Based on the following user interest profile, evaluate the relevance of
    the provided Hacker News article.

    User Interest Profile:
    {USER_INTEREST_PROFILE}

    Hacker News Article:
    Title: "{article_title}"
    URL: "{article_url}"

    Please provide your evaluation in a JSON format.
    The JSON should contain:
    1.  `relevance_score`: An integer from 1 (not relevant) to 10 (highly relevant).
    2.  `summary`: A concise one-sentence summary of what the article is about, focusing on its relevance to the user's interests.
    3.  `reasoning`: A very brief explanation for the score.

    Example output format:
    {{
        "relevance_score": 8,
        "summary": "This article discusses new advancements in LLM fine-tuning techniques relevant to AI engineers.",
        "reasoning": "Directly relates to LLMs and practical AI applications."
    }}
    """

    try:
        response = model.generate_content(prompt)

        # Extract text from the response
        response_text = response.text

        # Try to parse the JSON string
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        else:
            logger.warning(f"Could not find JSON in LLM response for '{
                article_title}': {response_text}")
            return None

    except Exception as e:
        logger.error(f"Error calling LLM for '{article_title}': {e}")
        # TODO: Add retry logic or backoff if needed
        time.sleep(1)  # Small delay to avoid hitting rate limits
        return None


def curate_articles_with_llm():
    """Fetches articles, then uses LLM to filter and provide summaries."""
    all_articles = fetch_hn_articles(
        num_articles=5)  # Fetch top N HN articles
    curated_articles = []

    logger.debug(f"Evaluating {len(all_articles)} articles with LLM...")
    for i, article in enumerate(all_articles):
        # Initial filter by HN score to reduce LLM calls
        if article.get('score', 0) < MIN_HN_SCORE:
            logger.debug(f"  Skipping '{article.get(
                'title')}' due to low HN score ({article.get('score')}).")
            continue

        llm_eval = get_llm_evaluation(article.get(
            'title', ''), article.get('url', ''))

        if llm_eval:
            try:
                relevance_score = llm_eval.get('relevance_score')
                summary = llm_eval.get('summary')

                if relevance_score and relevance_score >= MIN_LLM_RELEVANCE_SCORE:
                    article['llm_relevance_score'] = relevance_score
                    article['llm_summary'] = summary
                    article['llm_reasoning'] = llm_eval.get(
                        'reasoning', 'No specific reasoning provided.')
                    curated_articles.append(article)
                    logger.debug(f"  ✅ Relevant: '{
                        article['title']}' (LLM Score: {relevance_score})")
                else:
                    logger.debug(f"  ❌ Not Relevant: '{
                        article['title']}' (LLM Score: {relevance_score})")
            except Exception as e:
                logger.error(f"Error processing LLM evaluation for '{
                    article.get('title')}': {e}")
                logger.error(f"LLM Response: {llm_eval}")
        else:
            logger.info(f"  Skipping '{article.get('title')
                                       }' due to LLM evaluation error.")

    return sorted(curated_articles,
                  key=lambda x: (x.get('llm_relevance_score', 0),
                                 x.get('score', 0)),
                  reverse=True)
