from playwright.async_api import Page, Locator
from playwright._impl._errors import TimeoutError
from ._scroll_to_end import scroll_to_end
from core import MikhamImportException


async def select_listing_type(page: Page, listing_type: str, recur=0):
    try:
        print(f"importer ->step 03 select_listing_type({listing_type})")
        listing_type_drop_down_selector = '//div[contains(@class, "cts-term-select")]'
        listing_type_drop_down_element = await page.wait_for_selector(
            listing_type_drop_down_selector
        )
        await listing_type_drop_down_element.click(timeout=120000)

        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_timeout(1000)

        scroll_tag_selector = (
            '//li[contains(@class, "select2-results__option")][last()]'
        )
        listing_types_selector = '//li[contains(@class, "select2-results__option")]'
        await scroll_to_end(page, scroll_tag_selector, listing_types_selector)

        listing_type_locators = await page.locator(listing_types_selector).all()

        wanted_selector: Locator = None

        for listing_type_locator in listing_type_locators:
            listing_type_inner_text = await listing_type_locator.inner_text()
            if listing_type.strip() == listing_type_inner_text.strip():
                wanted_selector = listing_type_locator
        if not wanted_selector:
            raise MikhamImportException("listing type not found")
        await wanted_selector.click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_timeout(1000)
    except TimeoutError as e:
        if recur < 3:
            await select_listing_type(page, listing_type, recur + 1)
