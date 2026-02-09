from playwright.async_api import Page, Locator
import traceback
from utils.clean_text import cleaning_text


async def _08_get_listing_description_def(page: Page, locator: Locator):
    try:
        about_buttin_locator = page.locator(
            '//*[@id="root"]/div[4]/div/div[2]/div/div[1]/div[4]/button[last()]'
        )
        about_buttin_inner_html = await about_buttin_locator.inner_html()
        if "درباره" in about_buttin_inner_html:
            await about_buttin_locator.click(timeout=120000)

            all_inner_texts = await page.locator(
                '//div[contains(@class, "IFmLdoz")]//div[contains(@class, "NLVsn7A")]//div[contains(@class, "YNtcnXS")]'
            ).all_inner_texts()
            for index in range(len(all_inner_texts)):
                all_inner_texts[index] = cleaning_text(all_inner_texts[index])

            return "\n".join(all_inner_texts)
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
