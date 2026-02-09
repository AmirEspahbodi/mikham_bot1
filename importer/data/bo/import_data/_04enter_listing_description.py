from playwright.async_api import Page
from config import AppConfig
from playwright._impl._errors import TimeoutError


async def enter_listing_description(page: Page, listing_description, recur=0):
    try:
        print(f"importer ->step 05 enter_listing_description({listing_description})")
        input_selector = '//*[@id="job_description"]'
        listing_description_box_input = await page.wait_for_selector(
            input_selector, timeout=AppConfig.IMPORTER_TIME_OUT
        )
        await listing_description_box_input.type(listing_description)
        await page.wait_for_load_state("networkidle", timeout=120000)
    except TimeoutError as e:
        if recur < 3:
            await enter_listing_description(page, listing_description, recur + 1)
