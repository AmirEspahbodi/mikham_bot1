from playwright.async_api import Page
from config import AppConfig
from playwright._impl._errors import TimeoutError


async def enter_listing_website(page: Page, website: str, recur=0):
    try:
        if website:
            print(f"importer ->step 11 enter_listing_website({website})")
            input_selector = '//*[@id="job_website"]'
            listing_website_box_input = await page.wait_for_selector(
                input_selector, timeout=AppConfig.IMPORTER_TIME_OUT
            )
            await listing_website_box_input.type(website)
            await page.wait_for_load_state("networkidle", timeout=120000)
    except TimeoutError as e:
        if recur < 3:
            await enter_listing_website(page, website, recur + 1)
