import os
import pandas as pd
from openai import OpenAI
from kaggle_secrets import UserSecretsClient
import random

user_secrets = UserSecretsClient()
api_key = user_secrets.get_secret("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Load the dataset (ensure the correct path and file name)
#df = pd.read_csv("/kaggle/input/newdatacleaned/0-cleaned_books_with_descriptions_subset.csv")


# Function to format the prompt
def format_prompt(title, author, isbn13):
    # Create a prompt for the model
    prompt = f"""
    Generate a concise, complete and precise description for the following book:

    Title: {title}
    Author: {author}
    ISBN13: {isbn13}

    Description:
    """
    return prompt



# Function to get GPT-3.5 response
def get_gpt_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specializing in book descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()  # Correctly access the content
    except Exception as e:
        return f"Error: {e}"


# Function to fetch a description with a fallback
def fetch_description_with_fallback(isbn, title=None, author=None, existing_description=None):
    if existing_description == "No description found":
        return get_gpt_response(format_prompt(title, author, isbn))
    
    return existing_description

for i in range(9, 10):
    # Read the dataset
    books = pd.read_csv(f"/kaggle/input/newdatacleaned/{i}-cleaned_books_with_descriptions_subset.csv", on_bad_lines="skip")
    
    # Apply the function only if the description is missing or invalid
    books['description'] = books.apply(
        lambda row: fetch_description_with_fallback(
            row['isbn13'], 
            row.get('title'), 
            row.get('author'), 
            row.get('description')
        ), 
        axis=1
    )
    
    books['description'] = books['description'].str.replace('\n', ' ', regex=False)
    
    # Print a sample of the updated DataFrame
    print(books[['isbn13', 'description']].head(10))
    
    # Optionally save the updated subset to a new file
    books.to_csv(f"{i}ai-cleaned_books_with_descriptions_subset.csv", index=False)