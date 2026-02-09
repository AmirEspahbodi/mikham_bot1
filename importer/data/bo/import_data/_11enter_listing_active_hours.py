from playwright.async_api import Page, Locator
from data.dto.record import WeekDayHourSchema, HourSchema
from typing import Literal
import asyncio
import traceback
from playwright._impl._errors import TimeoutError


async def enter_listing_active_hours(
    page: Page, active_hours: list[WeekDayHourSchema], recur=0
):
    try:
        if active_hours:
            print(f"importer ->step 12 enter_listing_active_hours()")

            header_days_selector = '//div[contains(@class, "bl-tabs-menu")]//ul[contains(@class, "nav-tabs")]//li[contains(@role, "presentation")]'
            header_days_locator = await page.locator(header_days_selector).all()

            map_P2E_days = {
                "شنبه": "saturday",
                "یک شنبه": "sunday",
                "یکشنبه": "sunday",
                "دو شنبه": "monday",
                "دوشنبه": "monday",
                "سه شنبه": "tuesday",
                "سهشنبه": "tuesday",
                "چهار شنبه": "wednesday",
                "چهارشنبه": "wednesday",
                "پنج شنبه": "thursday",
                "پنجشنبه": "thursday",
                "جمعه": "friday",
            }
            map_days_id = {
                "saturday": "day_Saturday",
                "sunday": "day_Sunday",
                "monday": "day_Monday",
                "tuesday": "day_Tuesday",
                "wednesday": "day_Wednesday",
                "thursday": "day_Thursday",
                "friday": "day_Friday",
            }

            active_hourse_import_pre_data: list[
                dict[
                    Literal["id", "locator", "active_hour"],
                    Locator | str | WeekDayHourSchema,
                ]
            ] = []

            for header_day_locator in header_days_locator:
                header_day_text = await header_day_locator.locator(
                    "//a//span[1]"
                ).inner_text()

                this_active_hour = None

                for active_hour in active_hours:
                    if (
                        active_hour.day.strip().lower()
                        == map_P2E_days[header_day_text.strip()].strip().lower()
                    ):
                        this_active_hour = active_hour
                        break

                active_hourse_import_pre_data.append(
                    {
                        "id": map_days_id[map_P2E_days[header_day_text.strip()]],
                        "locator": header_day_locator,
                        "active_hour": this_active_hour,
                    }
                )

            for data in active_hourse_import_pre_data:
                await data["locator"].click()
                await asyncio.sleep(0.5)

                base_day_hour_add_selector = f'//div[@id="{data["id"]}"]'

                if data["active_hour"].is_open:
                    await (
                        page.locator(
                            base_day_hour_add_selector
                            + '//input[contains(@value, "open-all-day")]'
                        )
                        .locator("xpath=..")
                        .click()
                    )

                elif data["active_hour"].is_close:
                    await (
                        page.locator(
                            base_day_hour_add_selector
                            + '//input[contains(@value, "closed-all-day")]'
                        )
                        .locator("xpath=..")
                        .click()
                    )
                    continue

                elif data["active_hour"].hours:
                    active_hours: list[HourSchema] = data["active_hour"].hours
                    for active_hour in active_hours:
                        await page.locator(
                            base_day_hour_add_selector
                            + '//input[contains(@class, "add-row-button")]'
                        ).click()
                        await asyncio.sleep(0.5)

                        active_hour_box_selector = (
                            base_day_hour_add_selector
                            + '//li[contains(@class, "day-hour-ranges")][last()]'
                        )
                        active_hour_from_selector = (
                            active_hour_box_selector + "/span[1]"
                        )
                        active_hour_to_selector = active_hour_box_selector + "/span[2]"
                        active_hour_add_input = (
                            '//input[contains(@class, "select2-search__field")]'
                        )
                        wanted_hour_option_selector = (
                            '//li[contains(@class, "select2-results__option")]'
                        )

                        await page.locator(active_hour_from_selector).click()
                        await asyncio.sleep(0.5)
                        await page.locator(active_hour_add_input).type(
                            active_hour.from_hour
                        )
                        await asyncio.sleep(0.5)
                        await page.locator(wanted_hour_option_selector).click()

                        await asyncio.sleep(0.5)
                        await page.locator(active_hour_to_selector).click()
                        await asyncio.sleep(0.5)
                        await page.locator(active_hour_add_input).type(
                            active_hour.from_hour
                        )
                        await asyncio.sleep(0.5)
                        await page.locator(wanted_hour_option_selector).click()

            await asyncio.sleep(0.5)

    except TimeoutError as e:
        print(f"importer ->Error: {e}")
        traceback.print_exc()
        # if recur < 3:
        #     await enter_listing_active_hours(page, active_hours, recur + 1)
