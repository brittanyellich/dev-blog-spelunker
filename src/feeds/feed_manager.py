"""
RSS feed management and ingestion.

This module handles discovery, validation, and processing of RSS feeds
from developer blogs.
"""

from typing import List, Dict, Any
import asyncio
import feedparser
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedManager:
    """Manages RSS feed discovery, validation, and ingestion."""
    
    def __init__(self, config):
        self.config = config
        self.active_feeds = config.get_active_feeds()
        
    async def fetch_all_feeds(self) -> List[Dict[str, Any]]:
        """
        Fetch articles from all active RSS feeds.
        
        Returns:
            List of raw article data from all feeds
        """
        all_articles = []
        
        tasks = [self.fetch_feed(feed) for feed in self.active_feeds]
        feed_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for feed, result in zip(self.active_feeds, feed_results):
            if isinstance(result, Exception):
                logger.error(f"Feed fetch failed for {feed.name}: {result}")
                continue
                
            articles = result
            logger.info(f"Fetched {len(articles)} articles from {feed.name}")
            all_articles.extend(articles)
        
        return all_articles
    
    async def fetch_feed(self, feed_config) -> List[Dict[str, Any]]:
        """
        Fetch articles from a single RSS feed.
        
        Args:
            feed_config: Feed configuration object
            
        Returns:
            List of article data from the feed
        """
        try:
            # Use asyncio to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, requests.get, feed_config.url)
            response.raise_for_status()
            
            # Parse RSS feed
            feed_data = feedparser.parse(response.content)
            
            articles = []
            for entry in feed_data.entries:
                article = {
                    'id': self._generate_article_id(entry),
                    'title': entry.get('title', 'Untitled'),
                    'url': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'author': entry.get('author', ''),
                    'published_date': self._parse_date(entry.get('published')),
                    'source_feed': feed_config.id,
                    'source_name': feed_config.name,
                    'tags': [tag.term for tag in entry.get('tags', [])],
                    'raw_entry': entry
                }
                articles.append(article)
            
            return articles
            
        except Exception as e:
            logger.error(f"Failed to fetch feed {feed_config.name}: {e}")
            raise
    
    async def discover_feeds(self) -> List[Dict[str, Any]]:
        """
        Discover new developer blog feeds.
        
        Returns:
            List of newly discovered feed candidates
        """
        # Placeholder implementation
        # Real implementation would crawl blog directories,
        # check GitHub topics, analyze social media, etc.
        
        discovered_feeds = [
            {
                'name': 'Example Tech Blog',
                'url': 'https://example-tech-blog.com/rss',
                'description': 'A great tech blog about software engineering',
                'estimated_authority': 75
            }
        ]
        
        return discovered_feeds
    
    async def validate_feeds(self, feed_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate discovered feeds for quality and relevance.
        
        Args:
            feed_candidates: List of potential feeds to validate
            
        Returns:
            List of validated feeds suitable for inclusion
        """
        validated_feeds = []
        
        for candidate in feed_candidates:
            try:
                # Test feed accessibility
                response = requests.get(candidate['url'], timeout=10)
                response.raise_for_status()
                
                # Parse and validate feed structure
                feed_data = feedparser.parse(response.content)
                
                if len(feed_data.entries) > 0:
                    # Basic quality checks passed
                    validated_feeds.append(candidate)
                    
            except Exception as e:
                logger.warning(f"Feed validation failed for {candidate['url']}: {e}")
        
        return validated_feeds
    
    def _generate_article_id(self, entry) -> str:
        """Generate a unique ID for an article."""
        # Use URL or GUID if available, otherwise create from title + date
        return entry.get('id', entry.get('link', f"{entry.get('title', '')}_{entry.get('published', '')}"))
    
    def _parse_date(self, date_string) -> datetime:
        """Parse date string from RSS entry."""
        if not date_string:
            return datetime.now()
        
        try:
            # feedparser usually provides parsed date
            return datetime.now()  # Placeholder
        except:
            return datetime.now()