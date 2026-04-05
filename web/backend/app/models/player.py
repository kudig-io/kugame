"""
玩家游戏数据模型
"""
from datetime import datetime
from typing import TYPE_CHECKING, Dict, List, Optional, Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Player(Base):
    """玩家游戏数据"""
    __tablename__ = "players"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    
    # 基本信息
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    sect: Mapped[str] = mapped_column(String(20), default="青云宗")
    title: Mapped[str] = mapped_column(String(50), default="初入仙门")
    
    # 等级系统
    level: Mapped[int] = mapped_column(Integer, default=1)
    experience: Mapped[int] = mapped_column(Integer, default=0)
    cultivation_level: Mapped[str] = mapped_column(String(20), default="凡人")
    
    # 战斗属性
    health: Mapped[int] = mapped_column(Integer, default=100)
    max_health: Mapped[int] = mapped_column(Integer, default=100)
    attack: Mapped[int] = mapped_column(Integer, default=10)
    defense: Mapped[int] = mapped_column(Integer, default=5)
    
    # 资源
    gold: Mapped[int] = mapped_column(Integer, default=0)
    stamina: Mapped[int] = mapped_column(Integer, default=100)
    max_stamina: Mapped[int] = mapped_column(Integer, default=100)
    
    # 游戏进度
    current_chapter: Mapped[str] = mapped_column(String(50), default="序章")
    completed_chapters: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    # 统计数据
    total_combats: Mapped[int] = mapped_column(Integer, default=0)
    combats_won: Mapped[int] = mapped_column(Integer, default=0)
    highest_tower_level: Mapped[int] = mapped_column(Integer, default=0)
    
    # 复杂数据结构（JSON）
    achievements: Mapped[List[str]] = mapped_column(JSON, default=list)
    inventory: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, default=list)
    equipped_items: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    skills: Mapped[List[str]] = mapped_column(JSON, default=list)
    
    # 系统数据
    checkin_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    quest_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    pet_data: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    
    # 时间戳
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # 关系
    user: Mapped["User"] = relationship("User", back_populates="player")
    
    @property
    def win_rate(self) -> float:
        """胜率"""
        if self.total_combats == 0:
            return 0.0
        return self.combats_won / self.total_combats
    
    @property
    def exp_to_next_level(self) -> int:
        """升级所需经验"""
        return self.level * 100
    
    def __repr__(self) -> str:
        return f"<Player {self.name} Lv.{self.level}>"
