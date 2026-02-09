from playwright.async_api import Page
from config import AppConfig
from playwright._impl._errors import TimeoutError
from random import randint


async def upload_listing_logo(page: Page, image_name, recur=0):
    try:
        if image_name:
            input_selector = '//*[@id="job_logo"]'
            image_path = f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{AppConfig.PICTURES_DIRECTORY}/{image_name}"
            print(f"importer ->step 10 upload_listing_logo({image_path})")

            # listing_logo_box_input = await page.wait_for_selector(
            #     input_selector, timeout=AppConfig.IMPORTER_TIME_OUT
            # )
            # await listing_logo_box_input.click(timeout=120000)
            # await listing_logo_box_input.set_input_files(image_path)
            # await page.locator(f'text={image_path}').click(timeout=120000)
            # await page.wait_for_load_state("networkidle", timeout=120000)
            # await page.randint(13000, 20000)

            await page.set_input_files(input_selector, image_path)
            await page.wait_for_load_state("networkidle", timeout=120000)
            await page.wait_for_timeout(1000)
    except TimeoutError as e:
        if recur < 3:
            await upload_listing_logo(page, image_name, recur + 1)
