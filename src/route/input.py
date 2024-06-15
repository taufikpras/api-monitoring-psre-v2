from fastapi import APIRouter, File, UploadFile
# import src.util.scheduler as sch
# from src.model.input import Input
# import src.core.input_core as core
import src.util.file_handler as file_handler
import os
import zipfile
# from pathlib import Path
import shutil
import aiofiles
from src.parameters import TEMP
import json
import logging
import src.core.files as file_core 

str_name = "input"
router = APIRouter(prefix="/api",tags=[str_name],)
logger = logging.getLogger("monitoring_psre")

# @router.post("/insert")
# async def insert_from_file(input:Input):
#     ls = core.add_new(input)
#     return ls

# @router.post("/insert_all_file")
# async def insert_all_file():
#     ls = core.add_all_file()
#     return ls

@router.post("/list_file")
async def list_file():
    ls = file_core.get_all()

    return ls

@router.post("/upload")
async def create_upload_file(file: UploadFile):
    # contents = await file.read()
    
    if not os.path.exists(TEMP):
        os.makedirs(TEMP)

    tmp_path = os.path.join(TEMP, file.filename)

    async with aiofiles.open(tmp_path, 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    files = file_core.insert_from_file(tmp_path)
    

    res = {}

    res["files"] = files

    return res