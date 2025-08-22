from app.routers import face_reco, sheets
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(face_reco.router)
app.include_router(sheets.router)

@app.get("/")
def main():
    return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=4000)