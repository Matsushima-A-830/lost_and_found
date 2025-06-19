from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.db import get_session
from app.models import ITEMS

router = APIRouter()

@router.get("/expiring")
async def get_expiring_items(db: AsyncSession = Depends(get_session)):
    now = datetime.utcnow()
    limit = now + timedelta(days=3)
    # 仮に features に保管期限日付が入っていると仮定
    stmt = select(ITEMS).where(
        ITEMS.status == "保管中",
        ITEMS.features != None,
    )
    result = await db.execute(stmt)
    items = []
    for item in result.scalars():
        try:
            # features に "expire:YYYY-MM-DD" 形式で格納されていると仮定
            if "expire:" in (item.features or ""):
                expire_str = item.features.split("expire:")[1].split()[0]
                expire_date = datetime.strptime(expire_str, "%Y-%m-%d")
                if now <= expire_date <= limit:
                    items.append({
                        "id": item.id,
                        "management_number": item.management_number,
                        "expire_date": expire_str,
                    })
        except Exception:
            continue
    return {"message": "期限切れ間近アイテム", "data": items}
