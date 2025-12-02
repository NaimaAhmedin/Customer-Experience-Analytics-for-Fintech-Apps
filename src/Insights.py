import pandas as pd
import re
from collections import Counter

# Load data
df = pd.read_csv("data/processed/processed_reviews_sentiment.csv")
df['review'] = df['review'].fillna('')

print("=== STEP 3: IDENTIFY DRIVERS & PAIN POINTS ===\n")

# More comprehensive stopwords list
stopwords = {
    'the', 'and', 'for', 'this', 'that', 'with', 'have', 'has', 'had',
    'was', 'were', 'are', 'but', 'not', 'you', 'your', 'they', 'their',
    'what', 'from', 'been', 'has', 'had', 'will', 'would', 'could',
    'should', 'about', 'when', 'where', 'which', 'there', 'here',
    'just', 'like', 'very', 'much', 'many', 'some', 'then', 'than',
    'also', 'only', 'even', 'well', 'app', 'bank', 'please', 'cant',
    'dont', 'doesnt', 'its', 'one', 'all', 'now', 'use', 'used', 'using'
}

# Function to extract meaningful phrases (bigrams)
def extract_meaningful_phrases(text_series, top_n=15):
    """Extract meaningful phrases from reviews"""
    all_text = ' '.join(text_series.astype(str).tolist()).lower()
    
    # Clean text
    text = re.sub(r'[^\w\s]', '', all_text)
    words = text.split()
    
    # Filter stopwords
    filtered_words = [word for word in words if word not in stopwords and len(word) > 2]
    
    # Create bigrams (two-word phrases)
    bigrams = [' '.join(filtered_words[i:i+2]) for i in range(len(filtered_words)-1)]
    
    # Count frequency
    bigram_counts = Counter(bigrams)
    
    # Return most common bigrams that are meaningful
    meaningful_bigrams = []
    for bigram, count in bigram_counts.most_common(top_n * 2):
        # Filter out meaningless combinations
        words_in_bigram = bigram.split()
        if (words_in_bigram[0] not in stopwords and 
            words_in_bigram[1] not in stopwords and
            len(words_in_bigram[0]) > 2 and 
            len(words_in_bigram[1]) > 2):
            meaningful_bigrams.append((bigram, count))
            if len(meaningful_bigrams) >= top_n:
                break
    
    return meaningful_bigrams

# Function to categorize issues
def categorize_issue(keyword):
    """Categorize keywords into themes"""
    categories = {
        'Technical Issues': ['crash', 'bug', 'error', 'issue', 'problem', 'working', 'work', 'fix', 'update'],
        'Performance': ['slow', 'lag', 'loading', 'speed', 'time', 'wait', 'fast', 'quick'],
        'Usability': ['easy', 'hard', 'difficult', 'simple', 'complex', 'interface', 'design', 'user'],
        'Features': ['feature', 'transfer', 'payment', 'login', 'password', 'account', 'balance'],
        'Customer Service': ['support', 'service', 'help', 'response', 'contact'],
        'Security': ['secure', 'safe', 'trust', 'password', 'login', 'verification'],
        'General Sentiment': ['best', 'worst', 'nice', 'great', 'good', 'bad', 'super', 'excellent', 'terrible']
    }
    
    for category, keywords in categories.items():
        if any(kw in keyword.lower() for kw in keywords):
            return category
    
    return 'Other'

# Analyze each bank
bank_insights = {}

for bank in df['bank'].unique():
    print(f"\n{'='*60}")
    print(f"{bank.upper()} BANK - DRIVERS & PAIN POINTS")
    print(f"{'='*60}")
    
    bank_df = df[df['bank'] == bank]
    
    # DRIVERS: What users like (from 4-5 star reviews)
    high_ratings = bank_df[bank_df['rating'] >= 4]
    
    if len(high_ratings) > 0:
        print(f"\n📈 DRIVERS (from {len(high_ratings)} positive reviews):")
        
        # Extract meaningful phrases from positive reviews
        positive_phrases = extract_meaningful_phrases(high_ratings['review'])
        
        drivers = []
        for phrase, count in positive_phrases[:8]:  # Top 8 phrases
            category = categorize_issue(phrase)
            if category not in ['General Sentiment', 'Other']:
                drivers.append(f"{phrase} ({count} mentions)")
                print(f"  • {phrase}: {count} mentions")
        
        # If no categorized drivers, use general sentiment
        if not drivers and positive_phrases:
            print("  Key positive feedback:")
            for phrase, count in positive_phrases[:5]:
                print(f"  • {phrase}: {count} mentions")
    
    # PAIN POINTS: What users complain about (from 1-2 star reviews)
    low_ratings = bank_df[bank_df['rating'] <= 2]
    
    if len(low_ratings) > 0:
        print(f"\n⚠️ PAIN POINTS (from {len(low_ratings)} negative reviews):")
        
        # Extract meaningful phrases from negative reviews
        negative_phrases = extract_meaningful_phrases(low_ratings['review'])
        
        pain_points = []
        for phrase, count in negative_phrases[:8]:  # Top 8 phrases
            category = categorize_issue(phrase)
            pain_points.append((phrase, count, category))
            print(f"  • {phrase}: {count} mentions [{category}]")
        
        # Group by category for summary
        print(f"\n📋 SUMMARY BY CATEGORY:")
        category_summary = {}
        for phrase, count, category in pain_points:
            if category not in category_summary:
                category_summary[category] = 0
            category_summary[category] += count
        
        for category, total in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {total} mentions")
    
    # SPECIFIC ISSUE ANALYSIS (based on common complaints)
    print(f"\n🔍 SPECIFIC ISSUES IDENTIFIED:")
    
    # Check for specific common issues
    common_issues = {
        'Login/Account Issues': ['login', 'password', 'account', 'access', 'verification'],
        'Transaction Problems': ['transfer', 'payment', 'transaction', 'money', 'send'],
        'App Performance': ['crash', 'freeze', 'hang', 'not working', 'stop'],
        'Speed Issues': ['slow', 'loading', 'wait', 'time', 'delay'],
        'Update Problems': ['update', 'version', 'new version', 'upgrade'],
        'Customer Support': ['support', 'help', 'service', 'response']
    }
    
    for issue, keywords in common_issues.items():
        count = 0
        for review in bank_df['review']:
            if any(keyword in review.lower() for keyword in keywords):
                count += 1
        
        if count > 5:  # Only report if mentioned more than 5 times
            percentage = (count / len(bank_df)) * 100
            print(f"  • {issue}: {count} reviews ({percentage:.1f}%)")
    
    # Store insights for this bank
    bank_insights[bank] = {
        'total_reviews': len(bank_df),
        'avg_rating': bank_df['rating'].mean(),
        'positive_reviews': len(bank_df[bank_df['rating'] >= 4]),
        'negative_reviews': len(bank_df[bank_df['rating'] <= 2]),
        'drivers': extract_meaningful_phrases(high_ratings['review'])[:5] if len(high_ratings) > 0 else [],
        'pain_points': extract_meaningful_phrases(low_ratings['review'])[:5] if len(low_ratings) > 0 else []
    }

