from typing import Literal
import random
from playwright.async_api import (
    async_playwright,
    Playwright as AsyncPlaywright,
    Browser,
)
import logging
from utils import Singleton
from data.dao import BrowserPage
from data.user_agents import _CHROME, _WEBKIT


class RuntimeResource(metaclass=Singleton):
    playwright: AsyncPlaywright
    browsers: dict[Literal["firefox", "safari", "chrome"], Browser]
    browsers_pages = list[BrowserPage]

    def __init__(self):
        print("SCRAPER ->initialising resource ...")
        self.browsers: dict[Literal["firefox", "safari", "chrome"], Browser] = {}
        self.browsers_pages: list[BrowserPage] = []
        self.playwright: AsyncPlaywright = None
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    async def initialize_browsers(self):
        if not self.browsers:
            print("SCRAPER ->initializing playwright ...")
            self.playwright = await async_playwright().start()
            self.browsers = {
                # "firefox": await self.playwright.firefox.launch(headless=False),
                "safari": await self.playwright.webkit.launch(headless=True),
                "chrome": await self.playwright.chromium.launch(headless=True),
            }


    async def open_browser_tabs(self):
        print("SCRAPER ->opening browser tabs")
        if not self.browsers_pages:
            chrome_page1 = await (
                await self.browsers["chrome"].new_context(
                    user_agent=random.choice(_CHROME)
                )
            ).new_page()

            # firefox_page1 = await (await self.browsers["firefox"].new_context()).new_page()

            safari_page1 = await (
                await self.browsers["safari"].new_context(
                    user_agent=random.choice(_WEBKIT)
                )
            ).new_page()

            chrome_page2 = await (
                await self.browsers["chrome"].new_context(
                    user_agent=random.choice(_CHROME)
                )
            ).new_page()
            # # firefox_page2 = await (await self.browsers["firefox"].new_context()).new_page()
            safari_page2 = await (
                await self.browsers["safari"].new_context(
                    user_agent=random.choice(_WEBKIT)
                )
            ).new_page()

            # chrome_page3 = await (
            #     await self.browsers["chrome"].new_context(user_agent=random.choice(_CHROME))
            # ).new_page()
            self.browsers_pages = [
                BrowserPage("chrome_page_1", chrome_page1),
                # BrowserPage("firefox_page_1", firefox_page1),
                BrowserPage("safari_page_1", safari_page1),
                BrowserPage("chrome_page_2", chrome_page2),
                # BrowserPage("firefox_page_2", firefox_page2),
                BrowserPage("safari_page_2", safari_page2)
                # BrowserPage("chrome_page_3", chrome_page3),
            ]
            # for page in self.browsers_pages:
            #     page.page.on("console", lambda msg: logging.info(f"Console Log: {msg.text}"))
            #     page.page.on("request", lambda req: logging.info(f"Request: {req.method} {req.url}"))
            #     page.page.on("response", lambda res: logging.info(f"Response: {res.status} {res.url}"))


    async def close_browser_tabs(self):
        print("SCRAPER ->closing browser tabs")
        if self.browsers_pages:
            for tab in self.browsers_pages:
                await tab.page.close()
            self.browsers_pages.clear()

    async def free(self):
        if self.browsers:
            for name, browser in self.browsers.items():
                try:
                    print(f"SCRAPER ->Closing {name} browser ...")
                    await browser.close()
                except Exception as e:
                    print(f"SCRAPER ->Failed to close {name} browser: {e}")

            self.browsers.clear()

        if self.playwright:
            try:
                print("SCRAPER ->Stopping Playwright ...")
                await self.playwright.stop()
                self.playwright = None
            except Exception as e:
                print(f"SCRAPER ->Failed to stop Playwright: {e}")
