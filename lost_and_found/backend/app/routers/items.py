# /api/items ルーター
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from ..schemas import ItemCreate, ItemRead, ItemUpdate, ErrorResponse
from ..deps import get_db, get_current_user
from ..models import ITEMS
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=ItemRead, responses={400: {"model": ErrorResponse}})
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # 管理番号自動生成例
    management_number = f"MNG-{int(datetime.utcnow().timestamp())}"
    db_item = ITEMS(
        management_number=management_number,
        found_datetime=item.found_datetime,
        found_place=item.found_place,
        category_l=item.category_l,
        category_m=item.category_m,
        category_s=item.category_s,
        color=item.color,
        features=item.features,
        status=item.status,
        image_path=item.image_path,
        registered_by_user_id=user.id,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.get("/", response_model=list[ItemRead])
async def search_items(
    db: AsyncSession = Depends(get_db),
    status: str = Query(None),
    category_l: str = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    q: str = Query(None),
):
    stmt = select(ITEMS)
    filters = []
    if status:
        filters.append(ITEMS.status == status)
    if category_l:
        filters.append(ITEMS.category_l == category_l)
    if start_date:
        filters.append(ITEMS.found_datetime >= start_date)
    if end_date:
        filters.append(ITEMS.found_datetime <= end_date)
    if q:
        filters.append(or_(
            ITEMS.found_place.ilike(f"%{q}%"),
            ITEMS.features.ilike(f"%{q}%"),
        ))
    if filters:
        stmt = stmt.where(and_(*filters))
    result = await db.execute(stmt)
    items = result.scalars().all()
    return items

@router.get("/{id}", response_model=ItemRead)
async def get_item(id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(ITEMS, id)
    if not item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    return item

@router.put("/{id}", response_model=ItemRead)
async def update_item(
    id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    db_item = await db.get(ITEMS, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    for field, value in item.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.put("/{id}/status", response_model=ItemRead)
async def change_status(
    id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    db_item = await db.get(ITEMS, id)
    if not db_item:
        raise HTTPException(status_code=404, detail="アイテムが見つかりません")
    db_item.status = status
    await db.commit()
    await db.refresh(db_item)
    return db_item
