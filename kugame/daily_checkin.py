"""每日签到系统

提供每日签到奖励和连续签到奖励功能。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random


@dataclass
class CheckinReward:
    """签到奖励数据类
    
    Attributes:
        day: 签到天数
        experience: 经验奖励
        stamina: 体力奖励
        equipment_quality: 装备品质（可选）
        special_reward: 特殊奖励描述
    """
    day: int
    experience: int
    stamina: int
    equipment_quality: Optional[int] = None
    special_reward: Optional[str] = None


# 连续签到奖励配置
DAILY_REWARDS = [
    CheckinReward(day=1, experience=100, stamina=20),
    CheckinReward(day=2, experience=150, stamina=20),
    CheckinReward(day=3, experience=200, stamina=30),
    CheckinReward(day=4, experience=250, stamina=30),
    CheckinReward(day=5, experience=300, stamina=40, equipment_quality=2),
    CheckinReward(day=6, experience=400, stamina=40),
    CheckinReward(day=7, experience=500, stamina=50, equipment_quality=3, special_reward="周末大礼包"),
]

# 周循环奖励（第8天开始循环）
WEEKLY_BONUS = {
    7: {"title": "周签到王者", "bonus_exp": 1000},
    14: {"title": "半月达人", "bonus_exp": 2500},
    30: {"title": "月度签到大师", "bonus_exp": 5000, "equipment_quality": 4},
}


class DailyCheckin:
    """每日签到管理器
    
    管理玩家的每日签到状态和奖励发放。
    
    Attributes:
        last_checkin_date: 上次签到日期
        consecutive_days: 连续签到天数
        total_checkins: 总签到次数
        monthly_checkins: 本月签到次数
    """
    
    def __init__(self):
        self.last_checkin_date: Optional[str] = None
        self.consecutive_days: int = 0
        self.total_checkins: int = 0
        self.monthly_checkins: int = 0
        self.last_reset_month: int = datetime.now().month
    
    def can_checkin(self) -> bool:
        """检查今天是否可以签到
        
        Returns:
            bool: 可以签到返回True
        """
        if not self.last_checkin_date:
            return True
        
        try:
            last_date = datetime.fromisoformat(self.last_checkin_date).date()
            today = datetime.now().date()
            
            # 检查是否是同一天
            return last_date < today
        except (ValueError, TypeError):
            return True
    
    def get_checkin_status(self) -> Dict[str, Any]:
        """获取签到状态
        
        Returns:
            Dict[str, Any]: 签到状态信息
        """
        today = datetime.now()
        
        # 检查是否需要重置月度签到
        if today.month != self.last_reset_month:
            self.monthly_checkins = 0
            self.last_reset_month = today.month
        
        can_checkin = self.can_checkin()
        
        # 计算下次签到奖励
        next_day = self.consecutive_days + 1
        reward_index = min(next_day - 1, len(DAILY_REWARDS) - 1)
        next_reward = DAILY_REWARDS[reward_index]
        
        # 计算距离上次签到过了几天
        days_since_last = None
        if self.last_checkin_date:
            try:
                last_date = datetime.fromisoformat(self.last_checkin_date).date()
                days_since_last = (today.date() - last_date).days
            except (ValueError, TypeError):
                pass
        
        return {
            "can_checkin": can_checkin,
            "consecutive_days": self.consecutive_days,
            "total_checkins": self.total_checkins,
            "monthly_checkins": self.monthly_checkins,
            "last_checkin": self.last_checkin_date,
            "days_since_last": days_since_last,
            "next_reward": {
                "day": next_day,
                "experience": next_reward.experience,
                "stamina": next_reward.stamina,
                "has_equipment": next_reward.equipment_quality is not None,
            },
            "weekly_progress": self.consecutive_days % 7,
        }
    
    def checkin(self) -> Dict[str, Any]:
        """执行签到
        
        Returns:
            Dict[str, Any]: 签到结果和奖励
        """
        if not self.can_checkin():
            return {
                "success": False,
                "message": "今天已经签到过了，明天再来吧！"
            }
        
        today = datetime.now()
        
        # 检查是否需要重置月度签到
        if today.month != self.last_reset_month:
            self.monthly_checkins = 0
            self.last_reset_month = today.month
        
        # 更新连续签到天数
        if self.last_checkin_date:
            try:
                last_date = datetime.fromisoformat(self.last_checkin_date).date()
                if (today.date() - last_date).days == 1:
                    # 连续签到
                    self.consecutive_days += 1
                else:
                    # 断签，重置
                    self.consecutive_days = 1
            except (ValueError, TypeError):
                self.consecutive_days = 1
        else:
            self.consecutive_days = 1
        
        # 更新签到记录
        self.last_checkin_date = today.isoformat()
        self.total_checkins += 1
        self.monthly_checkins += 1
        
        # 获取今日奖励
        reward_index = min(self.consecutive_days - 1, len(DAILY_REWARDS) - 1)
        daily_reward = DAILY_REWARDS[reward_index]
        
        # 构建奖励结果
        rewards = {
            "experience": daily_reward.experience,
            "stamina": daily_reward.stamina,
        }
        
        result = {
            "success": True,
            "message": f"签到成功！连续签到 {self.consecutive_days} 天！",
            "consecutive_days": self.consecutive_days,
            "total_checkins": self.total_checkins,
            "rewards": rewards,
        }
        
        # 添加装备奖励
        if daily_reward.equipment_quality:
            rewards["equipment_quality"] = daily_reward.equipment_quality
            result["message"] += f"\n额外获得 {daily_reward.special_reward or '装备奖励'}！"
        
        # 检查周/月额外奖励
        if self.consecutive_days in WEEKLY_BONUS:
            bonus = WEEKLY_BONUS[self.consecutive_days]
            rewards["bonus_experience"] = bonus["bonus_exp"]
            if "equipment_quality" in bonus:
                rewards["bonus_equipment_quality"] = bonus["equipment_quality"]
            result["message"] += f"\n🎉 达成 {bonus['title']}！额外获得 {bonus['bonus_exp']} 经验！"
        
        return result
    
    def get_monthly_reward_status(self) -> Dict[str, Any]:
        """获取月度奖励状态
        
        Returns:
            Dict[str, Any]: 月度奖励信息
        """
        today = datetime.now()
        
        # 计算本月总天数
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        
        days_in_month = (next_month - today.replace(day=1)).days
        
        return {
            "current_month": today.month,
            "monthly_checkins": self.monthly_checkins,
            "days_in_month": days_in_month,
            "progress_percentage": round(self.monthly_checkins / days_in_month * 100, 1),
            "milestones": [
                {"days": 7, "reward": "500经验", "completed": self.monthly_checkins >= 7},
                {"days": 14, "reward": "1000经验 + 精良装备", "completed": self.monthly_checkins >= 14},
                {"days": 21, "reward": "2000经验 + 稀有装备", "completed": self.monthly_checkins >= 21},
                {"days": 28, "reward": "5000经验 + 史诗装备", "completed": self.monthly_checkins >= 28},
            ]
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典
        
        Returns:
            Dict[str, Any]: 签到数据字典
        """
        return {
            "last_checkin_date": self.last_checkin_date,
            "consecutive_days": self.consecutive_days,
            "total_checkins": self.total_checkins,
            "monthly_checkins": self.monthly_checkins,
            "last_reset_month": self.last_reset_month,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailyCheckin":
        """从字典创建签到管理器
        
        Args:
            data: 签到数据字典
            
        Returns:
            DailyCheckin: 签到管理器对象
        """
        checkin = cls()
        checkin.last_checkin_date = data.get("last_checkin_date")
        checkin.consecutive_days = data.get("consecutive_days", 0)
        checkin.total_checkins = data.get("total_checkins", 0)
        checkin.monthly_checkins = data.get("monthly_checkins", 0)
        checkin.last_reset_month = data.get("last_reset_month", datetime.now().month)
        return checkin
