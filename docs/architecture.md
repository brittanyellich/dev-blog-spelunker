# Dev Blog Spelunker Architecture

## Overview

The Dev Blog Spelunker is an automated system that discovers, ingests, classifies, and curates developer blog content into weekly reading lists. The system is powered by GitHub Actions and integrates with GitHub Copilot for intelligent content analysis.

## System Goals

- **Discover**: Automatically find and collect RSS feeds from developer blogs
- **Ingest**: Parse RSS feeds and extract article metadata and content
- **Classify**: Categorize articles into 8 balanced engineering categories with relevance scores
- **Curate**: Generate weekly reading lists of top articles by category
- **Automate**: Fully automated pipeline using GitHub Actions

## Architecture Components

### 1. Data Collection Layer
- **RSS Feed Discovery**: Automated discovery of new developer blogs
- **Feed Registry**: Centralized registry of known RSS feeds
- **Feed Ingestion**: Scheduled parsing and content extraction

### 2. Content Processing Layer
- **Article Parser**: Extract title, content, metadata from RSS items
- **Content Classifier**: AI-powered categorization into 8 categories
- **Relevance Scorer**: Calculate relevance percentage for each category
- **Duplicate Detection**: Identify and handle duplicate articles

### 3. Curation Layer
- **Ranking Engine**: Score articles based on relevance and quality metrics
- **List Generator**: Create weekly reading lists by category
- **Export Engine**: Generate markdown/JSON outputs for consumption

### 4. Integration Layer
- **GitHub Actions**: Orchestrate the entire pipeline
- **GitHub Copilot**: Power intelligent content analysis
- **GitHub Pages**: Host generated reading lists
- **GitHub API**: Store and version control all data

## Core Categories

The system classifies content into 8 balanced engineering categories:

1. **🔧 Technical Excellence** - Engineering skills beyond frameworks
2. **💬 Communication & Collaboration** - Human interaction skills
3. **🚀 Career & Growth** - Long-term success strategies
4. **🧠 Mental Models & Problem Solving** - Complex problem approaches
5. **⚖️ Work-Life Integration** - Sustainable practices
6. **🌱 Leadership & Mentoring** - Growing influence
7. **🔄 Process & Culture** - Systems that shape work
8. **🎯 Impact & Purpose** - Making work meaningful

## Technology Stack

- **Language**: Python 3.9+ (for RSS parsing, ML classification)
- **ML/AI**: GitHub Copilot API, scikit-learn, transformers
- **Data Storage**: JSON files in Git repository
- **Orchestration**: GitHub Actions
- **Output**: Markdown files, JSON APIs
- **Hosting**: GitHub Pages

## Security & Privacy

- All data stored in public GitHub repository
- No personal data collection beyond public RSS feeds
- Rate limiting to respect blog servers
- Respect robots.txt and RSS feed guidelines