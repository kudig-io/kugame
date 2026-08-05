"""Inventory API Routes（封装 kugame 核心装备系统）"""
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from kugame.equipment import Equipment, EquipmentType

from .deps import get_engine, get_player, persist

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


class EquipRequest(BaseModel):
    item_id: str


class UnequipRequest(BaseModel):
    slot: str  # weapon / armor / accessory


class UpgradeRequest(BaseModel):
    item_id: str


def _find_in_inventory(equipment_id: str) -> Optional[Equipment]:
    player = get_player()
    return next((e for e in player.inventory if e.id == equipment_id), None)


@router.get("")
async def get_inventory():
    """获取背包内容（玩家装备背包）"""
    player = get_player()
    items = [e.to_dict() for e in player.inventory]
    return {
        "status": "success",
        "data": {
            "items": items,
            "used": len(items),
        },
    }


@router.get("/equipment")
async def get_equipment():
    """获取已装备物品与套装加成"""
    player = get_player()
    equipped = {
        "weapon": player.equipped_weapon.to_dict() if player.equipped_weapon else None,
        "armor": player.equipped_armor.to_dict() if player.equipped_armor else None,
        "accessory": player.equipped_accessory.to_dict() if player.equipped_accessory else None,
    }
    set_info = player.set_bonuses
    return {
        "status": "success",
        "data": {
            "equipped": equipped,
            "active_sets": set_info.get("active_sets", []),
            "set_bonuses": set_info.get("bonuses", {}),
        },
    }


@router.post("/equip")
async def equip_item(request: EquipRequest):
    """装备物品"""
    engine = get_engine()
    equipment = _find_in_inventory(request.item_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="物品不存在或不在背包中")

    result = engine.equip_item(equipment)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "装备失败"))

    persist()
    return {
        "status": "success",
        "data": {
            "message": result["message"],
            "equipment": result["equipment"].to_dict(),
        },
    }


@router.post("/unequip")
async def unequip_item(request: UnequipRequest):
    """卸下装备"""
    engine = get_engine()
    try:
        equipment_type = EquipmentType(request.slot)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的装备槽位: {request.slot}")

    result = engine.unequip_item(equipment_type)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "卸下失败"))

    persist()
    return {
        "status": "success",
        "data": {
            "message": result["message"],
            "equipment": result["equipment"].to_dict(),
        },
    }


@router.post("/upgrade")
async def upgrade_item(request: UpgradeRequest):
    """强化装备"""
    engine = get_engine()
    player = get_player()
    equipment = _find_in_inventory(request.item_id)
    if not equipment:
        # 也可能已装备
        equipment = next(
            (e for e in (player.equipped_weapon, player.equipped_armor, player.equipped_accessory)
             if e and e.id == request.item_id),
            None,
        )
    if not equipment:
        raise HTTPException(status_code=404, detail="装备不存在")

    result = engine.upgrade_equipment(equipment)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message", "强化失败"))

    persist()
    return {
        "status": "success",
        "data": {
            "message": result["message"],
            "new_level": result.get("new_level"),
            "remaining_exp": result.get("remaining_exp"),
        },
    }
