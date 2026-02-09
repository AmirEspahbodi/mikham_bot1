from config import AppConfig
from playwright.async_api import Page, Locator
from ._scroll_to_end import scroll_to_end
from random import randint
from playwright._impl._errors import TimeoutError


async def select_listing_province(page: Page, listing_province: str, recur=0):
    try:
        print(f"importer ->step 06 select_listing_province({listing_province})")
        listing_province_drop_down_selector = '//div[contains(@class, "cts-term-hierarchy")]//div[contains(@class, "term-select-0")]'
        listing_province_drop_down_locator = page.locator(
            listing_province_drop_down_selector
        ).first
        await listing_province_drop_down_locator.click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_timeout(500)

        scroll_tag_selector = (
            '//li[contains(@class, "select2-results__option")][last()]'
        )
        listing_provinces_selector = '//li[contains(@class, "select2-results__option")]'
        await scroll_to_end(page, scroll_tag_selector, listing_provinces_selector)

        listing_province_locators = await page.locator(listing_provinces_selector).all()

        wanted_selector: Locator = None

        for listing_province_locator in listing_province_locators:
            listing_province_inner_text = await listing_province_locator.inner_text()
            if listing_province.strip() == listing_province_inner_text.strip():
                wanted_selector = listing_province_locator

        await wanted_selector.click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_timeout(500)
    except TimeoutError as e:
        if recur < 3:
            await select_listing_province(page, listing_province, recur + 1)
