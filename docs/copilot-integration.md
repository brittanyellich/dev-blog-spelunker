# GitHub Copilot Integration

## Overview

The Dev Blog Spelunker leverages GitHub Copilot's AI capabilities for intelligent content analysis, classification, and curation. This document outlines the integration points and usage patterns.

## Integration Points

### 1. Content Classification

GitHub Copilot analyzes article content to determine relevance to each of the 8 categories:

```python
# Example Copilot classification prompt
classification_prompt = f"""
Analyze this developer blog article and score its relevance to each category (0-100%):

Article Title: {article.title}
Article Content: {article.content[:2000]}...

Categories:
1. 🔧 Technical Excellence - Engineering practices, architecture, code quality
2. 💬 Communication & Collaboration - Leadership, teamwork, soft skills  
3. 🚀 Career & Growth - Career advice, skill development, industry trends
4. 🧠 Mental Models & Problem Solving - Thinking frameworks, debugging
5. ⚖️ Work-Life Integration - Productivity, health, learning strategies
6. 🌱 Leadership & Mentoring - Technical leadership, mentorship
7. 🔄 Process & Culture - Team processes, code review, agile practices
8. 🎯 Impact & Purpose - Product thinking, business context, ethics

Provide scores as JSON: {{"technical_excellence": 85, "career_growth": 20, ...}}
Only include categories with scores > 10%.
"""
```

### 2. Quality Assessment

Copilot evaluates article quality based on multiple factors:

```python
quality_prompt = f"""
Assess the quality of this developer blog article (0-100 score):

Title: {article.title}
Author: {article.author}
Content: {article.content}

Quality factors:
- Technical accuracy and depth
- Writing clarity and structure
- Practical applicability
- Originality and insights
- Evidence and examples

Provide: {{"quality_score": 85, "reasoning": "Well-structured with practical examples..."}}
"""
```

### 3. Content Summarization

Generate concise summaries for reading lists:

```python
summary_prompt = f"""
Create a 2-3 sentence summary of this article for a developer reading list:

Title: {article.title}
Content: {article.content}

Focus on:
- Key insights or takeaways
- Practical value for developers
- Specific audience (junior/senior developers, managers, etc.)

Summary:
"""
```

### 4. Trend Detection

Identify emerging topics and themes:

```python
trend_analysis_prompt = f"""
Analyze these article titles and summaries from the past week to identify trends:

Articles:
{weekly_articles}

Identify:
1. Emerging technologies or practices
2. Common themes or topics
3. Shift in developer interests
4. Notable industry developments

Format as: {{"trends": [...],"themes": [...],"analysis": "..."}}
"""
```

### 5. Feed Discovery

Assist in discovering and evaluating new blog sources:

```python
feed_evaluation_prompt = f"""
Evaluate this blog for inclusion in our developer reading list:

Blog Name: {blog.name}
URL: {blog.url}
Description: {blog.description}
Recent Posts: {recent_posts}

Assess:
- Content quality and depth
- Relevance to developer audience
- Publishing frequency and consistency
- Author expertise and credibility
- Category alignment

Recommendation: {{"include": true/false, "score": 0-100, "reasoning": "..."}}
"""
```

## Implementation Patterns

### 1. Copilot Client Setup

```python
from src.ai.copilot_client import CopilotClient

class ArticleClassifier:
    def __init__(self):
        self.copilot = CopilotClient(
            api_key=os.getenv('COPILOT_API_KEY'),
            model='gpt-4',
            timeout=30
        )
    
    async def classify_article(self, article: Article) -> Dict[str, float]:
        prompt = self._build_classification_prompt(article)
        response = await self.copilot.complete(prompt)
        return self._parse_classification_response(response)
```

### 2. Batch Processing

Process multiple articles efficiently:

```python
async def classify_batch(self, articles: List[Article]) -> Dict[str, Dict[str, float]]:
    tasks = [self.classify_article(article) for article in articles]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    classifications = {}
    for article, result in zip(articles, results):
        if isinstance(result, Exception):
            logger.error(f"Classification failed for {article.id}: {result}")
            continue
        classifications[article.id] = result
    
    return classifications
```

### 3. Error Handling & Fallbacks

```python
async def classify_with_fallback(self, article: Article) -> Dict[str, float]:
    try:
        # Primary: Copilot classification
        return await self.copilot_classify(article)
    except CopilotAPIError as e:
        logger.warning(f"Copilot classification failed: {e}")
        # Fallback: Keyword-based classification
        return self.keyword_classify(article)
    except Exception as e:
        logger.error(f"Classification error: {e}")
        # Final fallback: Default categories
        return self.default_classification()
```

### 4. Rate Limiting & Caching

