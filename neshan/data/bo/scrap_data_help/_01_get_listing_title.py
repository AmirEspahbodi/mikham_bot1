from playwright.async_api import Page, Locator
import traceback


async def _01_get_listing_title_def(page: Page, locator: Locator):
    try:
        title_locator = (
            '//div[contains(@class, "sL2Yt59")]/h1[contains(@class, "ZzIY7hD")]'
        )
        if await page.is_visible(title_locator):
            return (await page.locator(title_locator).first.text_content()).strip()
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
