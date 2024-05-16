import sys
import requests
from bs4 import BeautifulSoup

def search_audiobook(title, max_results=5):
    # Replace spaces with '+' for URL encoding
    query = title.replace(' ', '+')
    url = f'https://www.google.com/search?q={query}+audiobook'

    # Perform the request and parse the HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all search result links
    results = soup.find_all('h3', class_='LC20lb', limit=max_results)
    
    found_urls = []
    for result in results:
        link_element = result.parent
        if link_element and link_element.name == 'a':
            link = link_element['href']
            # Fetch the page and look for specific markers
            page_response = requests.get(link)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            # Check if it has similar meta tags or title
            if page_soup.find('title') and page_soup.find('link', rel='canonical') and page_soup.find('meta', property='og:title'):
                print(f"Matching page found: {link}")
                found_urls.append(link)
    
    if not found_urls:
        print("No matching results found.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python script_name.py 'Audiobook Title' number_of_results")
    else:
        title = sys.argv[1]
        try:
            max_results = int(sys.argv[2])
            search_audiobook(title, max_results)
        except ValueError:
            print("Please enter a valid number for max_results.")

