import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------
# STEP 1: SETUP AND DOWNLOAD REQUIRED NLP LEXICONS
# We use NLTK's VADER, which is specifically built to 
# analyze sentiments in social media and product reviews.
# ---------------------------------------------------------
print("Downloading NLTK VADER lexicon...")
nltk.download('vader_lexicon', quiet=True)
analyzer = SentimentIntensityAnalyzer()

# ---------------------------------------------------------
# STEP 2: LOAD / CREATE THE DATASET
# To make this easily runnable, we will create a mock dataset
# of realistic product reviews. 
# ---------------------------------------------------------
print("\nLoading dataset...")
data = {
    'Review_ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Review_Text': [
        "I absolutely love this product! It works flawlessly and looks great.",
        "Terrible experience. The item broke after just two days of use.",
        "It's okay. Not the best, but it gets the job done for the price.",
        "Highly recommend! Fast shipping and excellent customer service.",
        "I am very disappointed. The color doesn't match the picture at all.",
        "Five stars! This is exactly what I was looking for.",
        "Meh. It's just an average product. Nothing special.",
        "Waste of money. Do not buy this!",
        "Exceeded my expectations, the build quality is premium.",
        "It arrived on time."
    ]
}

df = pd.DataFrame(data)

# ---------------------------------------------------------
# STEP 3: PERFORM SENTIMENT ANALYSIS
# We will create a function to calculate the sentiment score
# and categorize it as Positive, Negative, or Neutral.
# ---------------------------------------------------------
print("Analyzing sentiments...")

def get_sentiment(text):
    # Get the sentiment scores (returns a dictionary with pos, neg, neu, and compound)
    scores = analyzer.polarity_scores(text)
    
    # The 'compound' score ranges from -1 (very negative) to +1 (very positive)
    compound_score = scores['compound']
    
    # Classify the sentiment based on the compound score
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Apply the function to our Review_Text column to create a new column
df['Sentiment'] = df['Review_Text'].apply(get_sentiment)

print("\n--- Analysis Complete. Here is a preview: ---")
print(df[['Review_Text', 'Sentiment']].head())

# ---------------------------------------------------------
# STEP 4: SAVE THE RESULTS TO A CSV FILE
# ---------------------------------------------------------
output_file = 'sentiment_analysis_results.csv'
df.to_csv(output_file, index=False)
print(f"\nSuccessfully saved the analyzed dataset to '{output_file}'")

# ---------------------------------------------------------
# STEP 5: VISUALIZE THE RESULTS (BONUS)
# Create a simple bar chart to show the count of each sentiment
# ---------------------------------------------------------
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

plt.figure(figsize=(8, 5))
# Count how many positive, negative, and neutral reviews there are
sentiment_counts = df['Sentiment'].value_counts()

# Create a bar plot using pandas built-in plotting
sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'], alpha=0.7)
plt.title('Customer Review Sentiment Analysis', fontsize=14, fontweight='bold')
plt.xlabel('Sentiment Category', fontsize=12)
plt.ylabel('Number of Reviews', fontsize=12)
plt.xticks(rotation=0)

# Save the chart
plt.savefig('screenshots/sentiment_distribution.png')
plt.close()

print("Successfully generated a sentiment distribution chart in the 'screenshots' folder.")
print("\n--- TASK 4 COMPLETE ---")