# Data Flow Architecture

## System Data Flow

```
[RSS Feeds] → [Ingestion] → [Classification] → [Ranking] → [Curation] → [Output]
     ↓              ↓             ↓             ↓           ↓          ↓
[Feed Registry] [Raw Articles] [Categorized] [Scored] [Reading Lists] [GitHub Pages]
```

## Detailed Data Flow

### 1. Input Sources
- **Feed Registry** (`config/feeds.json`): Curated list of developer blog RSS feeds
- **External RSS Feeds**: Live RSS feeds from various developer blogs
- **GitHub Copilot**: AI assistance for content analysis

### 2. Data Ingestion Pipeline

#### Step 1: Feed Discovery & Collection
```
RSS Feeds → Feed Parser → Raw Article Data
```
- Scheduled GitHub Action fetches all registered RSS feeds
- Parse RSS/Atom XML to extract article metadata
- Store raw articles in `data/raw/articles/YYYY-MM-DD.json`

#### Step 2: Content Processing
```
Raw Articles → Content Extractor → Full Article Content
```
- Extract full article content from URLs when available
- Clean and normalize text content
- Extract metadata (author, publish date, tags, etc.)

### 3. Classification Pipeline

#### Step 3: AI-Powered Classification
```
Article Content → Copilot Classifier → Category Scores
```
- Use GitHub Copilot to analyze article content
- Generate relevance scores (0-100%) for each of 8 categories
- Store classification results in `data/classified/YYYY-MM-DD.json`

#### Categories with Classification Criteria:
1. **🔧 Technical Excellence** (engineering practices, architecture, code quality)
2. **💬 Communication & Collaboration** (teamwork, leadership, soft skills)
3. **🚀 Career & Growth** (career advice, skill development, industry trends)
4. **🧠 Mental Models & Problem Solving** (thinking frameworks, debugging)
5. **⚖️ Work-Life Integration** (productivity, health, learning strategies)
6. **🌱 Leadership & Mentoring** (technical leadership, mentorship)
7. **🔄 Process & Culture** (team processes, code review, agile practices)
8. **🎯 Impact & Purpose** (product thinking, business context, ethics)

### 4. Ranking & Scoring

#### Step 4: Multi-Factor Scoring
```
Classified Articles → Ranking Engine → Scored Articles
```

**Scoring Factors:**
- **Relevance Score**: Category relevance percentage from classification
- **Recency Score**: How recent the article is (decay over time)
- **Authority Score**: Blog/author reputation and credibility
- **Engagement Score**: Social signals, backlinks (if available)

**Final Score Calculation:**
```
Final Score = (Relevance × 0.4) + (Recency × 0.3) + (Authority × 0.2) + (Engagement × 0.1)
```

### 5. Curation & Output

#### Step 5: Weekly List Generation
```
Scored Articles → List Generator → Reading Lists
```
- Generate top 5-10 articles per category for the week
- Create combined "Editor's Choice" cross-category list
- Output formats: Markdown, JSON, RSS

#### Step 6: Publication
```
Reading Lists → GitHub Pages → Public Access
```
- Commit generated lists to repository
- Deploy via GitHub Pages
- Update RSS feeds for subscribers

## Data Storage Structure

```
data/
├── raw/
│   ├── articles/
│   │   ├── 2024-01-01.json      # Daily article ingestion
│   │   └── 2024-01-02.json
│   └── feeds/
│       └── feed-status.json      # Feed health monitoring
├── classified/
│   ├── 2024-01-01.json          # Classified articles with scores
│   └── 2024-01-02.json
├── curated/
│   ├── weekly/
│   │   ├── 2024-W01.json        # Weekly reading lists
│   │   └── 2024-W02.json
│   └── monthly/
│       └── 2024-01.json         # Monthly summaries
└── exports/
    ├── rss/
    │   ├── technical-excellence.xml
    │   └── all-categories.xml
    └── api/
        └── latest.json          # API endpoint data
```

## Integration Points

### GitHub Copilot Integration
- **Content Analysis**: Classify articles into categories
- **Quality Assessment**: Evaluate article quality and relevance
- **Trend Detection**: Identify emerging topics and themes
- **Summary Generation**: Create article summaries for lists

### GitHub Actions Integration
- **Scheduled Ingestion**: Daily RSS feed processing
- **Weekly Curation**: Generate reading lists every Monday
- **Feed Discovery**: Monthly discovery of new blogs
- **Health Monitoring**: Check feed availability and update status

### External Integrations
- **RSS Feeds**: Primary content source
- **Web Scraping**: Full article content extraction
- **GitHub Pages**: Hosting for generated content
- **GitHub API**: Version control and data storage