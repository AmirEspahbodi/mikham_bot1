from playwright.async_api import Page, Locator
from lxml import etree
import traceback
from utils import save_image


def get_real_img(img_srcs):
    org_img = [
        img
        for img in img_srcs
        if img != "https://neshan.org/maps/43fe554149105b93d267.svg"
        and img != "https://neshan.org/maps/79aab9fabca77694a7e7.svg"
    ]
    return org_img[0] if org_img else None


async def _07_get_listing_picture_def(page: Page, locator: Locator):
    try:
        img_selector = '//div[contains(@class, "XUaBDPb no_scroll_bar")]//div[contains(@class, "vAVlB64")]//div[contains(@class, "UQf2Vvj")]'
        await page.wait_for_selector(img_selector)
        inner_html = await page.locator(img_selector).inner_html()
        if inner_html:
            parser = etree.HTMLParser()
            tree = etree.fromstring(inner_html, parser)
            img_srcs = tree.xpath("//img/@src")
            real_img = get_real_img(img_srcs)
            if real_img:
                picture_path = await save_image(real_img)
                return picture_path

    except Exception as e:
        print(f"NESHAN ->Error: {e}")
        traceback.print_exc()
