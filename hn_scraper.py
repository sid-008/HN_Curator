import requests

HN_API_BASE = "https://hacker-news.firebaseio.com/v0/"


def get_top_story_ids(limit=50):
    """Fetch IDs of the top stories."""
    try:
        response = requests.get(f"{HN_API_BASE}topstories.json")
        response.raise_for_status()  # Raise HTTP error either (4xx or 5xx)
        return response.json()[:limit]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top story IDs: {e}")
        return []


def get_item_details(item_id):
    """Fetches details for a given story ID."""
    try:
        response = requests.get(f"{HN_API_BASE}item/{item_id}.json")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # TODO: use Loguru here instead
        print(f"Error fetching item details for ID {item_id}: {e}")
        return None


def fetch_hn_articles(num_articles=30):
    """Fetches a specified number of top Hacker News articles."""
    story_ids = get_top_story_ids(num_articles)
    articles = []
    print(f"Fetching details for {len(story_ids)} articles...")
    for i, item_id in enumerate(story_ids):
        details = get_item_details(item_id)
        # Validate that it is a story
        if details and details.get('type') == 'story':
            articles.append({
                'id': details.get('id'),
                'title': details.get('title'),
                # Use HN link if no external URL
                'url': details.get('url', f"https://news.ycombinator.com/item?id={details.get('id')}"),
                'score': details.get('score'),
                'time': details.get('time')
            })
        print(f"  Fetched {i+1}/{len(story_ids)}...", end='\r')
    print("\nDone fetching articles.")
    return articles


if __name__ == "__main__":
    articles = fetch_hn_articles(num_articles=5)
    for article in articles[:5]:
        print(f"Title: {article['title']}\nURL: {
              article['url']}\nScore: {article['score']}\n---")
