import os
import requests
from lxml import html
import json

def get_xpath_for_index(index):
    """Return the appropriate XPath for the title based on the job element index."""
    div_number = index + 1  # Convert zero-based index to one-based for XPath
    # Adjust the XPath based on your IMPORTXML structure
    return f'//div[{div_number}]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div/div[2]/div[1]'

def scrape_titles():
    url = "https://www.pracuj.pl/praca/fujitsu;kw"
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []

    # Parse the page content
    tree = html.fromstring(response.content)

    # Determine the number of job listings (divs) on the page by counting the divs
    num_jobs = len(tree.xpath('//div'))  # Adjust this if needed based on the correct job listing div structure

    if num_jobs == 0:
        print("No job listings found on the page.")
        return []

    titles = []

    for index in range(num_jobs):
        # Generate the XPath for the job title based on index
        title_xpath = get_xpath_for_index(index)

        # Extract the title using the dynamically generated XPath
        title_elements = tree.xpath(title_xpath)
        title = title_elements[0].strip() if title_elements else 'No title found'

        print(f"Title for job {index+1}: {title}")
        titles.append(title)

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
