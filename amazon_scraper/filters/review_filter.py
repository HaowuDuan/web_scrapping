def filter_by_stars(reviews, star_rating):
    """Filter reviews by star rating"""
    if star_rating == 1:  # All reviews
        return reviews
    
    filtered_reviews = []
    for review in reviews:
        try:
            review_stars = int(review.stars)
            if review_stars == star_rating:
                filtered_reviews.append(review)
        except (ValueError, TypeError):
            continue
    
    return filtered_reviews