```python
from functools import lru_cache
import time

class RateLimitedCopilot:
    def __init__(self, requests_per_minute=50):
        self.rate_limit = requests_per_minute
        self.last_request_time = 0
        
    @lru_cache(maxsize=1000)
    def cached_classify(self, content_hash: str) -> Dict[str, float]:
        # Cache results to avoid re-classifying identical content
        return self._classify_content(content_hash)
    
    async def classify(self, article: Article) -> Dict[str, float]:
        # Rate limiting
        now = time.time()
        time_since_last = now - self.last_request_time
        min_interval = 60 / self.rate_limit
        
        if time_since_last < min_interval:
            await asyncio.sleep(min_interval - time_since_last)
        
        self.last_request_time = time.time()
        
        # Use cached result if available
        content_hash = hashlib.md5(article.content.encode()).hexdigest()
        return self.cached_classify(content_hash)
```

## Prompt Engineering Best Practices

### 1. Structured Prompts

Use consistent, structured prompts for reliable results:

```python
CLASSIFICATION_TEMPLATE = """
TASK: Classify developer blog article relevance

ARTICLE:
Title: {title}
Author: {author}
Content: {content_excerpt}
Tags: {tags}

CATEGORIES:
{category_definitions}

OUTPUT FORMAT:
JSON object with category scores (0-100):
{{"category_name": score, ...}}

RULES:
- Only include scores > 10%
- Scores represent relevance percentage
- Consider both explicit and implicit relevance
- Focus on practical value for developers
"""
```

### 2. Few-Shot Examples

Provide examples for better classification accuracy:

```python
def build_classification_prompt(self, article: Article) -> str:
    examples = [
        {
            "title": "Building Scalable Microservices at Netflix",
            "classification": {"technical_excellence": 95, "process_culture": 30}
        },
        {
            "title": "The Manager's Guide to 1:1 Meetings",
            "classification": {"communication_collaboration": 90, "leadership_mentoring": 75}
        }
    ]
    
    return self.template.format(
        article=article,
        examples=examples,
        categories=self.categories
    )
```

### 3. Validation & Consistency

Validate Copilot responses for consistency:

```python
def validate_classification(self, scores: Dict[str, float]) -> bool:
    # Check score ranges
    if any(score < 0 or score > 100 for score in scores.values()):
        return False
    
    # Check category names
    valid_categories = set(self.category_config.keys())
    if not set(scores.keys()).issubset(valid_categories):
        return False
    
    # Check minimum relevance threshold
    if all(score < 10 for score in scores.values()):
        return False
    
    return True
```

## Monitoring & Analytics

### 1. Classification Accuracy

Track classification performance over time:

```python
class ClassificationMetrics:
    def __init__(self):
        self.metrics = {
            'total_classifications': 0,
            'successful_classifications': 0,
            'failed_classifications': 0,
            'average_confidence': 0.0,
            'category_distribution': defaultdict(int)
        }
    
    def record_classification(self, article_id: str, scores: Dict[str, float], success: bool):
        self.metrics['total_classifications'] += 1
        if success:
            self.metrics['successful_classifications'] += 1
            # Update category distribution
            for category, score in scores.items():
                if score > 50:  # High relevance threshold
                    self.metrics['category_distribution'][category] += 1
        else:
            self.metrics['failed_classifications'] += 1
```

### 2. Cost Tracking

Monitor API usage and costs:

```python
class CopilotUsageTracker:
    def __init__(self):
        self.daily_usage = defaultdict(lambda: {'requests': 0, 'tokens': 0})
    
    def track_request(self, tokens_used: int):
        today = datetime.now().strftime('%Y-%m-%d')
        self.daily_usage[today]['requests'] += 1
        self.daily_usage[today]['tokens'] += tokens_used
    
    def get_monthly_cost(self) -> float:
        # Calculate estimated costs based on token usage
        total_tokens = sum(day['tokens'] for day in self.daily_usage.values())
        return total_tokens * COST_PER_TOKEN
```

## Configuration

### Environment Variables

```bash
# Required
COPILOT_API_KEY=your_copilot_api_key
GITHUB_TOKEN=your_github_token

# Optional
COPILOT_MODEL=gpt-4  # Default model to use
COPILOT_TIMEOUT=30   # Request timeout in seconds
COPILOT_RATE_LIMIT=50  # Requests per minute
COPILOT_MAX_RETRIES=3  # Retry failed requests
```

### Copilot Configuration (`config/copilot.yaml`)

```yaml
copilot:
  model: "gpt-4"
  temperature: 0.1  # Low temperature for consistent classification
  max_tokens: 1000
  timeout: 30
  
  classification:
    batch_size: 10
    min_confidence: 0.7
    retry_on_failure: true
    cache_results: true
    
  quality_assessment:
    enabled: true
    min_quality_score: 60
    
  summarization:
    max_length: 200
    style: "technical"
    
  trend_analysis:
    enabled: true
    analysis_frequency: "weekly"
    min_articles_for_trend: 5
```

This integration allows the Dev Blog Spelunker to leverage AI for intelligent content processing while maintaining reliability through proper error handling, caching, and fallback mechanisms.