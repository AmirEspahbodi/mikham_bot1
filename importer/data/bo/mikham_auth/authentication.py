from playwright.async_api import Page
from .login import mikham_login
from .sugnup import mikham_signup
from config import AppConfig
import asyncio
from core import MikhamAuthenticationException


async def mikham_authentication(page: Page, phone_number: str):
    print(f"in login function {phone_number}")
    if not phone_number:
        # login with mikham support account
        login_successful = await mikham_login(
            page,
            username=AppConfig.MIKHAM_DEFAULT_ACCOUNT_USERNAME,
            password=AppConfig.MIKHAM_DEFAULT_ACCOUNT_PASSWORD,
        )
        if not login_successful:
            raise MikhamAuthenticationException("could not authenticate account")
    else:
        # try to login with username=phone_number and password=phone_number
        login_successful = await mikham_login(
            page, username=phone_number, password=phone_number
        )

        if login_successful:
            return

        print("login faild, trying sign up")

        signup_successful = await mikham_signup(page, phone_number=phone_number)

        if signup_successful:
            return

        # login with mikham support account
        login_successful = await mikham_login(
            page,
            username=AppConfig.MIKHAM_DEFAULT_ACCOUNT_USERNAME,
            password=AppConfig.MIKHAM_DEFAULT_ACCOUNT_PASSWORD,
        )
        if not login_successful:
            raise MikhamAuthenticationException("could not authenticate account")
