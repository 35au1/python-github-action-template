import requests
from bs4 import BeautifulSoup
import json

def scrape_jobs(page_num):
    url = f"https://it.pracuj.pl/praca?pn={page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    job_listings = []
    
    for job_card in soup.find_all('div', class_='listing-item'):
        title_element = job_card.find('h2')
        company_element = job_card.find('span', class_='listing-item__company')
        location_element = job_card.find('span', class_='listing-item__location')
        
        if title_element and company_element and location_element:
            job = {
                'title': title_element.text.strip(),
                'company': company_element.text.strip(),
                'location': location_element.text.strip(),
            }
            job_listings.append(job)
    
    return job_listings

def main():
    all_jobs = []
    
    for page_num in range(2, 4):  # Scrape pages 2 and 3
        jobs = scrape_jobs(page_num)
        all_jobs.extend(jobs)

    with open('oferty.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
