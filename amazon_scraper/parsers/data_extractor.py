from bs4 import BeautifulSoup
import re
from models.product import Product
from models.review import Review

class DataExtractor:
    """Extract data from HTML content"""
    
    @staticmethod
    def extract_products_from_search(html_content):
        """Extract product information from Amazon search results"""
        soup = BeautifulSoup(html_content, 'html.parser')
        products = []
        
        # Try multiple selectors for product containers
        product_containers = (
            soup.find_all('div', {'data-component-type': 's-search-result'}) or
            soup.find_all('div', class_='s-result-item') or
            soup.find_all('div', class_='s-widget-container') or
            soup.find_all('div', {'data-asin': True})
        )
        
        for container in product_containers[:3]:  # Limit to first 3 products
            try:
                # Extract title - try multiple selectors
                title_elem = (
                    container.find('h2', class_='a-size-mini') or
                    container.find('span', class_='a-size-medium') or
                    container.find('h2') or
                    container.find('span', {'data-component-type': 's-product-title'})
                )
                title = title_elem.get_text(strip=True) if title_elem else "Unknown Product"
                
                # Extract URL - try multiple selectors
                link_elem = (
                    container.find('a', class_='a-link-normal') or
                    container.find('a', {'data-component-type': 's-product-image'}) or
                    container.find('a', href=True)
                )
                url = ""
                if link_elem and link_elem.get('href'):
                    href = link_elem['href']
                    if href.startswith('/'):
                        url = "https://www.amazon.com" + href
                    elif href.startswith('http'):
                        url = href
                
                # Extract price - try multiple selectors
                price_elem = (
                    container.find('span', class_='a-price-whole') or
                    container.find('span', class_='a-offscreen') or
                    container.find('span', class_='a-price') or
                    container.find('span', {'data-a-color': 'price'})
                )
                price = price_elem.get_text(strip=True) if price_elem else "Price not available"
                
                # Extract rating - try multiple selectors
                rating_elem = (
                    container.find('span', class_='a-icon-alt') or
                    container.find('i', class_='a-icon-star') or
                    container.find('span', class_='a-icon-alt')
                )
                rating = "0"
                if rating_elem:
                    rating_text = rating_elem.get_text()
                    rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                    if rating_match:
                        rating = rating_match.group(1)
                
                # Extract review count - try multiple selectors
                review_elem = (
                    container.find('a', class_='a-link-normal') or
                    container.find('span', class_='a-size-base') or
                    container.find('span', {'data-component-type': 's-product-reviews'})
                )
                review_count = "0"
                if review_elem:
                    review_text = review_elem.get_text()
                    review_match = re.search(r'(\d+)', review_text.replace(',', ''))
                    if review_match:
                        review_count = review_match.group(1)
                
                if title != "Unknown Product" and url:
                    product = Product(title, url, price, rating, review_count)
                    products.append(product)
                    
            except Exception as e:
                print(f"Error extracting product: {e}")
                continue
        
        return products
    
    @staticmethod
    def extract_reviews_from_product(html_content):
        """Extract reviews from a product page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        reviews = []
        
        # Find review containers
        review_containers = soup.find_all('div', {'data-hook': 'review'})
        
        for container in review_containers:
            try:
                # Extract review content
                content_elem = container.find('span', {'data-hook': 'review-body'})
                content = content_elem.get_text(strip=True) if content_elem else ""
                
                # Extract star rating
                stars_elem = container.find('i', {'data-hook': 'review-star-rating'})
                stars = "0"
                if stars_elem:
                    stars_text = stars_elem.get_text()
                    stars_match = re.search(r'(\d+)', stars_text)
                    if stars_match:
                        stars = stars_match.group(1)
                
                # Extract author
                author_elem = container.find('span', class_='a-profile-name')
                author = author_elem.get_text(strip=True) if author_elem else "Anonymous"
                
                # Extract date
                date_elem = container.find('span', {'data-hook': 'review-date'})
                date = date_elem.get_text(strip=True) if date_elem else "Unknown date"
                
                # Check if verified purchase
                verified_elem = container.find('span', {'data-hook': 'avp-badge'})
                verified = verified_elem is not None
                
                if content:
                    review = Review(content, stars, author, date, verified)
                    reviews.append(review)
                    
            except Exception as e:
                print(f"Error extracting review: {e}")
                continue
        
        return reviews
