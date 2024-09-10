import requests
from bs4 import BeautifulSoup
import json
import re

# List of search terms
search_terms = ['ufo', 'ai+app', 'paranormal']

# Base URL for concatenating incomplete image URLs
base_url = 'https://www.bing.com'

def scrape_news(search_term):
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

    # Loop through the news items and gather details, limiting to first 5 items
    for i, item in enumerate(news_items):
        if i >= 5:
            break

        # Find the title of the news item
        title_tag = item.find('a', class_='title')
        title = title_tag.text.strip() if title_tag else 'No title'

        # Find the URL of the news item
        link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else 'No link'

        # Find the description of the news item
        description_tag = item.find('div', class_='snippet')
        description = description_tag.text.strip() if description_tag else 'No description'

        # Find the image URL of the news item (checking for both 'src' and 'data-src')
        image_tag = item.find('img')
        image_url = image_tag.get('src') or image_tag.get('data-src') if image_tag else 'No image'

        # If the image URL is relative, prepend the base URL
        if image_url and not image_url.startswith('http'):
            image_url = base_url + image_url

        # Find the date of the news item (previously called source)
        date_tag = item.find('div', class_='source')
        date = date_tag.text.strip() if date_tag else 'Unknown date'

        # Find the source of the news item (located in 'data-author' attribute in class 't_t')
        source_tag = item.find('div', class_='t_t').find('a', attrs={'data-author': True}) if item.find('div', class_='t_t') else None
        source = source_tag['data-author'].strip() if source_tag else 'Unknown source'

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

# Process each search term and save results to a JSON file
for search_term in search_terms:
    news_data = scrape_news(search_term)
    if news_data:
        # Define the file path for the JSON file
        json_file_path = f'ufonews_{search_term}.json'
        
        # Write the news data to the JSON file (overwriting the file)
        with open(json_file_path, 'w') as json_file:
            json.dump(news_data, json_file, indent=4)
        
        print(f"News data for '{search_term}' successfully written to {json_file_path}")


