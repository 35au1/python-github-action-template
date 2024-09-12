import os
import requests
from lxml import html
import json

def scrape_titles():
    url = "https://www.pracuj.pl/praca/fujitsu;kw"
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []

    # Parse the page content
    tree = html.fromstring(response.content)

    # Use the provided XPath to locate job titles
    titles_xpath = '//*[@id="offers-list"]/div/div[1]/div[2]/div/div[1]/div[2]/h2'
    title_elements = tree.xpath(titles_xpath)

    # Extract and clean the job titles
    titles = [title.text_content().strip() for title in title_elements if title.text_content()]

    if titles:
        print(f"Found {len(titles)} job titles.")
    else:
        print("No job titles found.")

    return titles

def main():
    titles = scrape_titles()

    if titles:
        # Write the job titles to 'titles.json' in the current directory
        file_path = 'titles.json'
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(titles, f, ensure_ascii=False, indent=4)
            print(f"Job titles successfully written to {file_path}")
        except IOError as e:
            print(f"Error writing file: {e}")
    else:
        print("No titles found to write.")

if __name__ == "__main__":
    main()
