from playwright.async_api import Page
import asyncio


async def mikham_login(page: Page, username: str, password: str) -> bool:
    header_login_button_selector = '//div[contains(@class, "header-right")]//div[contains(@class, "signin-area")]//a[1]'
    username_input_selector = '//*[@id="username"]'
    password_input_selector = '//*[@id="password"]'
    login_button_selector = '//button[contains(@name, "login")]'
    auth_notices_selector = '//div[contains(@class, "auth-notices")]//div[contains(@class, "woocommerce-notices-wrapper")]'

    header_login_button_element = await page.wait_for_selector(
        header_login_button_selector, timeout=120000
    )
    await header_login_button_element.click()

    username_input_element = await page.wait_for_selector(
        username_input_selector, timeout=120000
    )
    password_input_element = await page.wait_for_selector(
        password_input_selector, timeout=120000
    )
    login_button_element = await page.wait_for_selector(
        login_button_selector, timeout=120000
    )

    await username_input_element.type(username)
    await asyncio.sleep(0.5)
    await password_input_element.type(password)
    await asyncio.sleep(0.5)
    await login_button_element.click(timeout=240000)
    # await page.wait_for_load_state("networkidle", timeout=240000)

    add_listing_to_mikham_button_selector = '//div[contains(@class, "header-right")]//div[contains(@class, "header-button")]'
    add_listing_to_mikham_button_element = await page.wait_for_selector(
        add_listing_to_mikham_button_selector, timeout=240000
    )

    if await page.is_visible(auth_notices_selector):
        auth_notices_inner_html = await page.inner_html(selector=auth_notices_selector)
        if (
            "خطا" in auth_notices_inner_html
            or "پاسخ شما نادرست بود - لطفاً دوباره امتحان کنید"
            in auth_notices_inner_html
            or "ERROR".lower() in auth_notices_inner_html.lower()
        ):
            return False

    return True
