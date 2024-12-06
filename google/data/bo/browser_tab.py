from random import random, randint
import asyncio
import traceback
from playwright.async_api import Page, TimeoutError

from config import RuntimeResource
from data.dao import BrowserPage
from .base_search import BaseSearchBo


class BrowserTabBo(BaseSearchBo):
    def __init__(self, start_url):
        self.start_url = start_url
        self.resource = RuntimeResource()

    async def clear_search_bar(self, search_query):
        await asyncio.gather(
            *[
                self.__clear_search_bar(page, search_query)
                for page in self.resource.browsers_pages
            ]
        )

    async def __clear_search_bar(self, browser_page: BrowserPage, search_query):
        try:
            await asyncio.sleep(random() * 5)
            search_box_input_xpath = "//input[@id='searchboxinput']"

            page_search_box_input = await browser_page.page.wait_for_selector(
                search_box_input_xpath, timeout=120000
            )

            await page_search_box_input.select_text()
            await page_search_box_input.type(search_query)

            await browser_page.page.wait_for_load_state("networkidle", timeout=120000)
        except Exception as e:
            # self.logger.error()
            print(
                f"error in CompleteSearchBo in _do_search function\npage={browser_page.name}"
            )
            print(f"SCRAPER ->Error: {e}")
            traceback.print_exc()

        await self._do_search(browser_page)

    async def goto_google_map(self) -> list[BrowserPage]:
        browsers_pages = self.resource.browsers_pages
        await asyncio.gather(
            *[self.__visit_page(browser_page.page) for browser_page in browsers_pages]
        )


        # with open("..goto_google_map__visit_page.html", 'w') as fw:
        #     fw.write(await browsers_pages[0].page.content())

        await asyncio.gather(
            *[
                self.__complete_before_you_continue_page(browser_page.page)
                for browser_page in browsers_pages
            ]
        )

    async def __visit_page(self, page: Page, recur=1, reload=False):
        try:
            await page.wait_for_timeout(randint(5000, 10000))
            if not reload:
                await page.goto(self.start_url, timeout=30000 + recur * 30000)
            else:
                await page.reload(timeout=30000 + recur * 30000)
            await page.wait_for_load_state("networkidle", timeout=30000 + recur * 30000)
        except TimeoutError as e:
            print(f"try recur = {recur}\nERROR={e}")
            if recur>=3:
                raise TimeoutError(e)
            else:
                self.__visit_page(page, recur=recur+1, reload=True)

                

    async def __complete_before_you_continue_page(self, page: Page):
        selector = "//div[contains(@class, 'saveButtonContainer')][1]//form[@action='https://consent.google.com/save'][2]"
        accept_all = page.locator(selector)
        if await accept_all.count():
            await accept_all.click(timeout=120000)
            await page.wait_for_timeout(randint(13000, 20000))

                