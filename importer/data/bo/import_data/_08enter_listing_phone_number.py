from playwright.async_api import Page
from config import AppConfig
from playwright._impl._errors import TimeoutError


async def enter_listing_phone_number(page: Page, phone_number: str, recur=0):
    try:
        if phone_number:
            phone_number = phone_number.replace(" ", "").replace("+98", "0")
            print(f"importer ->step 09 enter_listing_phone_number({phone_number})")

            input_selector = '//*[@id="job_phone"]'
            listing_phone_number_box_input = await page.wait_for_selector(
                input_selector, timeout=AppConfig.IMPORTER_TIME_OUT
            )
            await listing_phone_number_box_input.type(phone_number)
            await page.wait_for_load_state("networkidle", timeout=120000)
    except TimeoutError as e:
        if recur < 3:
            await enter_listing_phone_number(page, phone_number, recur + 1)
