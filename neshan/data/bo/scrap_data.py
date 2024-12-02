import traceback
import asyncio
from lxml import etree
from data.dao import BrowserPage
from playwright.async_api import Page, Locator
from random import choice, randint
from config import RuntimeResource
from utils import save_image
from .scrap_data_help import (
    _01_get_listing_title_def,
    _02_get_listing_address_def,
    _03_get_listing_phone_number_def,
    _04_get_listing_website_def,
    _05_get_listing_coordinate_def,
    _06_get_listing_active_hours_def,
    _07_get_listing_picture_def,
    _08_get_listing_description_def,
    _01_get_listing_category_def,
)


class ScrapDataBo:
    def __init__(self):
        self.resource = RuntimeResource()

    async def scrap_page(self, search_query):
        browser_pages = self.resource.browser_pages
        in_map_listing_selectors = '//div[contains(@class, "LmsM6Yo no_scroll_bar")]//div[contains(@class, "nrFZBE4")]'
        browser_pages_listings_locator = [
            [
                locator
                for locator in await browser_page.page.locator(
                    in_map_listing_selectors
                ).all()
            ]
            for browser_page in browser_pages
        ]
        is_end = False
        listing_count = 0

        final_listings = []
        lock = asyncio.Lock()

        while not is_end:
            do_scrap_page_listing = []
            for browser_number in range(len(browser_pages)):
                if listing_count < len(browser_pages_listings_locator[0]):
                    browser_pages_listings_locator[browser_number][listing_count]
                    do_scrap_page_listing.append(
                        {
                            "page": browser_pages[browser_number].page,
                            "locator": browser_pages_listings_locator[browser_number][
                                listing_count
                            ],
                        }
                    )
                    listing_count += 1
                else:
                    is_end = True
            await asyncio.gather(
                *[
                    self._scrap_indicidual_listing(
                        item["locator"], item["page"], final_listings, lock
                    )
                    for item in do_scrap_page_listing
                ]
            )
        return final_listings

    async def _scrap_indicidual_listing(
        self,
        listing_locator: Locator,
        page: Page,
        final_listings: list,
        lock: asyncio.Lock,
    ):
        await asyncio.sleep(randint(2, 5))

        exit_buttin_selector = '//button[contains(@class, "p7_5x8U cv4hqm6")]'
        await listing_locator.click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_selector('//div[contains(@class, "XUaBDPb no_scroll_bar")]')
        await page.wait_for_selector(exit_buttin_selector)
        await page.wait_for_selector('//div[contains(@class, "ig8onIQ wuKDcn0")]')
        await page.wait_for_selector('//div[contains(@class, "ig8onIQ wuKDcn0")]')
        await page.wait_for_timeout(randint(13000, 20000))

        title = await _01_get_listing_title_def(page, listing_locator)  # OK
        address = await _02_get_listing_address_def(page, listing_locator)  # OK
        phone_number = await _03_get_listing_phone_number_def(
            page, listing_locator
        )  # OK
        website = await _04_get_listing_website_def(page, listing_locator)  # OK
        coordinates = await _05_get_listing_coordinate_def(page, listing_locator)
        active_hours = await _06_get_listing_active_hours_def(
            page, listing_locator
        )  # OK
        pictures_path = await _07_get_listing_picture_def(page, listing_locator)  # OK
        description = await _08_get_listing_description_def(page, listing_locator)  # OK

        if coordinates:
            latitude, longitude = coordinates
        else:
            latitude, longitude = None, None

        await page.locator(exit_buttin_selector).click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_selector('//div[contains(@class, "LmsM6Yo no_scroll_bar")]')

        listing_data = {
            "title": title,
            "category": "",
            "address": address,
            "phone_number": phone_number,
            "website": website,
            "latitude": latitude,
            "longitude": longitude,
            "active_hours": active_hours,
            "pictures_path": pictures_path,
            "description": description,
        }
        for k, v in listing_data.items():
            print(f"NESHAN ->{k}: {v}")
        async with lock:
            final_listings.append(listing_data)
