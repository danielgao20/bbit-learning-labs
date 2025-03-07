"""Module for retrieving newsfeed information."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from app.utils.redis import REDIS_CLIENT


@dataclass
class Article:
    """Dataclass for an article."""

    author: str
    title: str
    body: str
    publish_date: datetime
    image_url: str
    url: str


def _format_article(raw_article: dict) -> Article:
    """Format raw article data into an Article object."""
    return Article(
        author=raw_article.get("author", "Unknown"),
        title=raw_article["title"],
        body=raw_article.get("body", raw_article.get("text", "No content available")),
        publish_date=datetime.strptime(raw_article.get("publish_date", "2000-01-01"), "%Y-%m-%d"),
        image_url=raw_article.get("image_url", raw_article.get("main_image", "/fallback-image.jpeg")),  # Fix here
        url=raw_article["url"],
    )


def get_all_news() -> List[Article]:
    """Get all news articles from Redis datastore."""
    raw_articles = REDIS_CLIENT.get_entry("all_articles")
    if not raw_articles:
        return []

    articles = [_format_article(article) for article in raw_articles]
    return articles


def get_featured_news() -> Optional[Article]:
    """Get the most recent featured news article."""
    articles = get_all_news()
    if not articles:
        return None

    sorted_articles = sorted(articles, key=lambda x: x.publish_date, reverse=True)
    return sorted_articles[0]  # Return the most recent article
