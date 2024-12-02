from playwright.async_api import Page, Locator
import traceback


async def _01_get_listing_category_def(page: Page, locator: Locator):
    try:
        title_locator = '//*[@id="root"]/div[4]/div/div[2]/div/div[1]/div[2]/p'
        if await page.is_visible(title_locator):
            text = (await page.locator(title_locator).first.text_content()).strip()
            return text.split("-")[0].strip()
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