# Comparative analysis
print(f"\n{'='*60}")
print("COMPARATIVE INSIGHTS & RECOMMENDATIONS")
print(f"{'='*60}")

# Create recommendations based on analysis
recommendations = {
    'Abyssinia': [
        "1. Address 'not working' and 'fix' issues - improve app stability",
        "2. Focus on improving 'mobile banking' experience",
        "3. Reduce 'worst' mentions by fixing critical bugs first",
        "4. Implement better error handling and user feedback"
    ],
    'CBE': [
        "1. Maintain 'best' and 'nice' aspects that users love",
        "2. Address 'why' questions by improving transparency",
        "3. Fix 'branch' related issues in the app",
        "4. Continue regular 'update' cycles based on user feedback"
    ],
    'Dashen': [
        "1. Leverage 'super' and 'best' sentiment in marketing",
        "2. Address 'worst' and 'slow' performance issues",
        "3. Improve 'bill' payment features mentioned by users",
        "4. Fix 'account' and 'working' issues reported"
    ]
}

for bank in df['bank'].unique():
    print(f"\n{bank.upper()} BANK - RECOMMENDATIONS:")
    print("-" * 40)
    
    insights = bank_insights[bank]
    
    # Strength summary
    if insights['drivers']:
        print("💪 STRENGTHS to maintain:")
        for phrase, count in insights['drivers'][:3]:
            print(f"  • {phrase} ({count} mentions)")
    
    # Weakness summary
    if insights['pain_points']:
        print("\n🔧 AREAS for improvement:")
        for phrase, count in insights['pain_points'][:3]:
            print(f"  • {phrase} ({count} mentions)")
    
    # Recommendations
    print("\n🎯 ACTIONABLE RECOMMENDATIONS:")
    for rec in recommendations.get(bank, []):
        print(f"  {rec}")
    
    # Success metrics
    print(f"\n📊 TARGET METRICS for improvement:")
    print(f"  • Increase average rating from {insights['avg_rating']:.2f} to {insights['avg_rating'] + 0.3:.2f}")
    print(f"  • Reduce negative reviews from {insights['negative_reviews']} to {max(0, insights['negative_reviews'] - 50)}")
    print(f"  • Increase positive reviews by 20% in next quarter")

# Save insights to CSV
print(f"\n{'='*60}")
print("SAVING INSIGHTS TO FILE...")
print(f"{'='*60}")

# Create insights DataFrame
insights_list = []
for bank, data in bank_insights.items():
    drivers_str = ', '.join([f"{phrase}({count})" for phrase, count in data['drivers'][:3]])
    pain_points_str = ', '.join([f"{phrase}({count})" for phrase, count in data['pain_points'][:3]])
    
    insights_list.append({
        'bank': bank,
        'total_reviews': data['total_reviews'],
        'avg_rating': round(data['avg_rating'], 2),
        'positive_reviews': data['positive_reviews'],
        'negative_reviews': data['negative_reviews'],
        'top_drivers': drivers_str,
        'top_pain_points': pain_points_str,
        'sentiment_score': round(df[df['bank'] == bank]['sentiment_score'].mean(), 3)
    })

insights_df = pd.DataFrame(insights_list)

# Create reports directory if it doesn't exist
import os
os.makedirs('reports', exist_ok=True)

insights_df.to_csv('reports/bank_insights_summary.csv', index=False)

print(f"✅ Insights saved to: reports/bank_insights_summary.csv")
print(f"\n📁 File contains:")
print(f"  • Key drivers for each bank")
print(f"  • Main pain points for each bank")
print(f"  • Performance metrics")
print(f"  • Sentiment analysis")
print(f"\n🎉 STEP 3 COMPLETE! Ready for Step 4: Creating enhanced visualizations.")