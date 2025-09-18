import json
from config.settings import OUTPUT_FILE

class FileHandler:
    """Handle saving and loading data"""
    
    @staticmethod
    def save_results(products, reviews):
        """Save scraped data to JSON file"""
        try:
            data = {
                'products': [product.to_dict() for product in products],
                'reviews': [review.to_dict() for review in reviews],
                'total_reviews': len(reviews)
            }
            
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Data saved to {OUTPUT_FILE}")
            return True
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    @staticmethod
    def load_results():
        """Load scraped data from JSON file"""
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"No data file found: {OUTPUT_FILE}")
            return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
