import string
from playwright.async_api import Page
from config import AppConfig
from random import choices
import asyncio


async def mikham_signup(page: Page, phone_number: str) -> bool:
    header_signup_button_selector = '//div[contains(@class, "signin-area")]//a[2]'
    email_field_selector = '//*[@id="reg_email"]'
    username_field_selector = '//*[@id="reg_username"]'
    password_field_selector = '//*[@id="reg_password"]'
    phone_number_input_field = '//*[@id="reg_Phone"]'
    signup_button_selector = '//*[@id="c27-site-wrapper"]/div[2]/div/div/div[1]/div/div/div/section/div/div/div/div[3]/form/div[3]/button'
    auth_notices_selector = '//div[contains(@class, "auth-notices")]//div[contains(@class, "woocommerce-notices-wrapper")]'

    header_signup_button_element = await page.wait_for_selector(
        header_signup_button_selector
    )
    await header_signup_button_element.click()

    email_field_element = await page.wait_for_selector(email_field_selector)
    username_field_element = await page.wait_for_selector(username_field_selector)
    password_field_element = await page.wait_for_selector(password_field_selector)
    phone_number_in_element = await page.wait_for_selector(phone_number_input_field)
    signup_button_element = await page.wait_for_selector(signup_button_selector)

    await email_field_element.type(
        "".join(choices(string.ascii_letters + string.digits, k=30)) + "@gmail.com"
    )
    await username_field_element.type(phone_number)
    await password_field_element.type(phone_number + AppConfig.MIKHAM_PASSWORD_SUFFIX)
    await phone_number_in_element.type(phone_number)
    await asyncio.sleep(4)
    await signup_button_element.click(timeout=240000)
    # await page.wait_for_load_state("networkidle", timeout=240000)

    add_listing_to_mikham_button_selector = '//div[contains(@class, "header-right")]//div[contains(@class, "header-button")]'
    add_listing_to_mikham_button_element = await page.wait_for_selector(
        add_listing_to_mikham_button_selector, timeout=240000
    )

    if await page.is_visible(auth_notices_selector):
        auth_notices_inner_html = await page.inner_html(selector=auth_notices_selector)
        if (
            "خطا" in auth_notices_inner_html
            or "قبلا این نام کاربری ثبت شده است" in auth_notices_inner_html
            or "ERROR".lower() in auth_notices_inner_html.lower()
        ):
            return False

    return True
