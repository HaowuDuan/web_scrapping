# Amazon Scraper Configuration

BASE_URL = "https://www.amazon.com"
SEARCH_URL = "https://www.amazon.com/s"

# Headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Request settings
REQUEST_DELAY = 1  # seconds between requests
MAX_RETRIES = 3
TIMEOUT = 10

# Output settings
OUTPUT_FILE = "scraped_data.json"
