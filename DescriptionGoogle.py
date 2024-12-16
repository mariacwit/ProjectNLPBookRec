import requests
import pandas as pd

def fetch_description_from_google_books_isbn(isbn):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data['items'][0]['volumeInfo'].get('description', "No description available")
    return "No description found"

def fetch_description_from_google_books(isbn, title=None, author=None):
    query = f"isbn:{isbn}"
    if title:
        query += f"+intitle:{title}"
    if author:
        query += f"+inauthor:{author}"
        
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if "items" in data:
                return data['items'][0]['volumeInfo'].get('description', "No description available")
    except Exception as e:
        print(f"Error fetching description for ISBN {isbn}: {e}")
    return "No description found"


def fetch_description_with_fallback(isbn, title=None, author=None):
    description = fetch_description_from_google_books_isbn(isbn)
    if description == "No description available":
        description = fetch_description_from_google_books(isbn, title, author)
    return description


# Read the dataset
books = pd.read_csv("NLP/Project/cleaned_books.csv", on_bad_lines="skip")

# Slice the DataFrame to process only the first 1000 entries
books_subset = books.iloc[9000:].copy()

books_subset['description'] = books_subset.apply(
    lambda row: fetch_description_with_fallback(row['isbn13'], row.get('title'), row.get('author')), 
    axis=1
)

# Print a sample of the updated DataFrame
print(books_subset[['isbn13', 'description']].head(10))

# Optionally save the updated subset to a new file
books_subset.to_csv("NLP/Project/9-cleaned_books_with_descriptions_subset.csv", index=False)