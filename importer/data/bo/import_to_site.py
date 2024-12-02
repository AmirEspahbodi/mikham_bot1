import traceback
import gc
from playwright.async_api import Page
from random import randint
import asyncio
from data.dto import RecordSchema
from typing import Any
from config import RuntimeResource
from config.app import AppConfig
from utils.save_faild_records import save_failed_records
from .import_data import (
    click_on_add_listing_on_mikham,
    select_listing_category,
    select_listing_type,
    enter_listing_title,
    enter_listing_description,
    select_listing_province,
    select_listing_city,
    enter_listing_coordinate,
    enter_listing_phone_number,
    upload_listing_logo,
    enter_listing_website,
    enter_listing_active_hours,
    upload_listing_galery,
)
from .mikham_auth import mikham_logout, mikham_authentication
from core import MikhamImportException, MikhamAuthenticationException


class ImportToSiteBo:
    def __init__(self):
        self.resource = RuntimeResource()

    async def import_data(
        self,
        data: list[dict[str, Any]],
        province: str,
        city: str,
        category: str,
        listing_type: str,
    ):
        pages: list[Page] = self.resource.pages
        index = 0
        done = False
        while not done:
            print("here 1")
            asyncio_gather_input = []
            for page in pages:
                if index >= len(data):
                    done = True
                    break
                page
                record = data[index]
                asyncio_gather_input.append(
                    self.do_import(page, record, province, city, category, listing_type)
                )
                index += 1
            await asyncio.gather(*asyncio_gather_input)
            asyncio_gather_input.clear()
            gc.collect()

    async def do_import(
        self,
        page: Page,
        record: dict[str, Any],
        province: str,
        city: str,
        category: str,
        listing_type: str,
    ):
        try:
            record_schema = RecordSchema.model_validate(record)
            # authentication
            await mikham_authentication(page, phone_number=record_schema.phone_number)

            # import data to data fieldds
            await click_on_add_listing_on_mikham(page)
            await select_listing_category(page, category)
            await select_listing_type(page, listing_type)
            await enter_listing_title(page, record_schema.title)
            await enter_listing_description(page, record_schema.title)
            await select_listing_province(page, province)
            await select_listing_city(page, city)
            await enter_listing_coordinate(
                page, record_schema.latitude, record_schema.longitude
            )
            await enter_listing_phone_number(page, record_schema.phone_number)
            await upload_listing_logo(page, record_schema.pictures_path)
            await enter_listing_website(page, record_schema.website)
            try:
                await enter_listing_active_hours(page, record_schema.active_hours)
            except:
                pass
            await upload_listing_galery(page, record_schema.pictures_path)

            # submit data
            await page.wait_for_timeout(1000)
            await page.locator(
                '//button[contains(@value, "submit--no-preview")]'
            ).click(timeout=240000)
            await page.wait_for_load_state("networkidle", timeout=240000)
            await page.wait_for_timeout(1000)

            # logaout
            await mikham_logout(page)

        except MikhamImportException as e:
            await mikham_logout(page)
            print(f"importer ->Error: {e}")
            traceback.print_exc()
            save_failed_records(
                {
                    "province": province,
                    "city": city,
                    "category_select": category,
                    "listing_type": listing_type,
                    **record,
                    "error": f"{e}",
                }
            )

        except MikhamAuthenticationException as e:
            print(f"importer ->Error: {e}")
            traceback.print_exc()
            save_failed_records(
                {
                    "province": province,
                    "city": city,
                    "category_select": category,
                    "listing_type": listing_type,
                    **record,
                    "error": f"{e}",
                }
            )

        except Exception as e:
            await mikham_logout(page)
            print(f"importer ->Error: {e}")
            traceback.print_exc()
            save_failed_records(
                {
                    "province": province,
                    "city": city,
                    "category_select": category,
                    "listing_type": listing_type,
                    **record,
                    "error": f"{e}",
                }
            )
