from playwright.async_api import Page
from playwright._impl._errors import TimeoutError
from config import AppConfig
from random import randint
import traceback
import re
import unicodedata


async def click_on_add_listing_on_mikham(page: Page, recur=0):
    try:
        await page.hover("//body", timeout=120000)
        await page.mouse.wheel(0, -20000)

        print(f"importer ->step 01 click_on_add_listing_on_mikham()")
        add_listing_to_mikham_button_selector = '//div[contains(@class, "header-right")]//div[contains(@class, "header-button")]'
        add_listing_to_mikham_button_element = await page.wait_for_selector(
            add_listing_to_mikham_button_selector
        )
        await add_listing_to_mikham_button_element.click(timeout=120000)

        await page.wait_for_selector('//div[contains(@class, "row section-body")]')
        category_locators = await page.locator(
            '//div[contains(@class, "row section-body")]//div[contains(@class, "ac-category")]'
        ).all()
        for category_locator in category_locators:
            await category_locator.wait_for()
        await page.wait_for_timeout(1000)
    except TimeoutError as e:
        if recur < 3:
            await click_on_add_listing_on_mikham(page, recur + 1)

    except Exception as e:
        print(f"importer ->Error: {e}")
        traceback.print_exc()
        if recur <= 2:
            html_content = await page.inner_html("//html")
            html_content = html_content.replace("\u200b", "")
            html_content = html_content.replace("\u200c", "")
            html_content = re.sub(r"[\u200b\u200c\u200d\u2060]", "", html_content)
            html_content = unicodedata.normalize("NFKC", html_content)
            if "خطای مهم در این وبسایت رخ داده" in html_content:
                await page.go_back()
                await click_on_add_listing_on_mikham(page, recur + 1)
