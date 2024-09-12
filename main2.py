import requests
from bs4 import BeautifulSoup
import json

# Define the URLs to scrape
urls = [
    'https://it.pracuj.pl/praca?pn=2',
    'https://it.pracuj.pl/praca?pn=3'
]

def scrape_job_data(url):
    job_data = []
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all job listings
        job_listings = soup.find_all('div', class_='offer-item')
        
        for job in job_listings:
            title = job.find('a', class_='offer-item__title').get_text(strip=True)
            company = job.find('div', class_='offer-item__company').get_text(strip=True)
            location = job.find('div', class_='offer-item__location').get_text(strip=True)
            
            job_data.append({
                'title': title,
                'company': company,
                'location': location
            })
    else:
        print(f"Failed to retrieve data from {url}")
    
    return job_data

def save_to_json(job_data, filename='oferty.json'):
    # Open the file in write mode and overwrite the content
    with open(filename, 'w', encoding='utf-8') as file:
        # Write data to JSON file with utf-8 encoding and indent for readability
        json.dump(job_data, file, ensure_ascii=False, indent=4)

def main():
    all_job_data = []
    
    # Scrape job data from each URL
    for url in urls:
        job_data = scrape_job_data(url)
        all_job_data.extend(job_data)
    
    # Save the collected data to a JSON file
    save_to_json(all_job_data)

if __name__ == '__main__':
    main()
