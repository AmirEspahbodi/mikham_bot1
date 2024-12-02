import traceback
import asyncio
from random import random, randint
from data.dao import BrowserPage


class BaseSearchBo:
    async def _do_search(self, browser_page: BrowserPage, search_query, recursion=0):
        if recursion >= 2:
            return
        try:
            await asyncio.sleep(random() * 5)
            search_box_input_xpath = '//*[@id="root"]/div[5]/div/div[1]/div/div/input'

            await browser_page.page.locator(search_box_input_xpath).click(
                timeout=120000
            )
            await browser_page.page.wait_for_load_state("networkidle", timeout=120000)
            await browser_page.page.wait_for_selector('//div[@id="map"]')

            new_input_selector = '//*[@id="root"]/div[4]/div/div[1]/div/div/input'
            new_button_selector = '//*[@id="root"]/div[4]/div/div[1]/div/div/button[2]'
            page_search_box_input = await browser_page.page.wait_for_selector(
                new_input_selector, timeout=120000
            )
            page_search_box_button = await browser_page.page.wait_for_selector(
                new_button_selector, timeout=120000
            )

            await page_search_box_input.type(search_query)
            await page_search_box_button.press("Enter")

            await browser_page.page.wait_for_load_state("networkidle", timeout=120000)
            await browser_page.page.wait_for_timeout(randint(13000, 20000))

        except Exception as e:
            # self.logger.error()
            print(
                f"error in CompleteSearchBo in _do_search function\npage={browser_page.name}"
            )
            print(f"NESHAN ->Error: {e}")
            traceback.print_exc()
            self._do_search(browser_page, search_query, recursion + 1)
