"""排行榜系统

提供玩家排名、成就展示等功能。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import os


@dataclass
class PlayerRanking:
    """玩家排名数据
    
    Attributes:
        player_id: 玩家ID
        player_name: 玩家名称
        level: 等级
        total_exp: 总经验
        achievements_count: 成就数量
        tower_level: 最高挑战塔层
        total_combats: 总战斗次数
        combats_won: 胜利次数
        play_time: 游戏时长（分钟）
        last_updated: 最后更新时间
    """
    player_id: str
    player_name: str
    level: int = 1
    total_exp: int = 0
    achievements_count: int = 0
    tower_level: int = 0
    total_combats: int = 0
    combats_won: int = 0
    play_time: int = 0
    last_updated: Optional[str] = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()
    
    @property
    def combat_win_rate(self) -> float:
        """战斗胜率"""
        if self.total_combats == 0:
            return 0.0
        return self.combats_won / self.total_combats
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "level": self.level,
            "total_exp": self.total_exp,
            "achievements_count": self.achievements_count,
            "tower_level": self.tower_level,
            "total_combats": self.total_combats,
            "combats_won": self.combats_won,
            "play_time": self.play_time,
            "last_updated": self.last_updated,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerRanking":
        """从字典创建"""
        return cls(
            player_id=data["player_id"],
            player_name=data["player_name"],
            level=data.get("level", 1),
            total_exp=data.get("total_exp", 0),
            achievements_count=data.get("achievements_count", 0),
            tower_level=data.get("tower_level", 0),
            total_combats=data.get("total_combats", 0),
            combats_won=data.get("combats_won", 0),
            play_time=data.get("play_time", 0),
            last_updated=data.get("last_updated"),
        )


class Leaderboard:
    """排行榜管理器"""
    
    LEADERBOARD_FILE = "leaderboard.json"
    
    def __init__(self):
        self.rankings: List[PlayerRanking] = []
        self._load_leaderboard()
    
    def _get_file_path(self) -> str:
        """获取排行榜文件路径"""
        return os.path.join(os.path.dirname(__file__), self.LEADERBOARD_FILE)
    
    def _load_leaderboard(self):
        """加载排行榜数据"""
        file_path = self._get_file_path()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.rankings = [PlayerRanking.from_dict(r) for r in data.get("rankings", [])]
            except Exception:
                self.rankings = []
    
    def _save_leaderboard(self):
        """保存排行榜数据"""
        file_path = self._get_file_path()
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "rankings": [r.to_dict() for r in self.rankings],
                    "last_updated": datetime.now().isoformat(),
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存排行榜失败: {e}")
    
    def update_player_ranking(self, player_data: Dict[str, Any]) -> int:
        """更新玩家排名数据
        
        Args:
            player_data: 玩家数据字典
            
        Returns:
            int: 当前排名（从1开始）
        """
        player_id = player_data.get("player_id")
        
        # 查找现有记录
        existing = None
        for r in self.rankings:
            if r.player_id == player_id:
                existing = r
                break
        
        if existing:
            # 更新现有记录
            existing.level = player_data.get("level", existing.level)
            existing.total_exp = player_data.get("total_exp", existing.total_exp)
            existing.achievements_count = player_data.get("achievements_count", existing.achievements_count)
            existing.tower_level = player_data.get("tower_level", existing.tower_level)
            existing.total_combats = player_data.get("total_combats", existing.total_combats)
            existing.combats_won = player_data.get("combats_won", existing.combats_won)
            existing.play_time = player_data.get("play_time", existing.play_time)
            existing.last_updated = datetime.now().isoformat()
        else:
            # 创建新记录
            new_ranking = PlayerRanking(
                player_id=player_id,
                player_name=player_data.get("player_name", "未知"),
                level=player_data.get("level", 1),
                total_exp=player_data.get("total_exp", 0),
                achievements_count=player_data.get("achievements_count", 0),
                tower_level=player_data.get("tower_level", 0),
                total_combats=player_data.get("total_combats", 0),
                combats_won=player_data.get("combats_won", 0),
                play_time=player_data.get("play_time", 0),
            )
            self.rankings.append(new_ranking)
        
        # 按经验值排序
        self.rankings.sort(key=lambda x: x.total_exp, reverse=True)
        
        # 保存
        self._save_leaderboard()
        
        # 返回排名
        for i, r in enumerate(self.rankings, 1):
            if r.player_id == player_id:
                return i
        return len(self.rankings)
    
    def get_top_players(self, category: str = "total_exp", limit: int = 10) -> List[Dict[str, Any]]:
        """获取排行榜前N名
        
        Args:
            category: 排序类别 (total_exp, level, achievements, tower, combat_wins)
            limit: 返回数量
            
        Returns:
            List[Dict]: 排名列表
        """
        sort_keys = {
            "total_exp": lambda x: x.total_exp,
            "level": lambda x: (x.level, x.total_exp),
            "achievements": lambda x: x.achievements_count,
            "tower": lambda x: x.tower_level,
            "combat_wins": lambda x: x.combats_won,
            "win_rate": lambda x: x.combat_win_rate,
        }
        
        key_func = sort_keys.get(category, sort_keys["total_exp"])
        sorted_rankings = sorted(self.rankings, key=key_func, reverse=True)
        
        return [
            {
                "rank": i,
                "player_name": r.player_name,
                "level": r.level,
                "total_exp": r.total_exp,
                "achievements_count": r.achievements_count,
                "tower_level": r.tower_level,
                "combats_won": r.combats_won,
                "combat_win_rate": round(r.combat_win_rate * 100, 1),
            }
            for i, r in enumerate(sorted_rankings[:limit], 1)
        ]
    
    def get_player_rank(self, player_id: str, category: str = "total_exp") -> Optional[Dict[str, Any]]:
        """获取玩家排名详情
        
        Args:
            player_id: 玩家ID
            category: 排序类别
            
        Returns:
            Optional[Dict]: 排名详情
        """
        top_players = self.get_top_players(category, limit=100)
        
        for player in top_players:
            # 这里简化处理，实际应该通过ID匹配
            pass
        
        # 查找玩家数据
        player_ranking = None
        for r in self.rankings:
            if r.player_id == player_id:
                player_ranking = r
                break
        
        if not player_ranking:
            return None
        
        # 计算排名
        sort_keys = {
            "total_exp": lambda x: x.total_exp,
            "level": lambda x: (x.level, x.total_exp),
            "achievements": lambda x: x.achievements_count,
            "tower": lambda x: x.tower_level,
            "combat_wins": lambda x: x.combats_won,
        }
        
        key_func = sort_keys.get(category, sort_keys["total_exp"])
        sorted_rankings = sorted(self.rankings, key=key_func, reverse=True)
        
        for i, r in enumerate(sorted_rankings, 1):
            if r.player_id == player_id:
                return {
                    "rank": i,
                    "total_players": len(self.rankings),
                    "player_name": r.player_name,
                    "level": r.level,
                    "total_exp": r.total_exp,
                    "achievements_count": r.achievements_count,
                    "tower_level": r.tower_level,
                    "combats_won": r.combats_won,
                    "total_combats": r.total_combats,
                    "combat_win_rate": round(r.combat_win_rate * 100, 1),
                }
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取排行榜统计信息"""
        if not self.rankings:
            return {
                "total_players": 0,
                "avg_level": 0,
                "avg_exp": 0,
                "max_tower": 0,
            }
        
        return {
            "total_players": len(self.rankings),
            "avg_level": sum(r.level for r in self.rankings) / len(self.rankings),
            "avg_exp": sum(r.total_exp for r in self.rankings) / len(self.rankings),
            "max_tower": max(r.tower_level for r in self.rankings),
            "total_combats": sum(r.total_combats for r in self.rankings),
        }
