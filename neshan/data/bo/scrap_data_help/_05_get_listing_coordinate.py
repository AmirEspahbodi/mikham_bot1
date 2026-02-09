from playwright.async_api import Page, Locator
import traceback


async def _05_get_listing_coordinate_def(page: Page, locator: Locator):
    try:
        copy_coordinate_selector = '//div[contains(@class, "acjDw8v")]//button[contains(@class, "wE_mwzL TLOaUaH")]'
        for locator in await page.locator(copy_coordinate_selector).all():
            if "مختصات جغرافیایی" in await locator.locator("//p//span").text_content():
                await locator.click(timeout=120000)
                copied_text = await page.evaluate("navigator.clipboard.readText()")
                return [coor.strip() for coor in copied_text.split(",")]
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
