from playwright.async_api import Page, Locator
from config import AppConfig
from random import randint
from playwright._impl._errors import TimeoutError
from core import MikhamImportException


async def select_listing_category(page: Page, category, recur=0):
    try:
        print(f"importer ->step 02 select_listing_category({category})")
        wanted_locator: Locator = None
        categories_selector = '//div[contains(@class, "row section-body")]//div[contains(@class, "ac-category")]'
        categories_locators = await page.locator(categories_selector).all()
        for category_locator in categories_locators:
            category_name = category_locator.locator(
                '//span[contains(@class, "category-name")]'
            ).first
            if (await category_name.inner_text()).strip() == category.strip():
                wanted_locator = category_locator
                break

        if wanted_locator is None:
            raise MikhamImportException("category not found")
        await wanted_locator.click(timeout=120000)
        await page.wait_for_load_state("networkidle", timeout=120000)
        await page.wait_for_timeout(1000)

    except TimeoutError as e:
        if recur < 3:
            await select_listing_category(page, category, recur + 1)
