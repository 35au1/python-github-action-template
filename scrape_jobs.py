import os
import requests
from lxml import html
import json

def get_xpath_for_index(index):
    """Return the appropriate XPath for the title based on the job element index."""
    div_number = index + 1  # Convert zero-based index to one-based for XPath
    return f'/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div[{div_number}]/div[2]/div/div[1]/div[2]/div[1]/div/h2/a/text()'

def scrape_titles():
    url = "https://www.pracuj.pl/praca/fujitsu;kw"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []

    tree = html.fromstring(response.content)

    # Determine the number of job listings (divs) on the page
    num_jobs = len(tree.xpath('/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div'))

    if num_jobs == 0:
        print("No job listings found on the page.")
        return []

    titles = []

    for index in range(num_jobs):
        # Generate the XPath for the job title based on index
        title_xpath = get_xpath_for_index(index)

        # Extract the title using the dynamically generated XPath
        title_elements = tree.xpath(title_xpath)
        title = title_elements[0].strip() if title_elements else 'No title'

        titles.append(title)

    return titles

def main():
    titles = scrape_titles()

    if titles:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, 'titles.json')
        
        print(f"Writing to {file_path}...")

        # Write the job titles to 'titles.json', overwriting if it exists
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
