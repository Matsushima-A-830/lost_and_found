from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import tempfile
from libs.ai import detect_objects, transcribe_audio

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        img = Image.open(file.file).convert("RGB")
        arr = np.array(img)
        results = detect_objects(arr)
        data = [
            {
                "label": r.label,
                "confidence": r.confidence,
                "bbox": r.bbox,
            }
            for r in results
        ]
        return {"message": "解析成功", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"画像解析失敗: {e}")

@router.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        text = transcribe_audio(tmp_path)
        return {"message": "文字起こし成功", "data": {"text": text}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"音声解析失敗: {e}")
