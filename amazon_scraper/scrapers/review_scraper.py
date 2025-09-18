import time
from parsers.data_extractor import DataExtractor
from auth.session_manager import SessionManager

class ReviewScraper:
    """Scrape reviews from Amazon product pages"""
    
    def __init__(self, session_manager=None):
        self.session_manager = session_manager or SessionManager()
    
    def scrape_reviews(self, product_url, max_pages=10):
        """Scrape all reviews from Amazon product review pages"""
        all_reviews = []
        
        try:
            # Extract ASIN from product URL
            asin = self._extract_asin(product_url)
            if not asin:
                print(f"Could not extract ASIN from URL: {product_url}")
                return []
            
            print(f"Found ASIN: {asin}")
            
            # Start with the dedicated review page
            for page in range(1, max_pages + 1):
                try:
                    # Construct the review-specific URL
                    if page == 1:
                        review_url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
                    else:
                        review_url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={page}"
                    
                    print(f"Scraping review page {page}: {review_url}")
                    response = self.session_manager.get(review_url)
                    response.raise_for_status()
                    
                    # Extract reviews from this page
                    page_reviews = DataExtractor.extract_reviews_from_product(response.text)
                    
                    if not page_reviews:
                        print(f"No more reviews found on page {page}")
                        break
                    
                    all_reviews.extend(page_reviews)
                    print(f"Found {len(page_reviews)} reviews on page {page}")
                    
                    # If we got fewer than 10 reviews, we might be at the end
                    if len(page_reviews) < 10:
                        print("Few reviews found, might be at the end of reviews")
                        break
                    
                except Exception as e:
                    print(f"Error scraping page {page}: {e}")
                    break
            
            print(f"Total reviews scraped: {len(all_reviews)}")
            return all_reviews
            
        except Exception as e:
            print(f"Error scraping reviews: {e}")
            return []
    
    def _extract_asin(self, product_url):
        """Extract ASIN from Amazon product URL"""
        try:
            # Handle different Amazon URL formats
            if '/dp/' in product_url:
                # Standard format: /dp/ASIN/
                asin = product_url.split('/dp/')[1].split('/')[0].split('?')[0]
            elif '/product/' in product_url:
                # Alternative format: /product/ASIN/
                asin = product_url.split('/product/')[1].split('/')[0].split('?')[0]
            elif '/gp/product/' in product_url:
                # Another format: /gp/product/ASIN/
                asin = product_url.split('/gp/product/')[1].split('/')[0].split('?')[0]
            else:
                # Try to find ASIN pattern in URL
                import re
                asin_match = re.search(r'/([A-Z0-9]{10})/', product_url)
                if asin_match:
                    asin = asin_match.group(1)
                else:
                    return None
            
            # Validate ASIN (should be 10 characters, alphanumeric)
            if len(asin) == 10 and asin.isalnum():
                return asin
            else:
                return None
                
        except Exception as e:
            print(f"Error extracting ASIN: {e}")
            return None
