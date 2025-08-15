"""
Main pipeline orchestrator for the Dev Blog Spelunker.

This module coordinates the entire content discovery, processing, and curation pipeline.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import asyncio
import logging
from pathlib import Path

from src.feeds.feed_manager import FeedManager
from src.content.article_processor import ArticleProcessor
from src.classification.copilot_classifier import CopilotClassifier
from src.ranking.article_ranker import ArticleRanker
from src.curation.list_generator import ListGenerator
from src.utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class SpelunkerPipeline:
    """Main pipeline for blog content processing and curation."""
    
    def __init__(self, config_path: str = "config"):
        self.config = ConfigManager(config_path)
        self.feed_manager = FeedManager(self.config)
        self.article_processor = ArticleProcessor(self.config)
        self.classifier = CopilotClassifier(self.config)
        self.ranker = ArticleRanker(self.config)
        self.list_generator = ListGenerator(self.config)
        
    async def run_daily_ingestion(self) -> Dict[str, Any]:
        """Run the daily feed ingestion pipeline."""
        logger.info("Starting daily ingestion pipeline")
        
        try:
            # 1. Fetch and parse RSS feeds
            raw_articles = await self.feed_manager.fetch_all_feeds()
            logger.info(f"Fetched {len(raw_articles)} articles from feeds")
            
            # 2. Process article content
            processed_articles = await self.article_processor.process_batch(raw_articles)
            logger.info(f"Processed {len(processed_articles)} articles")
            
            # 3. Classify articles using Copilot
            classified_articles = await self.classifier.classify_batch(processed_articles)
            logger.info(f"Classified {len(classified_articles)} articles")
            
            # 4. Save daily data
            today = datetime.now().strftime("%Y-%m-%d")
            await self._save_daily_data(today, classified_articles)
            
            return {
                "status": "success",
                "date": today,
                "articles_processed": len(classified_articles),
                "feeds_checked": len(self.feed_manager.active_feeds)
            }
            
        except Exception as e:
            logger.error(f"Daily ingestion failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "date": datetime.now().strftime("%Y-%m-%d")
            }
    
    async def run_weekly_curation(self, week_override: str = None) -> Dict[str, Any]:
        """Run the weekly curation pipeline."""
        week = week_override or datetime.now().strftime("%Y-W%U")
        logger.info(f"Starting weekly curation for {week}")
        
        try:
            # 1. Load week's classified articles
            weekly_articles = await self._load_weekly_articles(week)
            logger.info(f"Loaded {len(weekly_articles)} articles for {week}")
            
            # 2. Rank articles
            ranked_articles = await self.ranker.rank_articles(weekly_articles)
            logger.info(f"Ranked {len(ranked_articles)} articles")
            
            # 3. Generate reading lists
            reading_lists = await self.list_generator.generate_weekly_lists(ranked_articles)
            logger.info(f"Generated reading lists for {len(reading_lists)} categories")
            
            # 4. Save curated content
            await self._save_weekly_curation(week, reading_lists)
            
            return {
                "status": "success",
                "week": week,
                "articles_ranked": len(ranked_articles),
                "categories": list(reading_lists.keys())
            }
            
        except Exception as e:
            logger.error(f"Weekly curation failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "week": week
            }
    
    async def discover_new_feeds(self) -> Dict[str, Any]:
        """Discover new blog feeds to add to the registry."""
        logger.info("Starting feed discovery")
        
        try:
            new_feeds = await self.feed_manager.discover_feeds()
            validated_feeds = await self.feed_manager.validate_feeds(new_feeds)
            
            return {
                "status": "success",
                "discovered": len(new_feeds),
                "validated": len(validated_feeds),
                "new_feeds": validated_feeds
            }
            
        except Exception as e:
            logger.error(f"Feed discovery failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def _save_daily_data(self, date: str, articles: List[Dict[str, Any]]):
        """Save daily ingestion data."""
        data_dir = Path("data/classified")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Implementation would save to JSON files
        # This is a placeholder for the actual implementation
        pass
    
    async def _load_weekly_articles(self, week: str) -> List[Dict[str, Any]]:
        """Load a week's worth of classified articles."""
        # Implementation would load from daily JSON files
        # This is a placeholder for the actual implementation
        return []
    
    async def _save_weekly_curation(self, week: str, reading_lists: Dict[str, List[Dict[str, Any]]]):
        """Save weekly curation results."""
        data_dir = Path("data/curated/weekly")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Implementation would save reading lists
        # This is a placeholder for the actual implementation
        pass


async def main():
    """Main entry point for the pipeline."""
    pipeline = SpelunkerPipeline()
    
    # Run daily ingestion
    result = await pipeline.run_daily_ingestion()
    print(f"Daily ingestion result: {result}")
    
    # Run weekly curation (if it's Monday)
    if datetime.now().weekday() == 0:  # Monday
        curation_result = await pipeline.run_weekly_curation()
        print(f"Weekly curation result: {curation_result}")


if __name__ == "__main__":
    asyncio.run(main())