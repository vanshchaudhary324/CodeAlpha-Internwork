import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------------------------------------
# Create a folder to save our charts
# ---------------------------------------------------------
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

# ---------------------------------------------------------
# We are using Seaborn's built-in 'tips' dataset.
# It acts like a CSV file containing restaurant transaction data.
# ---------------------------------------------------------
print("Loading dataset...")
df = sns.load_dataset('tips')

print("\n--- First 5 rows of the dataset ---")
print(df.head())

# ---------------------------------------------------------
# Let's add a 'Tip Percentage' column. 
# ---------------------------------------------------------
df['tip_percentage'] = (df['tip'] / df['total_bill']) * 100

print("\nData successfully prepared. Generating visualizations...")

# ---------------------------------------------------------
# Set a clean, professional background theme for all charts
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# We will create 4 different types of charts to tell a story.
# ---------------------------------------------------------

# CHART 1: Bar Chart (Total Revenue by Day)
plt.figure(figsize=(8, 5))
sns.barplot(x='day', y='total_bill', data=df, estimator=sum, errorbar=None, palette='viridis')
plt.title('Total Restaurant Revenue by Day', fontsize=14, fontweight='bold')
plt.xlabel('Day of the Week', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)
plt.savefig('screenshots/1_revenue_by_day.png') # Save the image
plt.close() 

# CHART 2: Scatter Plot (Bill Amount vs. Tip Amount)
plt.figure(figsize=(8, 5))
sns.scatterplot(x='total_bill', y='tip', hue='time', data=df, palette='Set1', s=100)
plt.title('Relationship Between Total Bill and Tip Amount', fontsize=14, fontweight='bold')
plt.xlabel('Total Bill ($)', fontsize=12)
plt.ylabel('Tip Amount ($)', fontsize=12)
plt.legend(title='Meal Time')
plt.savefig('screenshots/2_bill_vs_tip.png')
plt.close()

# CHART 3: Histogram (Distribution of Bill Amounts)
plt.figure(figsize=(8, 5))
sns.histplot(df['total_bill'], bins=20, kde=True, color='skyblue')
plt.title('Distribution of Total Bill Amounts', fontsize=14, fontweight='bold')
plt.xlabel('Total Bill ($)', fontsize=12)
plt.ylabel('Number of Customers (Frequency)', fontsize=12)
plt.savefig('screenshots/3_bill_distribution.png')
plt.close()

# CHART 4: Box Plot (Tip Percentage by Gender and Smoking Status)
plt.figure(figsize=(8, 5))
sns.boxplot(x='sex', y='tip_percentage', hue='smoker', data=df, palette='pastel')
plt.title('Tip Percentage by Gender and Smoking Status', fontsize=14, fontweight='bold')
plt.xlabel('Customer Gender', fontsize=12)
plt.ylabel('Tip Percentage (%)', fontsize=12)
plt.legend(title='Smoker')
plt.savefig('screenshots/4_tip_percentage_boxplot.png')
plt.close()


print("\n--- TASK COMPLETE ---")
print("Successfully generated 4 charts.")
print("Please check the 'screenshots' folder in your directory to view the images!")