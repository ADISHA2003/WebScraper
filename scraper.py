import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract raw HTML, title, and all text content for simplicity
    scraped_data = {
        'url': url,
        'html': str(soup),
        'title': soup.title.string if soup.title else 'No title found',
        'text': soup.get_text()
    }
    return scraped_data
