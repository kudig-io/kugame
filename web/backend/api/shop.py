"""Shop API Routes（封装 kugame 核心商店系统）

商店货币使用玩家经验值（与游戏核心一致）。
"""
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from kugame.equipment import Equipment

from .deps import get_engine, get_player, get_shop_items, persist

router = APIRouter(prefix="/api/shop", tags=["shop"])


class BuyRequest(BaseModel):
    item_id: str


class SellRequest(BaseModel):
    item_id: str


def _shop_item_view(equipment: Equipment, price: int) -> dict:
    data = equipment.to_dict()
    data["price"] = price
    return data


@router.get("/items")
async def get_items():
    """获取商店商品列表（按玩家等级刷新）"""
    engine = get_engine()
    items = get_shop_items()
    data = [
        _shop_item_view(item, engine.equipment_manager.calculate_buy_price(item))
        for item in items
    ]
    return {
        "status": "success",
        "data": data,
    }


@router.post("/buy")
async def buy_item(request: BuyRequest):
    """购买装备（消耗经验值）"""
    engine = get_engine()
    equipment = next(
        (e for e in get_shop_items() if e.id == request.item_id), None
    )
    if not equipment:
        raise HTTPException(status_code=404, detail="商品不存在")

    result = engine.buy_equipment(equipment)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "购买失败"))

    persist()
    return {
        "status": "success",
        "data": {
            "message": result["message"],
            "equipment": result["equipment"].to_dict(),
            "remaining_exp": result.get("remaining_exp"),
        },
    }


@router.post("/sell")
async def sell_item(request: SellRequest):
    """出售背包装备（获得经验值）"""
    engine = get_engine()
    player = get_player()
    equipment = next(
        (e for e in player.inventory if e.id == request.item_id), None
    )
    if not equipment:
        raise HTTPException(status_code=404, detail="该装备不在背包中")

    result = engine.sell_equipment(equipment)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "出售失败"))

    persist()
    return {
        "status": "success",
        "data": {
            "message": result["message"],
            "gained_exp": result.get("gained_exp"),
            "total_exp": result.get("total_exp"),
        },
    }
