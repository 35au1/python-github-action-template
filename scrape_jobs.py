import requests
from lxml import html
import json

def get_xpath_for_index(index, field):
    """Return the appropriate XPath based on the job element index and field type."""
    div_number = index + 1  # Convert zero-based index to one-based for XPath

    if field == 'title':
        return f'/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div[{div_number}]/div[2]/div/div[1]/div[2]/div[1]/div/h2/a/text()'
    elif field == 'company':
        return f'/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div[{div_number}]/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div[2]/div/a[1]/h3/text()'
    elif field == 'location':
        return f'/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div[{div_number}]/div/div/div[1]/div[2]/div[1]/div/div/div[2]/h4/text()'
    return None

def scrape_jobs(page_num):
    url = f"https://it.pracuj.pl/praca/lodz;wp?page={page_num}&rd=0&its=product-management%2Cproject-management%2Cagile%2Cbusiness-analytics"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}. Status code: {response.status_code}")
        return []

    tree = html.fromstring(response.content)

    # Determine the number of job listings (divs) on the page
    num_jobs = len(tree.xpath('/html/body/div[1]/div[5]/div[2]/div[3]/div[1]/div[5]/div'))

    job_listings = []

    for index in range(num_jobs):
        # Determine the XPaths for title, company, and location based on index
        title_xpath = get_xpath_for_index(index, 'title')
        company_xpath = get_xpath_for_index(index, 'company')
        location_xpath = get_xpath_for_index(index, 'location')

        # Extract title, company, and location using dynamic XPaths
        title_elements = tree.xpath(title_xpath)
        company_elements = tree.xpath(company_xpath)
        location_elements = tree.xpath(location_xpath)

        title = title_elements[0].strip() if title_elements else 'No title'
        company = company_elements[0].strip() if company_elements else 'No company'
        location = location_elements[0].strip() if location_elements else 'No location'

        job = {
            'title': title,
            'company': company,
            'location': location,
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
