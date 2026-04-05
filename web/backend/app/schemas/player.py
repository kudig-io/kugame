"""
玩家相关 Pydantic 模型
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class PlayerBase(BaseModel):
    """玩家基础模型"""
    name: str = Field(..., min_length=1, max_length=50)
    sect: str = Field(default="青云宗")


class PlayerCreate(PlayerBase):
    """创建玩家"""
    pass


class PlayerUpdate(BaseModel):
    """更新玩家"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    title: Optional[str] = None


class PlayerStats(BaseModel):
    """玩家统计数据"""
    total_combats: int
    combats_won: int
    win_rate: float
    highest_tower_level: int


class PlayerAttributes(BaseModel):
    """玩家属性"""
    level: int
    experience: int
    exp_to_next_level: int
    cultivation_level: str
    health: int
    max_health: int
    attack: int
    defense: int
    gold: int
    stamina: int
    max_stamina: int


class PlayerResponse(PlayerBase):
    """玩家响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    title: str
    
    # 等级
    level: int
    experience: int
    cultivation_level: str
    
    # 属性
    health: int
    max_health: int
    attack: int
    defense: int
    
    # 资源
    gold: int
    stamina: int
    max_stamina: int
    
    # 进度
    current_chapter: str
    completed_chapters: List[str]
    
    # 统计
    total_combats: int
    combats_won: int
    win_rate: float
    highest_tower_level: int
    
    # 时间
    created_at: datetime
    last_login: Optional[datetime]


class PlayerDetail(PlayerResponse):
    """玩家详情"""
    achievements: List[str]
    inventory: List[Dict[str, Any]]
    equipped_items: Dict[str, Any]
    skills: List[str]


class PlayerListResponse(BaseModel):
    """玩家列表响应"""
    items: List[PlayerResponse]
    total: int
    page: int
    page_size: int


class LevelUpResponse(BaseModel):
    """升级响应"""
    success: bool
    old_level: int
    new_level: int
    rewards: Dict[str, Any]
    message: str


class CultivationInfo(BaseModel):
    """修炼信息"""
    current_level: str
    next_level: Optional[str]
    progress: float
    required_exp: int
