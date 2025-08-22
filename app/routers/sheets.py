from app.lib.sheets import Sheets
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse, Response
from typing import Dict

router = APIRouter(tags=["Sheets"])

@router.post("/export-json")
async def export_json(template_file: UploadFile, writer_file: UploadFile) -> Dict:
    try:
        sheets = Sheets(template_file=template_file, writer_file=writer_file)
        sheets_data = await sheets.generate_json() 
        return JSONResponse({"data": sheets_data})
    except Exception as e:
        return JSONResponse({"msg": str(e)}, status_code=500)