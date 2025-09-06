from app.routers import face_reco
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
import os
import uvicorn

app = FastAPI()
app.include_router(face_reco.router)

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

@app.get("/")
def main():
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=4000)