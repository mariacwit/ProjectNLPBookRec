import pandas as pd

# Load the dataset
books_df = pd.read_csv(
    "NLP/Project/books.csv", 
    on_bad_lines="skip"
)

# Keep only the relevant columns
books_df = books_df[['title', 'authors', 'average_rating', 'num_pages', 'ratings_count', 'isbn13']]

# Convert 'average_rating', 'num_pages', and 'ratings_count' to numeric, coercing errors to NaN (if any)
books_df['average_rating'] = pd.to_numeric(books_df['average_rating'], errors='coerce')
books_df['num_pages'] = pd.to_numeric(books_df['num_pages'], errors='coerce')
books_df['ratings_count'] = pd.to_numeric(books_df['ratings_count'], errors='coerce')

# Handle missing values
books_df.dropna(subset=['title', 'authors'], inplace=True)  # Drop rows with missing titles or authors
books_df.fillna({'average_rating': books_df['average_rating'].mean(),  # Fill missing average ratings with the mean
                 'num_pages': books_df['num_pages'].median(),        # Fill missing num_pages with the median
                 'ratings_count': books_df['ratings_count'].median()}, inplace=True)  # Fill missing ratings_count with the median

# Remove duplicates based on 'title' and 'authors'
books_df.drop_duplicates(subset=['title', 'authors'], inplace=True)

# Save the cleaned data to a new CSV file
books_df.to_csv('cleaned_books.csv', index=False)

# Show the first few rows of the cleaned dataset to confirm
print(books_df.head())
