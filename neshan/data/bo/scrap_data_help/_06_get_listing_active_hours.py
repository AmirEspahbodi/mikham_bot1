from playwright.async_api import Page, Locator
from config import AppConfig
import traceback

P2E_map = {
    "۱": "1",
    "۲": "2",
    "۳": "3",
    "۴": "4",
    "۵": "5",
    "۶": "6",
    "۷": "7",
    "۸": "8",
    "۹": "9",
    "۰": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
}

map_1 = {
    "0بامداد": "00",
    "1بامداد": "01",
    "2بامداد": "02",
    "3بامداد": "03",
    "4صبح": "04",
    "5صبح": "05",
    "6صبح": "06",
    "7صبح": "07",
    "12ظهر": "12",
    "1ظهر": "13",
    "2ظهر": "13",
}


async def _06_get_listing_active_hours_def(page: Page, locator: Locator):
    try:
        address_selector = '//div[contains(@class, "acjDw8v")]//div[contains(@class, "tMcwngO")]/p/span'
        if await page.is_visible(address_selector):
            for locator in await page.locator(address_selector).all():
                text_content = await locator.text_content()
                if "ساعت کاری" in text_content and any(
                    [k in text_content for k in P2E_map]
                ):
                    text_content = text_content.split("-")[-1].strip()
                    for k, v in P2E_map.items():
                        text_content = text_content.replace(k, v)
                    for k, v in map_1.items():
                        text_content = text_content.replace(k, v)
                    text_content = text_content.replace("تا", "to")
                    return f"{text_content}{AppConfig.NESHAN_ACTIVE_HOURS_END_ID}"
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
