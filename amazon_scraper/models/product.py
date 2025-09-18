class Product:
    """Simple product data structure"""
    
    def __init__(self, title, url, price, rating, review_count):
        self.title = title
        self.url = url
        self.price = price
        self.rating = rating
        self.review_count = review_count
    
    def __str__(self):
        return f"{self.title} - {self.price} ⭐{self.rating} ({self.review_count} reviews)"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'title': self.title,
            'url': self.url,
            'price': self.price,
            'rating': self.rating,
            'review_count': self.review_count
        }
