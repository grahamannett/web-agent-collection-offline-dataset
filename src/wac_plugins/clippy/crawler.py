import asyncio

from playwright.async_api import async_playwright
from wacommon import log


class Crawler:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None

    async def __aenter__(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=self.headless)
        self.page = await self.browser.new_page()
        await self.setup_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.browser.close()
        await self.page.context.close()

    async def setup_page(self):
        # Set up any initial configurations or JS injections here
        pass

    async def navigate(self, url):
        await self.page.goto(url)
        # Optionally, capture the navigation actions here

    async def capture_actions(self):
        # Implement the logic to capture user actions
        pass


# Usage example
async def main():
    log.info("Starting the crawler")
    async with Crawler(headless=False) as crawler:
        await crawler.navigate("http://example.com")
        await crawler.capture_actions()


# var1 = 100


# if __name__ == "__main__":
#     asyncio.run(main())
