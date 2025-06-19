from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import get_session
from app.models import ITEMS
from reportlab.pdfgen import canvas
import tempfile
from datetime import datetime

router = APIRouter()

@router.post("/")
async def create_police_report(
    filters: dict = Body(...),
    db: AsyncSession = Depends(get_session),
):
    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    if not start_date or not end_date:
        raise HTTPException(status_code=400, detail="日付範囲が必要です")
    stmt = select(ITEMS).where(
        ITEMS.found_datetime >= start_date,
        ITEMS.found_datetime <= end_date,
    )
    result = await db.execute(stmt)
    items = result.scalars().all()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        c = canvas.Canvas(tmp.name)
        c.drawString(100, 800, f"警察届出書: {start_date} ~ {end_date}")
        y = 780
        for item in items:
            c.drawString(100, y, f"管理番号: {item.management_number} / 場所: {item.found_place}")
            y -= 20
        c.save()
        pdf_path = tmp.name
    return FileResponse(pdf_path, filename="police_report.pdf", media_type="application/pdf")
