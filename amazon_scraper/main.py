#!/usr/bin/env python3
"""
Amazon Product Review Scraper - Main Entry Point
Follows the exact interactive flow specified in project requirements
"""

import sys
import os
import webbrowser
import threading
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.search_scraper import SearchScraper
from scrapers.review_scraper import ReviewScraper
from ui.terminal_interface import TerminalInterface
from filters.review_filter import filter_by_stars
from storage.file_handler import FileHandler
from web_interface.app import app
from auth.session_manager import SessionManager

def launch_web_interface():
    """Launch the web interface in a separate thread"""
    time.sleep(2)  # Give time for the server to start
    webbrowser.open('http://localhost:5001')

def main():
    """Main interactive flow as specified in requirements"""
    print("🛒 Amazon Product Review Scraper")
    print("=" * 40)
    
    # Initialize session manager
    session_manager = None
    
    try:
        # Step 1: Get login credentials first
        print("🔐 Amazon login required for full access:")
        email = input("Enter your Amazon email: ").strip()
        password = input("Enter your Amazon password: ").strip()
        
        # Step 2: Get keyword
        keyword = TerminalInterface.get_search_keyword()
        if not keyword:
            print("No keyword provided. Exiting.")
            return
        
        # Step 3: Search for products with logged-in session
        print(f"\nSearching for products with keyword: '{keyword}'...")
        session_manager = SessionManager(email, password)
        search_scraper = SearchScraper(session_manager)
        products = search_scraper.search_products(keyword)
        
        if not products:
            TerminalInterface.show_error("No products found. Please try a different keyword.")
            return
        
        # Step 4: Show products and let user select
        selected_products = TerminalInterface.display_products(products)
        if not selected_products:
            print("No products selected. Exiting.")
            return
        
        # Step 5: Review scraping options
        star_choice = TerminalInterface.get_star_filter()
        
        # Step 6: Scrape reviews
        print(f"\nScraping reviews from {len(selected_products)} product(s)...")
        
        review_scraper = ReviewScraper(session_manager)
        all_reviews = []
        
        for product in selected_products:
            print(f"\nScraping: {product.title}")
            reviews = review_scraper.scrape_reviews(product.url)
            
            # Apply star filter if user chose filtering and we're logged in
            if star_choice > 1 and session_manager.logged_in:
                reviews = filter_by_stars(reviews, star_choice)
                print(f"Applied {star_choice}-star filter")
            elif star_choice > 1 and not session_manager.logged_in:
                print("⚠️  Login failed - showing all reviews instead")
            
            all_reviews.extend(reviews)
            TerminalInterface.show_progress(product.title, len(reviews))
        
        # Step 7: Save results
        print(f"\nSaving results...")
        success = FileHandler.save_results(selected_products, all_reviews)
        
        if not success:
            TerminalInterface.show_error("Failed to save results.")
            return
        
        # Step 8: Launch web view
        TerminalInterface.show_completion(len(all_reviews))
        print("Results saved! View at http://localhost:5001")
        
        # Start web server in background
        print("Starting web server...")
        web_thread = threading.Thread(target=launch_web_interface)
        web_thread.daemon = True
        web_thread.start()
        
        # Run Flask app
        app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
    except Exception as e:
        TerminalInterface.show_error(f"Unexpected error: {e}")
        print("Please check your internet connection and try again.")
    finally:
        # Clean up browser resources
        if session_manager:
            print("Cleaning up browser resources...")
            session_manager.close()

if __name__ == "__main__":
    main()
