from playwright.async_api import Page
import asyncio


async def mikham_logout(page: Page) -> bool:
    print("here in logout funciton")
    print("clear context and cookies")

    user_dropdown_menu_selector = '//*[@id="user-dropdown-menu"]'
    logout_button = (
        '//*[@id="c27-site-wrapper"]/header/div[2]/div/div[3]/div[1]/div[1]/ul/li[6]/a'
    )

    # print("here in logout")
    # print("hover on user_dropdown_menu_selector")
    # await page.wait_for_selector(user_dropdown_menu_selector)
    # await page.locator(user_dropdown_menu_selector).hover()
    # await page.locator(user_dropdown_menu_selector).click()
    # await page.wait_for_selector(logout_button)
    # await page.locator(logout_button).click()
    # await page.wait_for_load_state('networkidle')

    await page.context.clear_cookies()
    await page.evaluate("() => window.localStorage.clear()")
    await page.evaluate("() => window.sessionStorage.clear()")
    await page.reload(timeout=240000)
    await page.wait_for_selector(
        '//div[contains(@class, "header-right")]//div[contains(@class, "header-button")]'
    )
    await page.wait_for_selector(
        '//div[contains(@class, "header-right")]//div[contains(@class, "signin-area")]'
    )
