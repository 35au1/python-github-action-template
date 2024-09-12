import requests
import json

def fetch_html(page_num):
    url = f"https://it.pracuj.pl/praca?pn={page_num}"
    response = requests.get(url)
    return response.text

def main():
    html_contents = {}

    for page_num in range(2, 4):  # Fetch HTML for pages 2 and 3
        html_contents[f'page_{page_num}'] = fetch_html(page_num)

    # Save HTML content to oferty.json
    with open('oferty.json', 'w', encoding='utf-8') as f:
        json.dump(html_contents, f, ensure_ascii=False, indent=4)

    print("HTML content saved to oferty.json")

if __name__ == "__main__":
    main()
