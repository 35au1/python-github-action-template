import requests
from bs4 import BeautifulSoup
import json
import re

# List of search terms that will scrape 5 news items
search_terms_5_news = ['ufo', 'ai+app', 'paranormal', 'science+discovery']

# List of search terms that will scrape only 2 news items
search_terms_2_news = ['nocode', 'it+startup', 'software+trend']

# Base URL for concatenating incomplete image URLs
base_url = 'https://www.bing.com'

def clean_text(text):
    """Replace specific Unicode characters with a single quote and strip leading/trailing whitespace."""
    if text:
        # Replace specific Unicode characters with a single quote
        text = text.replace('\u201c', "'").replace('\u201d', "'")
        # Replace newlines, tabs, and multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    return text

def scrape_news(search_term, max_news_items):
    # URL of the Bing News search page with the search term
    url = f'https://www.bing.com/news/search?q={search_term}&qft=interval%3d%227%22&form=PTFTNR'

    # Extract the category from the search term
    category = search_term

    # Send a GET request to the URL with a timeout
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes (e.g., 404)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page for search term '{search_term}': {e}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to store the news data
    news_list = []

    # Find all news items on the page
    news_items = soup.find_all('div', class_='news-card')

    if not news_items:
        print(f"No news items found for search term '{search_term}', please check the HTML structure.")
        return []

    # Loop through the news items and gather details, limiting to the specified number of items
    for i, item in enumerate(news_items):
        if i >= max_news_items:
            break

        # Find the title of the news item
        title_tag = item.find('a', class_='title')
        title = clean_text(title_tag.text) if title_tag else 'No title'

        # Find the URL of the news item
        link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else 'No link'

        # Find the description of the news item
        description_tag = item.find('div', class_='snippet')
        description = clean_text(description_tag.text) if description_tag else 'No description'

        # Find the image URL of the news item (checking for both 'src' and 'data-src')
        image_tag = item.find('img')
        image_url = image_tag.get('src') or image_tag.get('data-src') if image_tag else 'No image'

        # If the image URL is relative, prepend the base URL
        if image_url and not image_url.startswith('http'):
            image_url = base_url + image_url

        # Find the date of the news item
        date_tag = item.find('div', class_='source')
        date = clean_text(date_tag.text) if date_tag else 'Unknown date'

        # Find the source of the news item
        source_tag = item.find('div', class_='t_t').find('a', attrs={'data-author': True}) if item.find('div', class_='t_t') else None
        source = clean_text(source_tag['data-author']) if source_tag else 'Unknown source'

        # Append the news item details to the list
        news_list.append({
            'title': title,
            'link': link,
            'description': description,
            'image_url': image_url,
            'category': category,  # Add category to JSON
            'date': date,          # Renamed from source to date
            'source': source       # Extracted from 'data-author' attribute in 't_t' class
        })

    return news_list

# List to accumulate news data from all search terms
all_news_data = []

# Process each search term in search_terms_5_news (scrape 5 news)
for search_term in search_terms_5_news:
    news_data = scrape_news(search_term, max_news_items=5)
    if news_data:
        all_news_data.extend(news_data)

# Process each search term in search_terms_2_news (scrape 2 news)
for search_term in search_terms_2_news:
    news_data = scrape_news(search_term, max_news_items=2)
    if news_data:
        all_news_data.extend(news_data)

# Define the file path for the JSON file
json_file_path = 'ufonews.json'

# Write the accumulated news data to the JSON file (overwriting the file)
with open(json_file_path, 'w') as json_file:
    json.dump(all_news_data, json_file, indent=4)

print(f"News data successfully written to {json_file_path}")
