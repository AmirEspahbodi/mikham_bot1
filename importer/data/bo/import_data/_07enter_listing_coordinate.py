from playwright.async_api import Page
from config import AppConfig
from random import randint
from playwright._impl._errors import TimeoutError


async def enter_listing_coordinate(
    page: Page, latitude: float, longitude: float, recur=0
):
    try:
        print(f"importer ->step 08 enter_listing_coordinate({latitude}, {longitude})")

        enter_coordinate_button_selector = (
            '//div[contains(@class, "enter-coordinates-toggle")]'
        )
        await (await page.wait_for_selector(enter_coordinate_button_selector)).click(
            timeout=120000
        )
        await page.wait_for_timeout(500)
        latitude_selector = '//*[@id="lat"]'
        longitude_selector = '//*[@id="lng"]'
        latitude_locator = page.locator(latitude_selector).first
        longitude_locator = page.locator(longitude_selector).first
        await latitude_locator.clear()
        await longitude_locator.clear()
        await latitude_locator.type(str(latitude))
        await longitude_locator.type(str(longitude))
        await page.wait_for_timeout(500)
    except TimeoutError as e:
        if recur < 3:
            await enter_listing_coordinate(page, latitude, longitude, recur + 1)
