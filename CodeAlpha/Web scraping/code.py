import requests
from bs4 import BeautifulSoup
import pandas as pd

# We are using a safe, public demo site meant for scraping.
url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"


print("Sending request to the website...")
response = requests.get(url)

# Check if the request was successful (Status code 200 means OK)
if response.status_code == 200:
    print("Successfully connected to the website!\n")
else:
    print(f"Failed to connect. Status code: {response.status_code}")
    exit()


# We pass the raw HTML text into BeautifulSoup to make it searchable
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the blocks of HTML that contain an individual book
# On this website, every book is wrapped in an <article class="product_pod"> tag
books = soup.find_all('article', class_='product_pod')

# Create empty lists to hold our scraped data
titles = []
prices = []
ratings = []
availabilities = []

# A simple dictionary to convert text ratings to numbers (for data cleaning later)
rating_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

print(f"Found {len(books)} books on the page. Extracting data...")


# Loop through every single book found on the page
for book in books:
    # 1. Extract Title
    # The title is inside an <h3> tag, inside an <a> tag. We grab the 'title' attribute.
    title = book.find('h3').find('a')['title']
    titles.append(title)
    
    # 2. Extract Price
    # The price is in a <p> tag with the class 'price_color'
    price_text = book.find('p', class_='price_color').text
    prices.append(price_text)
    
    # 3. Extract Rating
    # The rating is a <p> tag with a class like 'star-rating Three'.
    # We get the second class name (e.g., 'Three')
    rating_class = book.find('p', class_='star-rating')['class'][1]
    ratings.append(rating_class)
    
    # 4. Extract Availability
    # Inside a <p> tag with class 'instock availability'
    availability_text = book.find('p', class_='instock availability').text.strip()
    availabilities.append(availability_text)

# Combine all our lists into a dictionary
data = {
    'Book_Title': titles,
    'Price': prices,
    'Star_Rating': ratings,
    'Availability': availabilities
}

# Convert the dictionary into a Pandas DataFrame (like a spreadsheet)
df = pd.DataFrame(data)


print("Cleaning the data...")

# A. Clean Price: Remove the '£' symbol and convert to a decimal number (float)
# The symbol extracted might be weird depending on encoding, so we slice off the first character.
df['Price'] = df['Price'].apply(lambda x: float(x.replace('£', '').replace('Â', '')))

# B. Clean Rating: Convert words ('Three') to actual numbers (3)
df['Star_Rating'] = df['Star_Rating'].map(rating_dict)

# C. Handle Missing Values: Drop any rows that accidentally have missing (NaN) data
df = df.dropna()

# D. Remove Duplicates: Just in case the page listed the same book twice
df = df.drop_duplicates()


file_name = "scraped_science_books.csv"
df.to_csv(file_name, index=False)

print("\n--- SCRAPING COMPLETED ---")
print(f"Successfully saved clean data to '{file_name}'")
print("\nHere is a preview of the scraped data:")
print(df.head())