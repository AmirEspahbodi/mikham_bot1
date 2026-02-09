from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
import math
from config.app import AppConfig
from utils import cleaning_text


class HourSchema(BaseModel):
    from_hour: str | None = None
    to_hour: str | None = None
    model_config = ConfigDict()


class WeekDayHourSchema(BaseModel):
    day: str
    hours: list[HourSchema] = []
    is_close: bool = False
    is_open: bool = False
    model_config = ConfigDict()


class RecordSchema(BaseModel):
    title: str | None = None
    category: str | None = None
    address: str | None = None
    phone_number: str | None = None
    website: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    active_hours: list[WeekDayHourSchema] | None = None
    pictures_path: str | None = None
    model_config = ConfigDict()

    @field_validator("title", mode="before")
    def title_validator(cls, value):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        value = cleaning_text(value)
        return value

    @field_validator("category", mode="before")
    def category_validator(cls, value):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        value = cleaning_text(value)
        return value

    @field_validator("address", mode="before")
    def address_validator(cls, value):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        if value and value.startswith("Address: "):
            value = value[len("Address: ") :]
        value = cleaning_text(value)
        return value

    @field_validator("phone_number", mode="before")
    def phone_number_validator(cls, value: str):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        if isinstance(value, int):
            value = f"0{value}"
        if value:
            if value.startswith("Phone: "):
                value = value[len("Phone: ") :]
            value = value.replace(" ", "")
            value = value.replace("-", "")
            if value.startswith("+98"):
                value = value.replace("+98", "0")
        value = cleaning_text(value)
        return value

    @field_validator("website", mode="before")
    def website_validator(cls, value):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        if value and value.startswith("/url?q="):
            value = value[len("/url?q=") :]
        value = cleaning_text(value)
        return value

    @field_validator("latitude", mode="before")
    def latitude_validator(cls, value):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        return value

    @field_validator("longitude", mode="before")
    def longitude_validator(cls, value):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        return value

    @field_validator("active_hours", mode="before")
    def active_hours_validator(cls, value: str) -> list[WeekDayHourSchema]:
        if isinstance(value, float) and math.isnan(value):
            value = []
            return value

        week_days = [
            "saturday",
            "sunday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
        ]

        if value.endswith("_**_google_map"):
            result = []
            value = value.replace(AppConfig.GOOGLE_MAP_ACTIVE_HOURS_END_ID, "")
            value = value.replace(", Hours might differ", "")

            if not value:
                return []

            days_and_status = [i.strip().lower() for i in value.split(";")]
            for day_status in days_and_status:
                day, status_of_day = [i.strip() for i in day_status.split(",", 1)]
                for week_day in week_days:
                    if week_day in day.lower().strip():
                        day = week_day
                        break
                if "close" in status_of_day:
                    result.append(
                        WeekDayHourSchema.model_validate(
                            {
                                "day": day,
                                "hours": [],
                                "is_close": True,
                                "is_open": False,
                            }
                        )
                    )
                    continue
                elif "open" in status_of_day:
                    result.append(
                        WeekDayHourSchema.model_validate(
                            {
                                "day": day,
                                "hours": [],
                                "is_close": False,
                                "is_open": True,
                            }
                        )
                    )
                    continue
                else:
                    open_hour = [i.strip() for i in status_of_day.split(",")]
                    open_hour_schemas = []
                    for open_hour_of_day in open_hour:
                        from_hour, to_hour = [
                            i.strip() for i in open_hour_of_day.split("to")
                        ]
                        if "am" in from_hour or "pm" in from_hour:
                            from_hour = cls.convert_12H_AP_PM_TO_24H(from_hour)
                            from_hour = cls.clean_hour(from_hour)
                        else:
                            from_hour = cls.clean_hour(from_hour)

                        if "am" in to_hour or "pm" in to_hour:
                            to_hour = cls.convert_12H_AP_PM_TO_24H(to_hour)
                            to_hour = cls.clean_hour(to_hour)
                        else:
                            to_hour = cls.clean_hour(to_hour)

                        if cls.hour_is_ok(from_hour) and cls.hour_is_ok(to_hour):
                            open_hour_schemas.append(
                                HourSchema.model_validate(
                                    {
                                        "from_hour": from_hour,
                                        "to_hour": to_hour,
                                    }
                                )
                            )
                    result.append(
                        WeekDayHourSchema.model_validate(
                            {
                                "day": day,
                                "hours": open_hour_schemas,
                                "is_close": False,
                                "is_open": False,
                            }
                        )
                    )
            return result

    @field_validator("pictures_path", mode="before")
    def pictures_path_validator(cls, value):
        if isinstance(value, float) and math.isnan(value):
            value = ""
        return value

    @staticmethod
    def hour_is_ok(hour: str):
        try:
            hour_to, hour_from = hour.split(":")
            if hour_to.isdigit() and hour_from.isdigit():
                return True
            return False
        except Exception as e:
            return False

    @staticmethod
    def convert_12H_AP_PM_TO_24H(time_str):
        time_str = time_str.strip()
        if ":" in time_str:
            in_time = datetime.strptime(time_str, "%I:%M %p")
        else:
            in_time = datetime.strptime(time_str, "%I %p")
        out_time = datetime.strftime(in_time, "%H:%M")
        return out_time

    @staticmethod
    def clean_hour(hour_minut):
        if ":" not in hour_minut:
            return f"{hour_minut}:00"

        def abs(a):
            if a < 0:
                return -a
            return a

        hour, minuts = hour_minut.split(":")
        my_list = [
            abs(int(minuts) - 00),
            abs(int(minuts) - 15),
            abs(int(minuts) - 30),
            abs(int(minuts) - 45),
        ]
        min_index = my_list.index(min(my_list))
        return f"{hour}:{["00", "15", "30", "45"][min_index]}"
