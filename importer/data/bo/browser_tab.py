from random import random, randint
import asyncio
from playwright.async_api import Page
from config import RuntimeResource
from config import AppConfig


class BrowserTabBo:
    def __init__(self, start_url):
        self.start_url = start_url
        self.resource = RuntimeResource()

    async def goto_mikham(self) -> Page:
        print("goto mikham ...")
        pages = self.resource.pages
        await asyncio.gather(*[self._visit_page(page) for page in pages])

    async def _visit_page(self, page: Page):
        await page.goto(self.start_url, timeout=120000)

        # after visiting page we must authenticate to system, for some case we msut import ads on guest mode, so wee need these selectors to be load
        await page.wait_for_selector(
            '//div[contains(@class, "header-right")]//div[contains(@class, "header-button")]'
        )
        await page.wait_for_selector(
            '//div[contains(@class, "header-right")]//div[contains(@class, "signin-area")]'
        )
