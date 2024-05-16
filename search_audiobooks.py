import argparse
from googlesearch import search
import requests
from bs4 import BeautifulSoup

def count_mp3_tags(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        mp3_tags = soup.find_all('mp3')
        return len(mp3_tags)
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return 0

def find_audiobook_page(book_title, num_results=10):
    # Perform Google search for audiobook related to the book title
    query = f"{book_title} audiobook"
    print(f"Searching for '{query}'...")
    
    search_results = search(query, num_results=num_results)

    # Iterate through search results to find potential audiobook sources
    for url in search_results:
        print(f"Checking URL: {url}")
        mp3_count = count_mp3_tags(url)
        if mp3_count >= 5:
            print(f"Audiobook found at: {url}")
            return url
    
    print("No suitable audiobook found.")
    return None

if __name__ == "__main__":
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Find a webpage for downloading an audiobook.')
    parser.add_argument('book_title', help='Title of the book to search for')
    parser.add_argument('-n', '--num-results', type=int, default=10, help='Number of search results to consider (default: 10)')
    args = parser.parse_args()

    # Find a webpage for downloading the audiobook
    audiobook_url = find_audiobook_page(args.book_title, num_results=args.num_results)
    if audiobook_url:
        print(f"Website for downloading audiobook: {audiobook_url}")
    else:
        print("No suitable webpage found for downloading the audiobook.")

