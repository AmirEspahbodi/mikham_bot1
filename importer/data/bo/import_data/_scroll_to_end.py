import traceback
from config import AppConfig
from playwright.async_api import Page, Locator
from random import randint
from core import MikhamImportException
import asyncio


async def scroll_to_end(page: Page, scroll_tag_selector: str, scroll_tag_count: str):
    previously_counted = 0
    error_count = 0
    reached_end_count = 0

    while True:
        if error_count > 3:
            break

        try:
            await page.hover(scroll_tag_selector, timeout=120000)
            # await page.mouse.wheel(0, 25000)
            await page.wait_for_load_state("networkidle", timeout=120000)
            await page.wait_for_timeout(1000)
            await asyncio.sleep(1.5)
            scraped_listings_count = await page.locator(scroll_tag_count).count()
            print(
                f"scrooling...\nscraped_listings_count = {scraped_listings_count}\npreviously_counted = {previously_counted}\n"
            )
            if scraped_listings_count == previously_counted:
                reached_end_count += 1
                if reached_end_count >= 3:
                    break
            else:
                reached_end_count = 0

            previously_counted = scraped_listings_count

        except Exception as e:
            error_count += 1
            print(
                f"\nerror in CompleteSearchBo in __scroll function\nerror count = {error_count}\n"
            )
            print(f"importer ->Error: {e}")
            traceback.print_exc()
            print("importer ->\n")
            if error_count >= 3:
                raise MikhamImportException("faild to scrool")
