from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional
from PIL import Image
import io
from ultralytics import YOLO
from fastapi.responses import HTMLResponse


class BoundingBox(BaseModel):
    x_min: int = Field(..., description="Левая координата", ge=0)
    y_min: int = Field(..., description="Верхняя координата", ge=0)
    x_max: int = Field(..., description="Правая координата", ge=0)
    y_max: int = Field(..., description="Нижняя координата", ge=0)

class Detection(BaseModel):
    bbox: BoundingBox = Field(..., description="Результат детекции")

class DetectionResponse(BaseModel):
    detections: List[Detection] = Field(..., description="Список найденных логотипов")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Описание ошибки")
    detail: Optional[str] = Field(None, description="Дополнительная информация")

app = FastAPI(title="T-Bank Logo Detector API")

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
        <body>
            <h2>Upload T-Bank Logo Image</h2>
            <form action="/detect" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
            </form>
        </body>
    </html>
    """


MODEL_PATH = "weights/best.pt"
model = YOLO(MODEL_PATH)


@app.post("/detect", response_model=DetectionResponse, responses={400: {"model": ErrorResponse}})
async def detect_logo(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        results = model(image)

        detections = []
        for r in results:  
            for box in r.boxes.xyxy.cpu().numpy():  
                x_min, y_min, x_max, y_max = map(int, box)
                detections.append(Detection(bbox=BoundingBox(
                    x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max
                )))

        return DetectionResponse(detections=detections)

    except Exception as e:
        return ErrorResponse(error="Failed to process image", detail=str(e))
    

