import random
from playwright.async_api import (
    async_playwright,
    Playwright as AsyncPlaywright,
    Browser,
)

from utils import Singleton
from data.dao import BrowserPage
from data.user_agents import _CHROME, _WEBKIT


class RuntimeResource(metaclass=Singleton):
    playwright: AsyncPlaywright
    browser: Browser
    browser_pages = list[BrowserPage]

    def __init__(self):
        print("NESHAN ->initialising resource ...")
        self.browser: Browser = {}
        self.browser_pages: list[BrowserPage] = []
        self.browser_type: str

    async def initialize_browsers(self):
        if not self.browser:
            print("NESHAN ->initializing playwright ...")
            self.playwright = await async_playwright().start()
            self.browser_type = "chrome" if random.randint(0, 1) == 0 else "safari"
            self.browser = (
                await self.playwright.webkit.launch(headless=True)
                if self.browser_type == "safari"
                else await self.playwright.chromium.launch(headless=True)
            )

    async def close_browser_tabs(self):
        print("NESHAN ->closing browser tabs")
        if self.browser_pages:
            for tab in self.browser_pages:
                await tab.page.close()
            self.browser_pages.clear()
        else:
            raise ValueError("there is no open tab")

    async def open_browser_tabs(self):
        print("NESHAN ->opening browser tabs")
        if not self.browser_pages:
            context1 = await self.browser.new_context(
                user_agent=random.choice(
                    _CHROME if self.browser_type == "chrome" else _WEBKIT
                )
            )
            context2 = await self.browser.new_context(
                user_agent=random.choice(
                    _CHROME if self.browser_type == "chrome" else _WEBKIT
                )
            )
            await context1.grant_permissions(["clipboard-read"])
            await context2.grant_permissions(["clipboard-read"])

            page2 = await (context2).new_page()
            page1 = await (context1).new_page()

            self.browser_pages = [
                BrowserPage(f"{self.browser_type}_page_1", page2),
                BrowserPage(f"{self.browser_type}_page_2", page1),
            ]

        else:
            raise RuntimeError("tabs are open now, first close them")

    async def free(self):
        try:
            print(f"NESHAN ->Closing {self.browser_type} browser ...")
            await self.browser.close()
        except Exception as e:
            print(f"NESHAN ->Failed to close {self.browser_type} browser: {e}")
        self.browser = None
        try:
            print("NESHAN ->Stopping Playwright ...")
            await self.playwright.stop()
            self.playwright = None
        except Exception as e:
            print(f"NESHAN ->Failed to stop Playwright: {e}")
