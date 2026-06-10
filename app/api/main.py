from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2
from app.services.detection_service import detect_plate

app = FastAPI()


@app.get("/")
def home():
    return {"message": "VNPR API Running"}


@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    contents = await file.read()

    np_arr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    result = detect_plate(frame)

    return result
