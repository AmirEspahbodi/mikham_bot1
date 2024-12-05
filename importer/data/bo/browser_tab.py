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
        print("start goto mikham ...")
        pages = self.resource.pages
        await asyncio.gather(*[self._visit_page(page) for page in pages])
        print("end goto mikham ...")


    async def _visit_page(self, page: Page):
        try:
            print(" 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ")
            await page.goto(self.start_url, timeout=120000)

            print(" 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 ")

            # after visiting page we must authenticate to system, for some case we msut import ads on guest mode, so wee need these selectors to be load
            await page.wait_for_selector(
                '//div[contains(@class, "header-right")]//div[contains(@class, "header-button")]'
            )
            print(" 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 ")

            await page.wait_for_selector(
                '//div[contains(@class, "header-right")]//div[contains(@class, "signin-area")]'
            )
            print(" 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 ")
        except Exception as e:
            pass

        page_content = await page.content()
        
        print("********** writing goto to goto_mikham.html")
        with open("../goto_mikham_visit_page.html", 'w') as fw:
            fw.write(page_content)