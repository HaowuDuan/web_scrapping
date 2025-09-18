import time
import random
import asyncio
from patchright.async_api import async_playwright
from config.settings import REQUEST_DELAY


class SessionManager:
    """Simple Amazon public data scraper with bot detection avoidance"""
    
    def __init__(self):
        # Browser components
        self.patchright = None
        self.browser = None
        self.page = None
        self.loop = None
        
        self._setup_browser()
    
    def _setup_browser(self):
        """Initialize browser with anti-bot settings"""
        # Create async event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Start patchright
        self.patchright = self.loop.run_until_complete(async_playwright().start())
        
        # Launch browser with stealth settings
        browser_args = [
            '--no-sandbox',
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--disable-web-security',
            '--no-first-run',
            '--disable-extensions',
            '--disable-plugins'
        ]
        
        self.browser = self.loop.run_until_complete(
            self.patchright.chromium.launch(headless=True, args=browser_args)
        )
        
        # Create realistic browser context
        context = self.loop.run_until_complete(
            self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US'
            )
        )
        
        # Create page
        self.page = self.loop.run_until_complete(context.new_page())
        
        # Add anti-detection script
        self.loop.run_until_complete(self.page.add_init_script("""
            // Remove webdriver traces
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            
            // Mock plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [
                    { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
                    { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
                    { name: 'Native Client', filename: 'internal-nacl-plugin' }
                ]
            });
            
            // Add chrome object
            window.chrome = {
                runtime: {},
                loadTimes: () => ({ requestTime: performance.now() }),
                csi: () => ({ pageT: performance.now() })
            };
            
            // Clean up automation traces
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """))
    
    def get(self, url, params=None):
        """Make GET request to URL"""
        try:
            # Add random delay
            delay = REQUEST_DELAY + random.uniform(2, 5)
            time.sleep(delay)
            
            # Build full URL
            full_url = url
            if params:
                param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
                full_url = f"{url}?{param_str}"
            
            print(f"🌐 Visiting: {full_url}")
            
            # Navigate to page
            response = self.loop.run_until_complete(
                self.page.goto(full_url, wait_until='domcontentloaded', timeout=30000)
            )
            
            # Simulate human behavior
            self._simulate_human()
            
            # Wait for content to load
            time.sleep(random.uniform(3, 6))
            
            # Get page content
            content = self.loop.run_until_complete(self.page.content())
            
            # Check if blocked
            if self._is_blocked(content):
                print("🚫 Detected as bot - try again later")
                raise Exception("Bot detected")
            
            # Return mock response object
            return MockResponse(content, response.status if response else 200, full_url)
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            raise
    
    def _simulate_human(self):
        """Simulate human-like behavior"""
        # Random mouse movement
        self.loop.run_until_complete(
            self.page.mouse.move(
                random.randint(100, 800), 
                random.randint(100, 600)
            )
        )
        
        # Random scroll
        scroll_amount = random.randint(100, 400)
        self.loop.run_until_complete(
            self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        )
        
        self._wait_random(0.5, 2)
    
    def _is_blocked(self, content):
        """Check if we're being blocked by Amazon"""
        block_words = ['robot', 'captcha', 'blocked', 'unusual activity', 'verify']
        return any(word in content.lower() for word in block_words)
    
    def _wait_random(self, min_seconds, max_seconds):
        """Wait for random amount of time"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def close(self):
        """Close browser and cleanup"""
        try:
            if self.loop and not self.loop.is_closed():
                if self.page:
                    self.loop.run_until_complete(self.page.close())
                if self.browser:
                    self.loop.run_until_complete(self.browser.close())
                if self.patchright:
                    self.loop.run_until_complete(self.patchright.stop())
                self.loop.close()
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.close()
        except:
            pass


class MockResponse:
    """Simple mock response object that mimics requests.Response"""
    
    def __init__(self, content, status_code, url):
        self.text = content
        self.status_code = status_code
        self.url = url
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code} error")


# Example usage for scraping Amazon product reviews:
if __name__ == "__main__":
    # Create session
    session = SessionManager()
    
    
       
    session.close()