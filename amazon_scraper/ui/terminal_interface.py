class TerminalInterface:
    """Handle all user interactions through terminal"""
    
    @staticmethod
    def get_search_keyword():
        """Get search keyword from user"""
        return input("Enter search keyword: ").strip()
    
    @staticmethod
    def display_products(products):
        """Display found products and get user selection"""
        if not products:
            print("No products found!")
            return []
        
        print("\nFound products:")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product}")
        
        while True:
            selection = input("\nSelect products (1,2,3 or 'all'): ").strip().lower()
            
            if selection == 'all':
                return products
            
            try:
                indices = [int(x.strip()) for x in selection.split(',')]
                selected_products = []
                for idx in indices:
                    if 1 <= idx <= len(products):
                        selected_products.append(products[idx-1])
                    else:
                        print(f"Invalid selection: {idx}")
                        break
                else:
                    return selected_products
            except ValueError:
                print("Invalid input. Please enter numbers separated by commas or 'all'")
    
    @staticmethod
    def get_star_filter():
        """Get star rating filter from user"""
        print("\nReview scraping options:")
        print("1. All visible reviews (recommended - no login needed)")
        print("2. Filter by star rating (requires Amazon login)")
        
        while True:
            try:
                choice = int(input("Choose (1-2): "))
                if choice == 1:
                    return 1  # All reviews
                elif choice == 2:
                    print("\nFilter by stars?")
                    print("1. All reviews")
                    print("2. 5-star only")
                    print("3. 4-star only")
                    print("4. 3-star only")
                    print("5. 2-star only")
                    print("6. 1-star only")
                    
                    while True:
                        try:
                            star_choice = int(input("Choose star filter (1-6): "))
                            if 1 <= star_choice <= 6:
                                return star_choice
                            else:
                                print("Please enter a number between 1 and 6")
                        except ValueError:
                            print("Please enter a valid number")
                else:
                    print("Please enter 1 or 2")
            except ValueError:
                print("Please enter a valid number")
    
    @staticmethod
    def show_progress(product_title, review_count):
        """Show scraping progress"""
        print(f"✓ {product_title} complete - {review_count} reviews")
    
    @staticmethod
    def show_completion(total_reviews):
        """Show final completion message"""
        print(f"\nScraping complete! Total reviews: {total_reviews}")
        print("Results saved! View at http://localhost:5001")
    
    @staticmethod
    def show_error(message):
        """Show error message"""
        print(f"Error: {message}")
