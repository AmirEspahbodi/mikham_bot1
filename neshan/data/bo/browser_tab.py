from random import random, randint
import asyncio
import traceback
from playwright.async_api import Page

from config import RuntimeResource
from data.dao import BrowserPage
from .base_search import BaseSearchBo


class BrowserTabBo(BaseSearchBo):
    def __init__(self, start_url):
        self.start_url = start_url
        self.resource = RuntimeResource()

    async def goto_neshan(self) -> list[BrowserPage]:
        browser_pages = self.resource.browser_pages

        await asyncio.gather(
            *[self.__visit_page(browser_page.page) for browser_page in browser_pages]
        )

        await asyncio.gather(
            *[
                self.__complete_before_you_continue_page(browser_page.page)
                for browser_page in browser_pages
            ]
        )

    async def __visit_page(self, page: Page, recur=0, reload=False):
        try:
            await asyncio.sleep(random() * 5)
            if reload:
                await page.reload(timeout=120000)
            else:
                await page.goto(self.start_url, timeout=120000)
            await page.wait_for_timeout(randint(13000, 20000))
        except Exception as e:
            if recur < 3:
                await self.__visit_page(page, recur + 1, True)

    async def __complete_before_you_continue_page(self, page: Page):
        selector = "//div[contains(@role, 'main')]//div[contains(@class, 'AIC7ge')]//div[contains(@class, 'VtwTSb')]//form[@action='https://consent.google.com/save'][2]"
        accept_all = page.locator(selector)
        if await accept_all.count():
            await accept_all.click(timeout=120000)
            await page.wait_for_timeout(randint(13000, 20000))
