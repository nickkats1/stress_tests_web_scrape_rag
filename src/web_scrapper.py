import requests
from bs4 import BeautifulSoup
from typing import Dict


def web_scrapper(url: str) -> Dict[str, any]:
    """
    Scrapes HTML from the given URL and returns structured data.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f'Response code from scrape: {response.status_code}')
        print(f'Success: {url}')
        
        soup = BeautifulSoup(response.content, "html.parser")

        # Paragraph tags
        paragraphs = [p.text for p in soup.find_all("p")]
        div_text = [div.text for div in soup.find_all("div")]

        # Metadata tags
        metadata_tags = soup.find_all("meta")
        metadata = {
            tag.get('name') or tag.get('property'): tag.get('content')
            for tag in metadata_tags if tag.get('content')
        }

        # Body text
        body = soup.find("body")
        body_text = body.text if body else ""


        all_text = soup.get_text(separator='\n', strip=True)

        return {
            "url": url,
            "paragraphs": paragraphs,
            "body": body_text,
            "metadata": metadata,
            "all_text": all_text,
            "div":div_text,
        }

    except requests.exceptions.RequestException as e:
        print(f'Error scraping data from {url}: {e}')
        return {}



URL_PATHS = [
    "https://apnews.com/article/bank-stress-tests-federal-reserve-private-credit-jpmorgan-citigroup-bd4c6049c0f060a6e43ec3aa229c22af",
    "https://fortune.com/2025/06/28/bank-stress-test-results-federal-reserve-dividends-stock-buybacks/",
    "https://www.bbc.co.uk/news/business-44567546"
]


if __name__ == "__main__":
    results = []

    for url in URL_PATHS:
        print(f'\n----------- Scraping URL: {url} --------------------')
        scraped_data = web_scrapper(url)
        if scraped_data:
            print(f'Length of <p> tags: {len(scraped_data["paragraphs"])}')
            print(f'Length of body text: {len(scraped_data["body"])}')
            print(f'Number of metadata tags: {len(scraped_data["metadata"])}')
            print(f'Length of all text: {len(scraped_data["all_text"])}')
            print(f'Length of <div> tags: {len(scraped_data["div"])}')

      
            filename = url.split('/')[-1] + ".txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(scraped_data["all_text"])
            print(f'Saved full text at: {filename}')

            results.append({
                "url": scraped_data["url"],
                "paragraph_count": len(scraped_data["paragraphs"]),
                "body_length": len(scraped_data["body"]),
                "metadata_count": len(scraped_data["metadata"]),
                "all_text_length": len(scraped_data["all_text"])
            })
        else:
            print("Failed to scrape HTML data")