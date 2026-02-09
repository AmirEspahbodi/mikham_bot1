from playwright.async_api import Page, Locator
import traceback


async def _04_get_listing_website_def(page: Page, locator: Locator):
    try:
        website_selector = '//div[contains(@class, "acjDw8v")]//button[contains(@class, "wE_mwzL TLOaUaH")]/p/span'
        if await page.is_visible(website_selector):
            for locator in await page.locator(website_selector).all():
                text_to_detect = (await locator.text_content()).strip()
                if "وبسایت" in text_to_detect:
                    return text_to_detect.split(":")[-1].strip()
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
