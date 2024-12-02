from playwright.async_api import Page, Locator
import traceback


async def _02_get_listing_address_def(page: Page, locator: Locator):
    try:
        address_selector = '//div[contains(@class, "acjDw8v")]//button[contains(@class, "wE_mwzL TLOaUaH")]/p/span'
        if await page.is_visible(address_selector):
            for locator in await page.locator(address_selector).all():
                text_to_detect = (await locator.text_content()).strip()
                if "،" in text_to_detect and "شماره تماس" not in text_to_detect:
                    return text_to_detect
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
