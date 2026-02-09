from config import AppConfig
from playwright.async_api import Page, Locator
from ._scroll_to_end import scroll_to_end
from random import randint
from playwright._impl._errors import TimeoutError


async def select_listing_city(page: Page, listing_city: str, recur=0):
    try:
        print(f"importer ->step 07 select_listing_city({listing_city})")
        listing_city_drop_down_selector = '//div[contains(@class, "cts-term-hierarchy")]//div[contains(@class, "term-select-1")]'
        listing_city_drop_down_locator = page.locator(
            listing_city_drop_down_selector
        ).first
        await listing_city_drop_down_locator.click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_timeout(500)

        scroll_tag_selector = (
            '//li[contains(@class, "select2-results__option")][last()]'
        )
        listing_citys_selector = '//li[contains(@class, "select2-results__option")]'
        await scroll_to_end(page, scroll_tag_selector, listing_citys_selector)

        listing_city_locators = await page.locator(listing_citys_selector).all()

        wanted_selector: Locator = None

        for listing_city_locator in listing_city_locators:
            listing_city_inner_text = await listing_city_locator.inner_text()
            if listing_city.strip() == listing_city_inner_text.strip():
                wanted_selector = listing_city_locator

        await wanted_selector.click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_timeout(500)
    except TimeoutError as e:
        if recur < 3:
            await select_listing_city(page, listing_city, recur + 1)
