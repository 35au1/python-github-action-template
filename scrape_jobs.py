import requests
from lxml import html
import json

def scrape_jobs(page_num):
    url = f"https://it.pracuj.pl/praca?pn={page_num}"
    response = requests.get(url)
    tree = html.fromstring(response.content)

    job_listings = []

    # XPath queries for the title, company, and location
    titles = tree.xpath('/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div/h2/a/text()')
    companies = tree.xpath('/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/span/text()')
    locations = tree.xpath('/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/span/text()')

    # Combine the data into job listings
    for title, company, location in zip(titles, companies, locations):
        job = {
            'title': title.strip(),
            'company': company.strip(),
            'location': location.strip(),
        }
        job_listings.append(job)

    return job_listings

def main():
    all_jobs = []
    
    for page_num in range(2, 4):  # Scrape pages 2 and 3
        jobs = scrape_jobs(page_num)
        all_jobs.extend(jobs)

    if all_jobs:
        with open('oferty.json', 'w', encoding='utf-8') as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=4)
    else:
        print("No job listings found.")

if __name__ == "__main__":
    main()
