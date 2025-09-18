#!/usr/bin/env python3
"""
Simple Amazon Login Test
"""

import asyncio
from patchright.async_api import async_playwright

async def test_login():
    """Simple login test"""
    print("🧪 Testing Amazon Login...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Get credentials
        email = input("Email: ")
        password = input("Password: ")
        
        # Navigate to login
        await page.goto("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=900&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fpath%3D%252Fgp%252Fyourstore%252Fhome%26signIn%3D1%26useRedirectOnSuccess%3D1%26action%3Dsign-out%26ref_%3Dnav_AccountFlyout_signout&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        await asyncio.sleep(2)
        
        # Fill email
        await page.fill("input[type='email']", email)
        await page.click("input[id='continue']")
        await asyncio.sleep(2)
        
        # Fill password
        await page.fill("input[name='password']", password)
        await page.click("input[id='signInSubmit']")
        await asyncio.sleep(3)
        
        # Check result
        url = page.url
        print(f"Final URL: {url}")
        
        if "signin" not in url.lower():
            print("✅ Login successful!")
        else:
            print("❌ Login failed")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_login())