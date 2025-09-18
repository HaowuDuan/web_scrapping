class Review:
    """Simple review data structure"""
    
    def __init__(self, content, stars, author, date, verified):
        self.content = content
        self.stars = stars
        self.author = author
        self.date = date
        self.verified = verified
    
    def __str__(self):
        verified_text = "✓" if self.verified else ""
        return f"⭐{self.stars} {verified_text} {self.author} ({self.date}): {self.content[:100]}..."
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'content': self.content,
            'stars': self.stars,
            'author': self.author,
            'date': self.date,
            'verified': self.verified
        }
