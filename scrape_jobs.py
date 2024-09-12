import requests
from lxml import html
import json

def scrape_jobs(page_num):
    url = f"https://it.pracuj.pl/praca/lodz;wp?page={page_num}&rd=0&its=product-management%2Cproject-management%2Cagile%2Cbusiness-analytics"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")
        return []

    tree = html.fromstring(response.content)

    # XPath queries for the title, company, and location
    titles = tree.xpath('//h2/a/text()')
    companies = tree.xpath('//div[contains(@class, "company-name")]/span/text()')
    locations = tree.xpath('//div[contains(@class, "job-location")]/span/text()')

    # Debug output
    print(f"Titles: {titles}")
    print(f"Companies: {companies}")
    print(f"Locations: {locations}")

    job_listings = []

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
    
    # Scrape pages 1 to 3 (or adjust as needed)
    for page_num in range(1, 4):
        jobs = scrape_jobs(page_num)
        all_jobs.extend(jobs)

    # Write the job data to 'oferty.json', overwriting if it exists
    with open('oferty.json', 'w', encoding='utf-8') as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=4)

    print(f"Job data successfully written to oferty.json")

if __name__ == "__main__":
    main()
