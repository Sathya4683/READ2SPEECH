import json
import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url: str) -> str:
    """
    Fetch and extract readable text from a webpage.
    
    Args:
        url (str): The URL of the webpage to scrape.
    
    Returns:
        str: Extracted text content.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise if invalid response

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Get main body text
    text = soup.get_text(separator=' ', strip=True)
    return text

if __name__ == "__main__":
    text=scrape_text_from_url("https://www.geeksforgeeks.org/introduction-of-operating-system-set-1/")
    json_string=json.dumps({"text":text})

    with open("scraped.json", "w", encoding="utf-8") as f:
        f.write(json_string)