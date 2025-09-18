# Amazon Product Review Scraper

A simple web scraper that searches Amazon for products and extracts reviews, following the project requirements exactly.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd amazon_scraper
   pip install -r requirements.txt
   ```

2. **Run the scraper:**
   ```bash
   python main.py
   ```

3. **Follow the interactive prompts:**
   - Enter a search keyword (e.g., "laptop", "headphones")
   - Select which products to scrape
   - Choose star rating filter
   - View results in your browser at http://localhost:5000

## Features

- ✅ Search Amazon for products
- ✅ Interactive product selection
- ✅ Star rating filtering
- ✅ Scrape all reviews from selected products
- ✅ Save results to JSON
- ✅ Web interface to view results
- ✅ Simple, clean code structure

## Project Structure

```
amazon_scraper/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── config/settings.py         # Configuration
├── models/                    # Data structures
├── scrapers/                  # Web scraping logic
├── parsers/                   # HTML parsing
├── ui/                        # Terminal interface
├── storage/                   # File handling
└── web_interface/             # Flask web app
```

## Usage Example

```
Enter search keyword: wireless headphones
Found products:
1. Sony WH-1000XM4 - $349.99 ⭐4.6 (12,543 reviews)
2. Bose QuietComfort 35 - $329.00 ⭐4.4 (8,921 reviews)
3. Apple AirPods Pro - $249.00 ⭐4.5 (15,234 reviews)

Select products (1,2,3 or 'all'): all
Filter by stars?
1. All reviews
2. 5-star only
...
Choose (1-6): 1

Scraping reviews...
✓ Sony WH-1000XM4 complete - 150 reviews
✓ Bose QuietComfort 35 complete - 120 reviews
✓ Apple AirPods Pro complete - 180 reviews

Scraping complete! Total reviews: 450
Results saved! View at http://localhost:5000
```

## Notes

- The scraper uses respectful delays between requests
- Results are saved to `scraped_data.json`
- Web interface automatically opens in your browser
- Press Ctrl+C to stop the scraper at any time
