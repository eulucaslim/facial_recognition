from app.config.settings import logging as logger
from fastapi import UploadFile
from typing import List
import pandas as pd
import os


class Sheets(object):

    def __init__(self, template_file: UploadFile, writer_file: UploadFile):
        self.template_file = template_file
        self.writer_file = writer_file
        self.path_data = "./data"

    async def generate_json(self) -> dict:
        try:
            if not os.path.exists(self.path_data):
                os.makedirs(self.path_data)
            # Generate first the template
            template_file_path = os.path.join(
                self.path_data, 
                self.template_file.filename
            )

            await self.generate_temp_file(self.template_file, template_file_path)
            template_data = self.read_sheet(template_file_path)
            os.remove(template_file_path)
            return template_data

        except Exception as error:
            logger.error(f"Error: {str(error)}")
            raise (error)

    async def generate_temp_file(self, file: UploadFile, file_path: str) -> bool | None:
        try:
            logger.info(f"Saving this temp file -> {file.filename}")
            with open(file_path, "wb") as temp_file:
                content = await file.read()
                temp_file.write(content)
            return True

        except Exception as error:
            logger.error(f"Error: {str(error)}")
            raise (error)
        
    def read_sheet(self, local_file_path: str) -> List[dict]:
        sheets = list()
        try:
            logger.info(f"Reading a excel file in this path-> {local_file_path}")
            workbook = pd.read_excel(local_file_path, engine="calamine", sheet_name=None)
            for sheet_name, df in workbook.items():
                sheet_data = dict()
                df_dict = df.to_dict(orient='dict')
                sheet_data[sheet_name] = df_dict
                sheets.append(sheet_data)
            logger.info(f"Finally to Read excel!")
            return sheets

        except Exception as error:
            os.remove(local_file_path)
            logger.error(f"Error: {str(error)}")
            raise (error)