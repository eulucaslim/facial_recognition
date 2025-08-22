from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.lib.face_reco import FaceReco

router = APIRouter(tags=["Face Recognition"])
face_reco = FaceReco()

@router.post("/register")
async def register(file: UploadFile = File(...), 
    user_name: str = Form(...),
    cpf: str = Form(...) 
) -> dict:
    response = face_reco.register_user(img_bytes=file.file, user_name=user_name, cpf=cpf)
    if response:
        return JSONResponse(content={"message": "201 CREATED"}, status_code=201)
    else:
        return JSONResponse(content={"message": "400 BAD REQUEST"}, status_code=400)

@router.post("/verify-user")
async def verify_user(file: UploadFile = File(...)):
    response = face_reco.found_user(img_bytes=file.file)
    return JSONResponse(content={"message": response})