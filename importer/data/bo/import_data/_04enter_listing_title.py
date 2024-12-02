from playwright.async_api import Page
from config import AppConfig
from playwright._impl._errors import TimeoutError


async def enter_listing_title(page: Page, listing_title, recur=0):
    try:
        print(f"importer ->step 04 enter_listing_title({listing_title})")
        input_selector = '//*[@id="job_title"]'
        listing_title_box_input = await page.wait_for_selector(
            input_selector, timeout=AppConfig.IMPORTER_TIME_OUT
        )
        await listing_title_box_input.type(listing_title)
        await page.wait_for_load_state("networkidle", timeout=120000)
    except TimeoutError as e:
        if recur < 3:
            await enter_listing_title(page, listing_title, recur + 1)
