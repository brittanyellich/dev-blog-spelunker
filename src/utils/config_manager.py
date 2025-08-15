"""Configuration manager for the Dev Blog Spelunker."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CategoryConfig:
    """Configuration for a content category."""
    name: str
    description: str
    weight: float
    keywords: List[str]
    examples: List[str]
    classification_prompts: List[str]


@dataclass
class FeedConfig:
    """Configuration for an RSS feed."""
    id: str
    name: str
    url: str
    description: str
    authority_score: float
    category_hints: List[str]
    tags: List[str]
    last_checked: datetime = None
    status: str = "active"


class ConfigManager:
    """Manages configuration for the entire application."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._categories = None
        self._feeds = None
        self._app_config = None
    
    @property
    def categories(self) -> Dict[str, CategoryConfig]:
        """Get category configurations."""
        if self._categories is None:
            self._load_categories()
        return self._categories
    
    @property
    def feeds(self) -> List[FeedConfig]:
        """Get feed configurations."""
        if self._feeds is None:
            self._load_feeds()
        return self._feeds
    
    @property
    def app_config(self) -> Dict[str, Any]:
        """Get application configuration."""
        if self._app_config is None:
            self._load_app_config()
        return self._app_config
    
    def _load_categories(self):
        """Load category configurations from YAML."""
        categories_file = self.config_dir / "categories.yaml"
        with open(categories_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        self._categories = {}
        for category_id, config in data['categories'].items():
            self._categories[category_id] = CategoryConfig(
                name=config['name'],
                description=config['description'],
                weight=config['weight'],
                keywords=config['keywords'],
                examples=config['examples'],
                classification_prompts=config['classification_prompts']
            )
    
    def _load_feeds(self):
        """Load feed configurations from YAML."""
        feeds_file = self.config_dir / "feeds.yaml"
        with open(feeds_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        self._feeds = []
        for feed_config in data['feeds']:
            self._feeds.append(FeedConfig(
                id=feed_config['id'],
                name=feed_config['name'],
                url=feed_config['url'],
                description=feed_config['description'],
                authority_score=feed_config['authority_score'],
                category_hints=feed_config['category_hints'],
                tags=feed_config['tags'],
                status=feed_config.get('status', 'active')
            ))
    
    def _load_app_config(self):
        """Load application configuration."""
        self._app_config = {
            'github': {
                'token': os.getenv('GITHUB_TOKEN'),
                'repository': 'brittanyellich/dev-blog-spelunker'
            },
            'copilot': {
                'api_key': os.getenv('COPILOT_API_KEY'),
                'model': os.getenv('COPILOT_MODEL', 'gpt-4'),
                'timeout': int(os.getenv('COPILOT_TIMEOUT', '30')),
                'rate_limit': int(os.getenv('COPILOT_RATE_LIMIT', '50'))
            },
            'processing': {
                'batch_size': 10,
                'max_retries': 3,
                'timeout': 30
            }
        }
    
    def get_category_by_id(self, category_id: str) -> CategoryConfig:
        """Get a specific category configuration."""
        return self.categories.get(category_id)
    
    def get_feed_by_id(self, feed_id: str) -> FeedConfig:
        """Get a specific feed configuration."""
        return next((f for f in self.feeds if f.id == feed_id), None)
    
    def get_active_feeds(self) -> List[FeedConfig]:
        """Get all active feeds."""
        return [f for f in self.feeds if f.status == 'active']