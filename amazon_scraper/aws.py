import asyncio
import traceback

from patchright.async_api import async_playwright
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]


async def create_stealth_context(browser):
    """创建隐身浏览器上下文"""
    context = await browser.new_context(
        user_agent=random.choice(user_agents),
    )

    # 添加隐身脚本
    await context.add_init_script(path='auth/stealth.min.js')

    return context


async def main(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled'
            ]
        )

        try:
            # 创建隐身上下文
            context = await create_stealth_context(browser)
            page = await context.new_page()

            # 设置额外的反检测措施
            await page.set_extra_http_headers({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })

            # 访问页面
            await page.goto(
                url,
                wait_until='networkidle',
                timeout=30000
            )
            await asyncio.sleep(1100)
        except Exception as e:
            traceback.print_exc()
# [2600:9000:2753:2600:7:49a5:5fd5:9881]:443
# 127.0.0.1:7890
if __name__ == '__main__':
    # https://www.amazon.com/product-reviews/{product_id}/ref=acr_dp_hist_1
    # asyncio.run(main('https://www.amazon.com/dp/B08N5WRWNW'))
    # asyncio.run(main('https://www.amazon.com/product-reviews/B08N5WRWNW/ref=acr_dp_hist_1'))
    # asyncio.run(main('https://www.amazon.com/Queen-Size-Piece-Sheet-Set/dp/B06WWRCZXX?th=1'))
    asyncio.run(main('https://www.amazon.com/s?k=Large+Language+Model'))
    # https://www.amazon.com/Amazon-Basics-Lightweight-Microfiber-14-Inch/dp/B00Q7OB1TM/ref=sr_1_1