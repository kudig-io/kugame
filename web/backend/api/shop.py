"""Shop API Routes"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel

router = APIRouter(prefix="/api/shop", tags=["shop"])


class BuyRequest(BaseModel):
    item_id: str
    quantity: int = 1


class SellRequest(BaseModel):
    item_id: str
    quantity: int = 1


# 商店商品
SHOP_ITEMS = [
    {
        "id": "health_potion",
        "name": "生命药水",
        "type": "consumable",
        "price": 50,
        "description": "恢复 50 点生命值",
        "effect": {"hp": 50},
    },
    {
        "id": "mana_potion",
        "name": "法力药水",
        "type": "consumable",
        "price": 30,
        "description": "恢复 30 点法力值",
        "effect": {"mp": 30},
    },
    {
        "id": "cultivation_pill",
        "name": "修炼丹",
        "type": "consumable",
        "price": 100,
        "description": "增加 100 点修为",
        "effect": {"cultivation": 100},
    },
    {
        "id": "iron_sword",
        "name": "铁剑",
        "type": "weapon",
        "price": 200,
        "description": "攻击力 +10",
        "stats": {"attack": 10},
    },
    {
        "id": "leather_armor",
        "name": "皮甲",
        "type": "armor",
        "price": 150,
        "description": "防御力 +5",
        "stats": {"defense": 5},
    },
    {
        "id": "spirit_stone",
        "name": "灵石",
        "type": "currency",
        "price": 10,
        "description": "修仙界的通用货币",
    },
]


@router.get("/items")
async def get_items(category: str = None):
    """获取商店商品列表"""
    items = SHOP_ITEMS
    if category:
        items = [item for item in items if item["type"] == category]
    
    return {
        "status": "success",
        "data": items,
    }


@router.post("/buy")
async def buy_item(request: BuyRequest):
    """购买物品"""
    item = next((i for i in SHOP_ITEMS if i["id"] == request.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    total_price = item["price"] * request.quantity
    
    return {
        "status": "success",
        "data": {
            "item": item,
            "quantity": request.quantity,
            "total_price": total_price,
            "message": f"成功购买 {request.quantity} 个 {item['name']}",
        },
    }


@router.post("/sell")
async def sell_item(request: SellRequest):
    """出售物品"""
    # 模拟出售逻辑，价格为购买价的 50%
    sell_price = 25 * request.quantity  # 假设基础价格
    
    return {
        "status": "success",
        "data": {
            "item_id": request.item_id,
            "quantity": request.quantity,
            "total_price": sell_price,
            "message": f"成功出售 {request.quantity} 个物品",
        },
    }


@router.get("/categories")
async def get_categories():
    """获取商品分类"""
    categories = list(set(item["type"] for item in SHOP_ITEMS))
    return {
        "status": "success",
        "data": categories,
    }
