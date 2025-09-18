import time
from urllib.parse import quote_plus
from config.settings import SEARCH_URL
from parsers.data_extractor import DataExtractor
from auth.session_manager import SessionManager

class SearchScraper:
    """Scrape Amazon search results for products"""
    
    def __init__(self, session_manager=None):
        self.session_manager = session_manager or SessionManager()
    
    def search_products(self, keyword):
        """Search for products on Amazon and return list of Product objects"""
        try:
            # Construct search URL
            search_params = {
                'k': keyword,
                'ref': 'sr_pg_1'
            }
            
            print(f"Searching for: {keyword}")
            response = self.session_manager.get(SEARCH_URL, params=search_params)
            response.raise_for_status()
            
            # Extract products from HTML
            products = DataExtractor.extract_products_from_search(response.text)
            
            print(f"Found {len(products)} products")
            return products
            
        except Exception as e:
            print(f"Error searching for products: {e}")
            return []
    
    def get_product_details(self, product_url):
        """Get detailed information from a product page"""
        try:
            response = self.session_manager.get(product_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error getting product details: {e}")
            return None
