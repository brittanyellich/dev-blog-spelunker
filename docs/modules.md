# Core Modules Architecture

## Module Overview

The Dev Blog Spelunker is designed with a modular architecture for maintainability, testability, and extensibility.

## Core Modules

### 1. Feed Management (`src/feeds/`)

#### `feed_registry.py`
- Manages the registry of RSS feeds
- Validates feed URLs and health
- Discovers new feeds through various methods

#### `feed_parser.py`
- Parses RSS/Atom feeds
- Extracts article metadata
- Handles different feed formats and encodings

#### `feed_discoverer.py`
- Automatically discovers new developer blogs
- Crawls blog directories and recommendation lists
- Uses AI to evaluate blog relevance

### 2. Content Processing (`src/content/`)

#### `article_extractor.py`
- Extracts full article content from URLs
- Handles various content management systems
- Cleans and normalizes text content

#### `content_cleaner.py`
- Removes ads, navigation, and boilerplate
- Normalizes text formatting
- Extracts structured data

#### `duplicate_detector.py`
- Identifies duplicate or near-duplicate articles
- Handles cross-posting and syndication
- Maintains article uniqueness

### 3. Classification Engine (`src/classification/`)

#### `copilot_classifier.py`
- Integrates with GitHub Copilot for content analysis
- Generates category relevance scores
- Handles AI model interactions

#### `category_manager.py`
- Manages the 8 category definitions
- Provides category-specific classification logic
- Maintains category taxonomy

#### `relevance_scorer.py`
- Calculates relevance percentages
- Combines multiple scoring signals
- Normalizes scores across categories

### 4. Ranking System (`src/ranking/`)

#### `article_ranker.py`
- Implements multi-factor ranking algorithm
- Combines relevance, recency, authority, and engagement
- Provides configurable scoring weights

#### `authority_calculator.py`
- Calculates blog and author authority scores
- Tracks historical performance
- Integrates external authority signals

#### `engagement_tracker.py`
- Tracks social media engagement
- Monitors backlinks and citations
- Calculates engagement scores

### 5. Curation Engine (`src/curation/`)

#### `list_generator.py`
- Generates weekly reading lists
- Applies diversity and balance algorithms
- Creates category-specific and cross-category lists

#### `export_manager.py`
- Exports reading lists in multiple formats
- Generates RSS feeds for subscribers
- Creates API endpoints

#### `quality_filter.py`
- Applies quality filters to articles
- Removes low-quality or spam content
- Maintains content standards

### 6. Utilities (`src/utils/`)

#### `config_manager.py`
- Manages application configuration
- Handles environment variables
- Provides configuration validation

#### `logging_setup.py`
- Configures logging for all modules
- Provides structured logging
- Handles log rotation and archival

#### `github_client.py`
- GitHub API client for data storage
- Manages repository operations
- Handles authentication and rate limiting

## Module Dependencies

```
┌─────────────────────┐
│   GitHub Actions   │
│    (Orchestrator)   │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  Main Pipeline      │
│  (src/pipeline.py)  │
└─────────┬───────────┘
          │
          ├─── Feed Management
          ├─── Content Processing  
          ├─── Classification Engine
          ├─── Ranking System
          ├─── Curation Engine
          └─── Utilities
```

## Configuration System

### Category Configuration (`config/categories.yaml`)
```yaml
categories:
  technical_excellence:
    name: "🔧 Technical Excellence"
    description: "Building skills that last beyond any framework"
    keywords: ["architecture", "performance", "code quality", "engineering"]
    weight: 1.0
    examples:
      - "Engineering blogs (Shopify, Stripe, Netflix tech blogs)"
      - "Architecture decision records and case studies"
      
  communication_collaboration:
    name: "💬 Communication & Collaboration" 
    description: "Because the best code means nothing if you can't work with humans"
    keywords: ["leadership", "team dynamics", "feedback", "collaboration"]
    weight: 1.0
    examples:
      - "Management and leadership blogs"
      - "Team dynamics research"
```

### Feed Configuration (`config/feeds.yaml`)
```yaml
feeds:
  - name: "Netflix Tech Blog"
    url: "https://netflixtechblog.com/feed"
    category_hints: ["technical_excellence", "process_culture"]
    authority_score: 95
    last_checked: "2024-01-01T00:00:00Z"
    status: "active"
    
  - name: "Shopify Engineering"
    url: "https://shopify.engineering/blog.rss"
    category_hints: ["technical_excellence", "career_growth"]
    authority_score: 90
    last_checked: "2024-01-01T00:00:00Z"
    status: "active"
```

## Data Models

### Article Model
```python
@dataclass
class Article:
    id: str
    title: str
    url: str
    content: str
    summary: str
    author: str
    published_date: datetime
    source_feed: str
    category_scores: Dict[str, float]  # Category -> relevance score
    final_score: float
    tags: List[str]
    metadata: Dict[str, Any]
```

### Feed Model
```python
@dataclass
class Feed:
    id: str
    name: str
    url: str
    description: str
    authority_score: float
    category_hints: List[str]
    last_checked: datetime
    status: FeedStatus
    error_count: int
    articles_count: int
```

## Error Handling & Monitoring

### Error Handling Strategy
- Graceful degradation for feed failures
- Retry logic with exponential backoff
- Comprehensive error logging
- Health monitoring for all components

### Monitoring & Alerting
- Feed health monitoring
- Classification accuracy tracking
- Performance metrics collection
- GitHub Actions workflow monitoring

## Testing Strategy

### Unit Tests
- Individual module testing
- Mock external dependencies
- Test classification accuracy
- Validate data transformations

### Integration Tests  
- End-to-end pipeline testing
- Feed parsing validation
- GitHub Actions workflow testing
- Output format validation

### Performance Tests
- Large dataset processing
- Memory usage optimization
- API rate limit handling
- Concurrent processing validation