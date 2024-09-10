import requests
from bs4 import BeautifulSoup
import json

# URL of the Bing News search page
url = 'https://www.bing.com/news/search?q=ufo&qft=interval%3d%227%22&form=PTFTNR'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # List to store the news data
    news_list = []

    # Find all news items on the page
    news_items = soup.find_all('div', class_='news-card')

    # Loop through the news items and gather details
    for item in news_items:
        # Find the title of the news item
        title = item.find('a', class_='title').text.strip()
        
        # Find the URL of the news item
        link = item.find('a', class_='title')['href']
        
        # Find the description of the news item
        description = item.find('div', class_='snippet').text.strip() if item.find('div', class_='snippet') else 'No description'
        
        # Find the image URL of the news item (checking for both 'src' and 'data-src')
        image_tag = item.find('img')
        image_url = image_tag.get('src') or image_tag.get('data-src') if image_tag else 'No image'
        
        # Append the news item details to the list
        news_list.append({
            'title': title,
            'link': link,
            'description': description,
            'image_url': image_url
        })
    
    # Define the file path for the JSON file
    json_file_path = 'ufonews.json'
    
    # Write the news data to the JSON file (overwriting the file)
    with open(json_file_path, 'w') as json_file:
        json.dump(news_list, json_file, indent=4)
    
    print(f"News data successfully written to {json_file_path}")
    
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
