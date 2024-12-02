from playwright.async_api import Page, Locator

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
import traceback


async def _03_get_listing_phone_number_def(page: Page, locator: Locator):
    try:
        phone_number_locator = '//div[contains(@class, "ig8onIQ wuKDcn0")]//button[contains(@class, "wE_mwzL TLOaUaH")]/p/span'
        if await page.is_visible(phone_number_locator):
            for locator in await page.locator(phone_number_locator).all():
                text_to_detect = (await locator.text_content()).strip()
                if "شماره تماس" in text_to_detect:
                    raw_phone = text_to_detect.split(":")[-1].strip()
                    for k, v in P2E_map.items():
                        raw_phone = raw_phone.replace(k, v)
                    return raw_phone
        else:
            return "09373110981"
    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
