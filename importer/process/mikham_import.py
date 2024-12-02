import os
import random
import shutil
import asyncio
from pathlib import Path
import pandas as pd
from config import RuntimeResource, AppConfig
from data import BrowserTabBo
from data.dao import RedisDao
from data.bo import ImportToSiteBo
import traceback


class MikhamImporterProcess:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.resource = RuntimeResource()
        self.broser_tab_bo = BrowserTabBo(start_url)
        self.redis_dao = RedisDao()
        self.import_to_site_bo = ImportToSiteBo()

    async def start(self):
        while True:
            print("importer ->check for break")
            need_break = self._check_for_break()
            if need_break:
                break

            print("importer ->check for sheet to import")
            try:
                sheet_name = self._get_random_not_imported_excel()
            except Exception as e:
                sheet_name = None
            if not sheet_name:
                print(f"importer ->no sheet found. wait for {2.5} minuts")
                await asyncio.sleep(2.5 * 60)
                continue

            print(f"importer ->start import sheet {sheet_name}")

            await self.resource.initialize_browsers()
            await self.resource.initialize_tabs()

            dict_data = self._get_sheet_data(sheet_name)
            province, city, category, listing_type = self._get_data_from_sheet_name(
                sheet_name
            )

            try:
                await self.broser_tab_bo.goto_mikham()
            except Exception as e:
                print("error on goto mikham ... ")
                print(f"importer ->Error: {e}")
                traceback.print_exc()
                await self.resource.free()
                continue
            
            try:
                await self.import_to_site_bo.import_data(
                    dict_data, province, city, category, listing_type
                )
            except Exception as e:
                print(f"importer ->Error: {e}")
                traceback.print_exc()
            else:
                self._move_sheet_to_imported(sheet_name)
            finally:
                await self.resource.free()
                
                
            await asyncio.sleep(5)

    @staticmethod
    def _move_sheet_to_imported(file_name):
        source_path = f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{AppConfig.NOT_IMPORTED_SHEETS_DIRECTORY}"
        dest_path = f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{AppConfig.IMPORTED_SHEETS_DIRECTORY}"
        print(f"moving file {file_name} from {source_path} to {dest_path}\n\n")
        Path(dest_path).mkdir(parents=True, exist_ok=True)
        shutil.move(f"{source_path}/{file_name}", f"{dest_path}/{file_name}")

    @staticmethod
    def _get_data_from_sheet_name(sheet_name: str):
        category, search_query_type, province, scraper = sheet_name[
            : -len(".xlsx")
        ].split(AppConfig.LISTING_NAME_ITEMS_SEPARATOR)
        listing_type, verb, city = search_query_type.split(
            AppConfig.SEARCH_QUERY_SEPARATOR
        )
        return province, city, category, listing_type

    @staticmethod
    def _get_sheet_data(sheet_name):
        sheet_path = f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{AppConfig.NOT_IMPORTED_SHEETS_DIRECTORY}/{sheet_name}"
        data = pd.read_excel(sheet_path, sheet_name="Sheet1")
        dict_data = data.to_dict(orient="records")
        return dict_data

    @staticmethod
    def _get_random_not_imported_excel():
        dource_dir = f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{AppConfig.NOT_IMPORTED_SHEETS_DIRECTORY}"
        temp = [
            file
            for file in os.listdir(dource_dir)
            if os.path.isfile(os.path.join(dource_dir, file))
        ]
        if not temp:
            return None
        return random.choice(temp)

    def _check_for_break(self):
        break_status = self.redis_dao.get_importer_break()
        if break_status:
            self.redis_dao.set_importer_break(False)
            return True
        return False

    def _move_not_imported_excel_to_imported(file_name):
        pass
