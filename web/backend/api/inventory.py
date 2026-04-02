"""Inventory API Routes"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from pydantic import BaseModel

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


class UseItemRequest(BaseModel):
    item_id: str


class EquipRequest(BaseModel):
    item_id: str
    slot: str = None


# 模拟库存数据
MOCK_INVENTORY = [
    {"id": "health_potion", "name": "生命药水", "type": "consumable", "quantity": 5, "icon": "fa-flask"},
    {"id": "mana_potion", "name": "法力药水", "type": "consumable", "quantity": 3, "icon": "fa-tint"},
    {"id": "iron_sword", "name": "铁剑", "type": "weapon", "quantity": 1, "equipped": True, "icon": "fa-sword"},
    {"id": "leather_armor", "name": "皮甲", "type": "armor", "quantity": 1, "equipped": False, "icon": "fa-shield-alt"},
    {"id": "spirit_stone", "name": "灵石", "type": "currency", "quantity": 1000, "icon": "fa-gem"},
]


@router.get("")
async def get_inventory():
    """获取背包内容"""
    return {
        "status": "success",
        "data": {
            "items": MOCK_INVENTORY,
            "capacity": 50,
            "used": len(MOCK_INVENTORY),
        },
    }


@router.post("/use")
async def use_item(request: UseItemRequest):
    """使用物品"""
    item = next((i for i in MOCK_INVENTORY if i["id"] == request.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    if item["quantity"] <= 0:
        raise HTTPException(status_code=400, detail="物品数量不足")
    
    # 模拟使用效果
    effects = {}
    if item["type"] == "consumable":
        if "health" in item["id"]:
            effects["hp"] = 50
        elif "mana" in item["id"]:
            effects["mp"] = 30
        elif "cultivation" in item["id"]:
            effects["cultivation"] = 100
    
    return {
        "status": "success",
        "data": {
            "item": item,
            "effects": effects,
            "message": f"使用了 {item['name']}",
        },
    }


@router.post("/equip")
async def equip_item(request: EquipRequest):
    """装备物品"""
    item = next((i for i in MOCK_INVENTORY if i["id"] == request.item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="物品不存在")
    
    if item["type"] not in ["weapon", "armor", "accessory"]:
        raise HTTPException(status_code=400, detail="该物品无法装备")
    
    return {
        "status": "success",
        "data": {
            "item": item,
            "equipped": True,
            "message": f"装备了 {item['name']}",
        },
    }


@router.get("/equipment")
async def get_equipment():
    """获取已装备物品"""
    equipped = [i for i in MOCK_INVENTORY if i.get("equipped")]
    return {
        "status": "success",
        "data": equipped,
    }
