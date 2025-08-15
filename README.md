# Dev Blog Spelunker 🔍

An intelligent content curation system that discovers, classifies, and curates developer blog content into personalized weekly reading lists. Powered by GitHub Actions and GitHub Copilot for automated content analysis.

## 🎯 Purpose

The Dev Blog Spelunker addresses the challenge of information overload in the developer community by:
- **Discovering** quality developer blogs and RSS feeds
- **Classifying** articles into 8 balanced engineering categories
- **Ranking** content based on relevance, quality, and timeliness
- **Curating** weekly reading lists for different developer interests

## 🏗️ Architecture

### Core Components
- **Feed Management**: Discovers and monitors RSS feeds from developer blogs
- **Content Processing**: Extracts and normalizes article content
- **AI Classification**: Uses GitHub Copilot to categorize articles by relevance
- **Ranking Engine**: Scores articles based on multiple quality factors
- **Curation System**: Generates weekly reading lists per category

### Technology Stack
- **Python 3.9+** for core processing
- **GitHub Actions** for automation and orchestration
- **GitHub Copilot** for AI-powered content analysis
- **GitHub Pages** for hosting reading lists
- **YAML/JSON** for configuration and data storage

## 📚 Content Categories

Articles are classified into 8 balanced engineering categories:

### 🔧 Technical Excellence
*Building skills that last beyond any framework*
- Engineering practices, architecture, performance optimization
- Code quality, system design, technical debt management

### 💬 Communication & Collaboration  
*Because the best code means nothing if you can't work with humans*
- Leadership, team dynamics, feedback practices
- Cross-functional collaboration, management skills

### 🚀 Career & Growth
*Intentional choices for long-term success*
- Career development, skill building, industry trends
- Personal branding, promotion strategies

### 🧠 Mental Models & Problem Solving
*How we think about complex problems*
- Decision-making frameworks, debugging approaches
- Systems thinking, analytical methods

### ⚖️ Work-Life Integration
*Sustainable practices for long-term success*
- Productivity, learning strategies, health practices
- Time management, work-life balance

### 🌱 Leadership & Mentoring
*Growing influence without formal authority*
- Technical leadership, mentoring practices
- Building psychological safety, team building

### 🔄 Process & Culture
*The systems that shape how we work*
- Agile practices, code review culture
- Team processes, continuous improvement

### 🎯 Impact & Purpose
*Making work meaningful*
- Product thinking, business context
- Ethical technology, social impact

## 🔄 Data Flow

```
RSS Feeds → Ingestion → Classification → Ranking → Curation → Reading Lists
    ↓           ↓            ↓           ↓          ↓           ↓
Feed Registry  Raw Data   Categorized  Scored   Weekly Lists  GitHub Pages
```

## 🤖 GitHub Actions Workflows

### Daily Ingestion (`daily-ingestion.yml`)
- Runs every day at 6 AM UTC
- Fetches and parses RSS feeds
- Classifies content using Copilot
- Stores processed articles

### Weekly Curation (`weekly-curation.yml`)
- Runs every Monday at 8 AM UTC  
- Ranks articles from the past week
- Generates reading lists by category
- Publishes to GitHub Pages

### Feed Discovery (`feed-discovery.yml`)
- Runs monthly on the 1st
- Discovers new developer blogs
- Validates feed quality
- Creates PRs for new additions

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- GitHub account and repository
- GitHub Copilot API access

### Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables:
   ```bash
   GITHUB_TOKEN=your_github_token
   COPILOT_API_KEY=your_copilot_api_key
   ```
4. Customize categories and feeds in `config/`

### Running Locally
```bash
# Run daily ingestion
python -m src.pipeline.ingest_pipeline

# Run weekly curation
python -m src.pipeline.curation_pipeline

# Discover new feeds
python -m src.pipeline.discovery_pipeline
```

## 📁 Project Structure

```
dev-blog-spelunker/
├── .github/workflows/          # GitHub Actions automation
├── config/                     # Configuration files
│   ├── categories.yaml         # Category definitions
│   └── feeds.yaml             # RSS feed registry
├── docs/                      # Architecture documentation
│   ├── architecture.md        # System overview
│   ├── data-flow.md           # Data processing flow
│   ├── modules.md             # Module architecture
│   └── copilot-integration.md # AI integration details
├── data/                      # Generated data storage
│   ├── raw/                   # Daily article ingestion
│   ├── classified/            # Categorized articles
│   └── curated/              # Weekly reading lists
├── src/                       # Core application modules
│   ├── feeds/                 # RSS feed management
│   ├── content/               # Article processing
│   ├── classification/        # AI categorization
│   ├── ranking/               # Article scoring
│   ├── curation/              # List generation
│   └── utils/                 # Shared utilities
└── exports/                   # Published outputs
    ├── rss/                   # Category RSS feeds
    └── api/                   # JSON API endpoints
```

## 🔧 Configuration

### Adding New Categories
Edit `config/categories.yaml` to add or modify content categories:
```yaml
new_category:
  name: "📱 Mobile Development"
  description: "Mobile app development insights"
  keywords: ["ios", "android", "react-native", "flutter"]
  # ... additional configuration
```

### Adding New Feeds
Add to `config/feeds.yaml`:
```yaml
- id: "new-blog"
  name: "Amazing Dev Blog"
  url: "https://blog.example.com/rss"
  authority_score: 85
  category_hints: ["technical_excellence"]
```

## 📊 Monitoring & Analytics

The system tracks:
- Feed health and availability
- Classification accuracy
- Content quality metrics
- Weekly curation statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes with tests
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- [Architecture Documentation](docs/architecture.md)
- [GitHub Copilot Integration](docs/copilot-integration.md)
- [Data Flow Diagrams](docs/data-flow.md)
- [Module Documentation](docs/modules.md)