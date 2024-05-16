import sys
from googlesearch import search
from bs4 import BeautifulSoup
import requests

def search_for_html_code(query, num_pages, html_code):
    # Iterate over search results
    for url in search(query, num_results=int(num_pages), lang='en'):
        print(f"Scanning website: {url}")  # Log the website being scanned
        try:
            # Fetch the content of the URL
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                # Search for the exact HTML code
                if str(soup).find(html_code) != -1:
                    return f"Match found at {url}"
        except Exception as e:
            print(f"Failed to retrieve or parse {url}: {str(e)}")
    return "No match found"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py 'search term' number_of_pages")
    else:
        query = sys.argv[1]
        num_pages = sys.argv[2]
        html_code_to_find = '<h3 class="widgettitle"><span>Random Posts</span></h3>'
        result = search_for_html_code(query, num_pages, html_code_to_find)
        print(result)

