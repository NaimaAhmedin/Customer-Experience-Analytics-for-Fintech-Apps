# Customer Experience Analytics for Fintech Apps

A Real-World Data Engineering Challenge: Scraping, Analyzing, and Visualizing Google Play Store Reviews

## 📋 Project Overview

This project analyzes customer satisfaction with mobile banking apps by collecting and processing user reviews from the Google Play Store for three Ethiopian banks:

- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

The project simulates a consulting role at Omega Consultancy, advising banks on improving their mobile apps to enhance customer retention and satisfaction.

## 🎯 Business Objective

Support Ethiopian banks in improving their mobile banking applications by:

- Analyzing user sentiment and feedback
- Identifying satisfaction drivers and pain points
- Providing data-driven recommendations for app improvement
- Enhancing customer retention and competitive positioning

## 📊 Scenarios Addressed

### Scenario 1: Retaining Users

Analysis of performance issues like slow loading during transfers across banks.

### Scenario 2: Enhancing Features

Extraction of desired features through keyword and theme analysis.

### Scenario 3: Managing Complaints

Clustering and tracking complaints to guide AI chatbot integration.

## 🏗️ Project Structure

Customer-Experience-Analytics-for-Fintech-Apps/
├── data/
│ ├── raw/ # Original scraped data
│ └── processed/ # Cleaned and processed data
├── src/
│ ├── scraping.py # Web scraping scripts
│ ├── clean_reviews.py # Data cleaning and preprocessing
│ ├── sentiment_analysis.py # Sentiment analysis implementation
│ ├── thematic_analysis.py # Theme extraction and clustering
│ ├── load_to_postgres.py # PostgreSQL integration
│ ├── visualize.py # Basic visualizations
│ ├── Insights.py # Driver and pain point analysis
│ └── isualizations.py # Enhanced visualizations for Task 4
├── reports/
│ ├── figures/ # All visualization images
│ └── insights/ # Analysis reports and insights
├── database/
│ └── schema.sql # Database schema definition
├── tests/ # Unit tests
├── requirements.txt # Python dependencies
└── README.md # This file

## 📚 Tasks Completed

### Task 1: Data Collection and Preprocessing

- **Objective**: Scrape and preprocess reviews from Google Play Store
- **Key Components**:
  - Used `google-play-scraper` to collect 400+ reviews per bank (1,200+ total)
  - Removed duplicates and handled missing data
  - Normalized dates and saved as structured CSV
- **Files**:
  - `src/scraping.py` - Web scraping implementation
  - `src/preprocessing.py` - Data cleaning pipeline

### Task 2: Sentiment and Thematic Analysis

- **Objective**: Quantify review sentiment and identify key themes
- **Key Components**:
  - Applied `distilbert-base-uncased-finetuned-sst-2-english` for sentiment analysis
  - Used TF-IDF and spaCy for keyword extraction
  - Grouped feedback into 3-5 themes per bank
- **Files**:
  - `src/sentiment_analysis.py` - Sentiment classification
  - `src/thematic_analysis.py` - Theme extraction and clustering

### Task 3: Store Cleaned Data in PostgreSQL

- **Objective**: Design and implement relational database for review data
- **Key Components**:
  - Created `bank_reviews` database with `banks` and `reviews` tables
  - Implemented proper schema with foreign key relationships
  - Inserted 1,200+ processed reviews using psycopg2
- **Files**:
  - `src/database.py` - Database connection and operations
  - `database/schema.sql` - Database schema definition

### Task 4: Insights and Recommendations ✓

- **Objective**: Derive insights, create visualizations, and recommend improvements
- **Key Components**:
  - Identified 2+ drivers and pain points per bank
  - Created 6+ visualizations (dashboard, heatmaps, radar charts)
  - Generated actionable recommendations for each bank
  - Produced 10-page final report with ethical considerations
- **Files**:
  - `src/Insights.py` - Driver and pain point analysis
  - `src/task4_visualizations.py` - Enhanced visualizations
  - `src/task4_report_structure.py` - Report generation
  - `reports/final/task4_final_report.txt` - Complete report

## 🚀 How to Run

### Prerequisites

1. Python 3.8+
2. PostgreSQL
3. Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Customer-Experience-Analytics-for-Fintech-Apps.git
cd Customer-Experience-Analytics-for-Fintech-Apps

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
sudo -u postgres psql -f database/schema.sql

Running the Analysis

# Task 1: Data collection (if needed)
python src/scraping.py

# Task 2: Sentiment analysis
python src/sentiment_analysis.py

# Task 3: Database operations
python src/database.py

# Task 4: Insights and visualizations
python src/Insights.py
python src/task4_visualizations.py
python src/task4_report_structure.py
```
