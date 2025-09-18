import time
import random
import asyncio
import os
from patchright.async_api import async_playwright
from config.settings import REQUEST_DELAY

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]


class SessionManager:
    """Simple Amazon public data scraper with bot detection avoidance"""
    
    def __init__(self, email=None, password=None):
        # Browser components
        self.patchright = None
        self.browser = None
        self.page = None
        self.loop = None
        self.logged_in = False
        self.email = email
        self.password = password
        
        self._setup_browser()
        
        # Login if credentials provided
        if email and password:
            self.login()
    
    def _setup_browser(self):
        """Initialize browser with anti-bot settings"""
        # Create async event loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Start patchright
        self.patchright = self.loop.run_until_complete(async_playwright().start())
        
        # Launch browser with stealth settings
        browser_args = [
            '--disable-blink-features=AutomationControlled'
        ]
        
        self.browser = self.loop.run_until_complete(
            self.patchright.chromium.launch(headless=False, args=browser_args)
        )
        
        # Create realistic browser context
        context = self.loop.run_until_complete(
            self.browser.new_context(
                user_agent=random.choice(user_agents)
            )
        )
        
        # Add stealth script
        stealth_path = os.path.join(os.path.dirname(__file__), 'stealth.min.js')
        self.loop.run_until_complete(context.add_init_script(path=stealth_path))
        
        # Create page
        self.page = self.loop.run_until_complete(context.new_page())
        
        # Set extra HTTP headers
        self.loop.run_until_complete(self.page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }))
    
    def login(self):
        """Login to Amazon - opens browser for manual login"""
        try:
            print("🔐 Opening Amazon login page...")
            print("📝 Please complete the login manually in the browser window")
            print("⏳ Waiting for you to complete login...")
            
            # Navigate to Amazon login page
            login_url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=900&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fpath%3D%252Fgp%252Fyourstore%252Fhome%26signIn%3D1%26useRedirectOnSuccess%3D1%26action%3Dsign-out%26ref_%3Dnav_AccountFlyout_signout&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
            self.loop.run_until_complete(
                self.page.goto(login_url, wait_until='networkidle', timeout=30000)
            )
            
            # Wait for manual login completion
            print("🔄 Monitoring for login completion...")
            max_wait_time = 300  # 5 minutes
            check_interval = 5   # Check every 5 seconds
            waited_time = 0
            
            while waited_time < max_wait_time:
                current_url = self.page.url
                
                # Check if we're logged in (not on signin page)
                if "signin" not in current_url.lower():
                    self.logged_in = True
                    print("✅ Login completed successfully!")
                    return
                
                # Wait and check again
                self.loop.run_until_complete(asyncio.sleep(check_interval))
                waited_time += check_interval
                
                if waited_time % 30 == 0:  # Print status every 30 seconds
                    print(f"⏳ Still waiting... ({waited_time}s elapsed)")
            
            print("⏰ Login timeout - please try again")
                
        except Exception as e:
            print(f"❌ Login error: {e}")
    
    def get(self, url, params=None):
        """Make GET request to URL"""
        try:
            # Add random delay
            delay = REQUEST_DELAY + random.uniform(3, 8)
            time.sleep(delay)
            
            # Build full URL
            full_url = url
            if params:
                param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
                full_url = f"{url}?{param_str}"
            
            print(f"🌐 Visiting: {full_url}")
            
            # Navigate to page with more stealth
            response = self.loop.run_until_complete(
                self.page.goto(full_url, wait_until='domcontentloaded', timeout=30000)
            )
            
            # Simulate human behavior before getting content
            self._simulate_human()
            
            # Wait for content to load
            time.sleep(random.uniform(3, 6))
            
            # Get page content
            content = self.loop.run_until_complete(self.page.content())
            
            # Check if blocked or got 503 error
            if self._is_blocked(content) or (response and response.status == 503):
                print("🚫 Detected as bot or service unavailable - waiting longer...")
                time.sleep(random.uniform(10, 20))  # Wait longer
                raise Exception("Bot detected or service unavailable")
            
            # Return mock response object
            return MockResponse(content, response.status if response else 200, full_url)
            
        except Exception as e:
            print(f"❌ Request failed: {e}")
            raise
    
    def _simulate_human(self):
        """Simulate human-like behavior"""
        try:
            # Random mouse movement
            self.loop.run_until_complete(
                self.page.mouse.move(
                    random.randint(100, 800), 
                    random.randint(100, 600)
                )
            )
            
            # Random scroll
            scroll_amount = random.randint(200, 600)
            self.loop.run_until_complete(
                self.page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            )
            
            # Wait a bit
            self._wait_random(1, 3)
            
            # Sometimes scroll back up a bit
            if random.random() > 0.5:
                scroll_back = random.randint(50, 200)
                self.loop.run_until_complete(
                    self.page.evaluate(f"window.scrollBy(0, -{scroll_back})")
                )
                self._wait_random(0.5, 1.5)
                
        except Exception as e:
            # If simulation fails, just wait
            self._wait_random(1, 2)
    
    def _is_blocked(self, content):
        """Check if we're being blocked by Amazon"""
        # More specific blocking indicators
        block_indicators = [
            'robot or not?',
            'enter the characters you see below',
            'unusual traffic',
            'automated requests',
            'captcha',
            'access denied',
            'blocked'
        ]
        
        # Check if we got a proper Amazon page (should contain Amazon-specific elements)
        amazon_indicators = [
            'amazon.com',
            's-search-result',
            'a-size-mini',
            'a-link-normal'
        ]
        
        content_lower = content.lower()
        
        # If we see specific blocking indicators, we're blocked
        if any(indicator in content_lower for indicator in block_indicators):
            return True
            
        # If we don't see Amazon indicators, we might be blocked
        if not any(indicator in content_lower for indicator in amazon_indicators):
            return True
            
        return False
    
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