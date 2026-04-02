"""PVP竞技场系统

提供异步PVP对战、排名赛、赛季奖励等功能。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import random
import json
import os


class ArenaRank(Enum):
    """竞技场段位"""
    青铜 = (1, "青铜", 0, 1000)
    白银 = (2, "白银", 1000, 1200)
    黄金 = (3, "黄金", 1200, 1400)
    铂金 = (4, "铂金", 1400, 1600)
    钻石 = (5, "钻石", 1600, 1800)
    大师 = (6, "大师", 1800, 2000)
    王者 = (7, "王者", 2000, 9999)
    
    def __init__(self, level, name, min_rating, max_rating):
        self.level = level
        self.cn_name = name
        self.min_rating = min_rating
        self.max_rating = max_rating
    
    @classmethod
    def get_rank_by_rating(cls, rating: int) -> "ArenaRank":
        """根据积分获取段位"""
        for rank in cls:
            if rank.min_rating <= rating < rank.max_rating:
                return rank
        return cls.王者


@dataclass
class ArenaPlayer:
    """竞技场玩家数据
    
    Attributes:
        player_id: 玩家ID
        player_name: 玩家名称
        level: 玩家等级
        attack: 攻击力
        defense: 防御力
        health: 生命值
        equipment_score: 装备评分
        win_count: 胜场
        lose_count: 负场
        rating: 竞技场积分
        highest_rating: 最高积分
        rank: 段位
        streak: 连胜/连败
    """
    player_id: str
    player_name: str
    level: int = 1
    attack: int = 10
    defense: int = 5
    health: int = 100
    equipment_score: int = 0
    win_count: int = 0
    lose_count: int = 0
    rating: int = 1000
    highest_rating: int = 1000
    streak: int = 0
    last_battle_time: Optional[str] = None
    
    @property
    def total_battles(self) -> int:
        """总对战次数"""
        return self.win_count + self.lose_count
    
    @property
    def win_rate(self) -> float:
        """胜率"""
        if self.total_battles == 0:
            return 0.0
        return self.win_count / self.total_battles
    
    @property
    def rank(self) -> ArenaRank:
        """当前段位"""
        return ArenaRank.get_rank_by_rating(self.rating)
    
    def update_rating(self, delta: int):
        """更新积分"""
        self.rating += delta
        self.rating = max(0, self.rating)  # 最低0分
        if self.rating > self.highest_rating:
            self.highest_rating = self.rating
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "player_id": self.player_id,
            "player_name": self.player_name,
            "level": self.level,
            "attack": self.attack,
            "defense": self.defense,
            "health": self.health,
            "equipment_score": self.equipment_score,
            "win_count": self.win_count,
            "lose_count": self.lose_count,
            "rating": self.rating,
            "highest_rating": self.highest_rating,
            "streak": self.streak,
            "last_battle_time": self.last_battle_time,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArenaPlayer":
        """从字典创建"""
        return cls(
            player_id=data["player_id"],
            player_name=data["player_name"],
            level=data.get("level", 1),
            attack=data.get("attack", 10),
            defense=data.get("defense", 5),
            health=data.get("health", 100),
            equipment_score=data.get("equipment_score", 0),
            win_count=data.get("win_count", 0),
            lose_count=data.get("lose_count", 0),
            rating=data.get("rating", 1000),
            highest_rating=data.get("highest_rating", 1000),
            streak=data.get("streak", 0),
            last_battle_time=data.get("last_battle_time"),
        )


@dataclass
class ArenaBattle:
    """竞技场战斗记录
    
    Attributes:
        battle_id: 战斗ID
        attacker_id: 攻击方ID
        defender_id: 防守方ID
        winner_id: 胜利方ID
        attacker_rating_change: 攻击方积分变化
        defender_rating_change: 防守方积分变化
        battle_time: 战斗时间
        battle_log: 战斗日志
    """
    battle_id: str
    attacker_id: str
    defender_id: str
    winner_id: str
    attacker_rating_before: int
    defender_rating_before: int
    attacker_rating_change: int
    defender_rating_change: int
    battle_time: str
    battle_log: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "battle_id": self.battle_id,
            "attacker_id": self.attacker_id,
            "defender_id": self.defender_id,
            "winner_id": self.winner_id,
            "attacker_rating_before": self.attacker_rating_before,
            "defender_rating_before": self.defender_rating_before,
            "attacker_rating_change": self.attacker_rating_change,
            "defender_rating_change": self.defender_rating_change,
            "battle_time": self.battle_time,
            "battle_log": self.battle_log,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArenaBattle":
        """从字典创建"""
        return cls(
            battle_id=data["battle_id"],
            attacker_id=data["attacker_id"],
            defender_id=data["defender_id"],
            winner_id=data["winner_id"],
            attacker_rating_before=data["attacker_rating_before"],
            defender_rating_before=data["defender_rating_before"],
            attacker_rating_change=data["attacker_rating_change"],
            defender_rating_change=data["defender_rating_change"],
            battle_time=data["battle_time"],
            battle_log=data.get("battle_log", []),
        )


@dataclass
class SeasonInfo:
    """赛季信息"""
    season_id: str
    season_name: str
    start_time: str
    end_time: str
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "season_id": self.season_id,
            "season_name": self.season_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_active": self.is_active,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SeasonInfo":
        return cls(
            season_id=data["season_id"],
            season_name=data["season_name"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            is_active=data.get("is_active", True),
        )


class ArenaSystem:
    """竞技场系统
    
    管理PVP竞技场功能，包括匹配、战斗、排名、赛季等。
    """
    
    # 积分计算参数
    K_FACTOR_BASE = 32  # 基础K值
    RATING_DIFF_SCALE = 400  # 积分差缩放
    
    # 连胜/连败加成
    STREAK_BONUS = {
        3: 5,
        5: 10,
        7: 20,
        10: 50,
    }
    
    def __init__(self, data_dir: str = None):
        """初始化
        
        Args:
            data_dir: 数据存储目录，默认使用项目目录
        """
        if data_dir is None:
            data_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.data_dir = data_dir
        self.players: Dict[str, ArenaPlayer] = {}
        self.battle_history: List[ArenaBattle] = []
        self.current_season: Optional[SeasonInfo] = None
        
        self._load_data()
        self._check_season()
    
    def _get_data_file(self) -> str:
        """获取数据文件路径"""
        return os.path.join(self.data_dir, "arena_data.json")
    
    def _load_data(self):
        """加载数据"""
        file_path = self._get_data_file()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.players = {
                        pid: ArenaPlayer.from_dict(p)
                        for pid, p in data.get("players", {}).items()
                    }
                    self.battle_history = [
                        ArenaBattle.from_dict(b)
                        for b in data.get("battle_history", [])
                    ]
                    if data.get("current_season"):
                        self.current_season = SeasonInfo.from_dict(data["current_season"])
            except Exception as e:
                print(f"加载竞技场数据失败: {e}")
                self._init_default_data()
        else:
            self._init_default_data()
    
    def _save_data(self):
        """保存数据"""
        file_path = self._get_data_file()
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "players": {
                        pid: p.to_dict()
                        for pid, p in self.players.items()
                    },
                    "battle_history": [b.to_dict() for b in self.battle_history[-100:]],  # 只保留最近100场
                    "current_season": self.current_season.to_dict() if self.current_season else None,
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存竞技场数据失败: {e}")
    
    def _init_default_data(self):
        """初始化默认数据"""
        self._create_new_season()
    
    def _create_new_season(self):
        """创建新赛季"""
        now = datetime.now()
        season_num = 1
        if self.current_season:
            # 从旧赛季名称提取数字
            try:
                season_num = int(self.current_season.season_name.replace("第", "").replace("赛季", "")) + 1
            except:
                season_num = 1
        
        self.current_season = SeasonInfo(
            season_id=f"season_{now.strftime('%Y%m')}",
            season_name=f"第{season_num}赛季",
            start_time=now.isoformat(),
            end_time=(now + timedelta(days=30)).isoformat(),
            is_active=True,
        )
        
        # 重置玩家积分（但保留最高积分记录）
        for player in self.players.values():
            player.rating = 1000
            player.streak = 0
        
        self._save_data()
    
    def _check_season(self):
        """检查赛季状态"""
        if not self.current_season:
            self._create_new_season()
            return
        
        # 检查是否过期
        end_time = datetime.fromisoformat(self.current_season.end_time)
        if datetime.now() > end_time:
            # 结算赛季奖励
            self._settle_season_rewards()
            # 创建新赛季
            self._create_new_season()
    
    def _settle_season_rewards(self):
        """结算赛季奖励"""
        # 按积分排序
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: p.rating,
            reverse=True
        )
        
        # 这里可以实现赛季奖励发放逻辑
        # 例如：前10名获得特殊奖励
        pass
    
    def register_player(self, player_data: Dict[str, Any]) -> ArenaPlayer:
        """注册竞技场玩家
        
        Args:
            player_data: 玩家数据字典
            
        Returns:
            ArenaPlayer: 竞技场玩家对象
        """
        player_id = player_data["player_id"]
        
        if player_id in self.players:
            # 更新数据
            player = self.players[player_id]
            player.player_name = player_data.get("player_name", player.player_name)
            player.level = player_data.get("level", player.level)
            player.attack = player_data.get("attack", player.attack)
            player.defense = player_data.get("defense", player.defense)
            player.health = player_data.get("health", player.health)
            player.equipment_score = player_data.get("equipment_score", player.equipment_score)
        else:
            # 创建新玩家
            player = ArenaPlayer(
                player_id=player_id,
                player_name=player_data.get("player_name", "未知"),
                level=player_data.get("level", 1),
                attack=player_data.get("attack", 10),
                defense=player_data.get("defense", 5),
                health=player_data.get("health", 100),
                equipment_score=player_data.get("equipment_score", 0),
            )
            self.players[player_id] = player
        
        self._save_data()
        return player
    
    def find_match(self, player_id: str) -> Optional[ArenaPlayer]:
        """寻找匹配对手
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Optional[ArenaPlayer]: 匹配到的对手，如果没有则返回None
        """
        if player_id not in self.players:
            return None
        
        player = self.players[player_id]
        player_rating = player.rating
        
        # 查找积分相近的对手
        # 积分差在200分以内
        candidates = [
            p for p in self.players.values()
            if p.player_id != player_id
            and abs(p.rating - player_rating) <= 200
        ]
        
        if not candidates:
            # 如果没有找到，放宽条件到所有玩家
            candidates = [
                p for p in self.players.values()
                if p.player_id != player_id
            ]
        
        if not candidates:
            # 如果还是没有，返回AI对手
            return self._create_ai_opponent(player_rating)
        
        # 按积分接近程度排序，优先选择接近的
        candidates.sort(key=lambda p: abs(p.rating - player_rating))
        
        # 前3个中随机选择
        top_candidates = candidates[:min(3, len(candidates))]
        return random.choice(top_candidates)
    
    def _create_ai_opponent(self, target_rating: int) -> ArenaPlayer:
        """创建AI对手
        
        Args:
            target_rating: 目标积分
            
        Returns:
            ArenaPlayer: AI对手
        """
        ai_names = [
            "剑圣", "刀狂", "拳霸", "枪神", "弓灵",
            "影刺", "法尊", "道玄", "佛心", "魔君",
        ]
        
        name = random.choice(ai_names)
        # 根据积分计算属性
        rating_diff = target_rating - 1000
        level = max(1, min(100, 10 + rating_diff // 50))
        
        return ArenaPlayer(
            player_id=f"ai_{random.randint(1000, 9999)}",
            player_name=f"[{name}]",
            level=level,
            attack=10 + level * 2 + rating_diff // 100,
            defense=5 + level + rating_diff // 200,
            health=100 + level * 10,
            equipment_score=level * 10,
            rating=target_rating + random.randint(-50, 50),
        )
    
    def calculate_battle_result(self, attacker: ArenaPlayer, defender: ArenaPlayer) -> Dict[str, Any]:
        """计算战斗结果
        
        简化版战斗模拟，基于属性计算胜率
        
        Args:
            attacker: 攻击方
            defender: 防守方
            
        Returns:
            Dict: 战斗结果
        """
        # 计算战力
        attacker_power = attacker.attack * 2 + attacker.defense + attacker.health // 10 + attacker.equipment_score
        defender_power = defender.attack * 2 + defender.defense + defender.health // 10 + defender.equipment_score
        
        # 计算胜率
        total_power = attacker_power + defender_power
        attacker_win_rate = attacker_power / total_power if total_power > 0 else 0.5
        
        # 随机决定胜负
        attacker_wins = random.random() < attacker_win_rate
        
        return {
            "attacker_wins": attacker_wins,
            "attacker_power": attacker_power,
            "defender_power": defender_power,
            "win_rate": attacker_win_rate,
        }
    
    def _calculate_rating_change(self, winner: ArenaPlayer, loser: ArenaPlayer) -> tuple:
        """计算积分变化
        
        使用ELO算法变种
        
        Returns:
            tuple: (胜者积分变化, 败者积分变化)
        """
        rating_diff = loser.rating - winner.rating
        expected_score = 1 / (1 + 10 ** (rating_diff / self.RATING_DIFF_SCALE))
        
        # 基础K值根据段位调整
        k_factor = self.K_FACTOR_BASE
        if winner.rank.level >= 5:  # 钻石以上
            k_factor = 16
        elif winner.rank.level <= 2:  # 青铜白银
            k_factor = 48
        
        # 连胜加成
        winner_bonus = 0
        for streak, bonus in sorted(self.STREAK_BONUS.items()):
            if winner.streak >= streak:
                winner_bonus = bonus
        
        winner_change = int(k_factor * (1 - expected_score)) + winner_bonus
        loser_change = -int(k_factor * expected_score)
        
        return winner_change, loser_change
    
    def battle(self, attacker_id: str, defender_id: str) -> Dict[str, Any]:
        """进行战斗
        
        Args:
            attacker_id: 攻击方ID
            defender_id: 防守方ID
            
        Returns:
            Dict: 战斗结果
        """
        if attacker_id not in self.players:
            return {"success": False, "message": "攻击方未注册"}
        
        attacker = self.players[attacker_id]
        
        # 获取防守方
        if defender_id.startswith("ai_"):
            defender = self._create_ai_opponent(attacker.rating)
        elif defender_id in self.players:
            defender = self.players[defender_id]
        else:
            return {"success": False, "message": "防守方未找到"}
        
        # 记录战斗前积分
        attacker_rating_before = attacker.rating
        defender_rating_before = defender.rating
        
        # 计算战斗结果
        result = self.calculate_battle_result(attacker, defender)
        attacker_wins = result["attacker_wins"]
        
        # 更新胜负统计
        if attacker_wins:
            attacker.win_count += 1
            attacker.streak = max(1, attacker.streak + 1) if attacker.streak > 0 else 1
            if not defender_id.startswith("ai_"):
                defender.lose_count += 1
                defender.streak = min(-1, defender.streak - 1) if defender.streak < 0 else -1
            winner_id = attacker_id
        else:
            attacker.lose_count += 1
            attacker.streak = min(-1, attacker.streak - 1) if attacker.streak < 0 else -1
            if not defender_id.startswith("ai_"):
                defender.win_count += 1
                defender.streak = max(1, defender.streak + 1) if defender.streak > 0 else 1
            winner_id = defender_id
        
        # 计算积分变化
        if attacker_wins:
            winner_change, loser_change = self._calculate_rating_change(attacker, defender)
            attacker_rating_change = winner_change
            defender_rating_change = loser_change
            attacker.update_rating(winner_change)
            if not defender_id.startswith("ai_"):
                defender.update_rating(loser_change)
        else:
            if not defender_id.startswith("ai_"):
                winner_change, loser_change = self._calculate_rating_change(defender, attacker)
                defender_rating_change = winner_change
                defender.update_rating(winner_change)
            else:
                defender_rating_change = 0
            # 攻击方失败扣分
            expected_score = 1 / (1 + 10 ** ((defender.rating - attacker.rating) / self.RATING_DIFF_SCALE))
            attacker_rating_change = -int(self.K_FACTOR_BASE * expected_score)
            attacker.update_rating(attacker_rating_change)
        
        # 更新时间
        now = datetime.now().isoformat()
        attacker.last_battle_time = now
        if not defender_id.startswith("ai_"):
            defender.last_battle_time = now
        
        # 创建战斗记录
        battle = ArenaBattle(
            battle_id=f"battle_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            attacker_id=attacker_id,
            defender_id=defender_id,
            winner_id=winner_id,
            attacker_rating_before=attacker_rating_before,
            defender_rating_before=defender_rating_before,
            attacker_rating_change=attacker_rating_change,
            defender_rating_change=defender_rating_change,
            battle_time=now,
            battle_log=[
                f"战斗开始！{attacker.player_name} VS {defender.player_name}",
                f"{attacker.player_name} 战力: {result['attacker_power']}",
                f"{defender.player_name} 战力: {result['defender_power']}",
                f"战斗结束！{self.players.get(winner_id, defender).player_name} 获胜！",
            ],
        )
        
        self.battle_history.append(battle)
        self._save_data()
        
        return {
            "success": True,
            "battle_id": battle.battle_id,
            "winner_id": winner_id,
            "attacker_wins": attacker_wins,
            "attacker": {
                "id": attacker_id,
                "name": attacker.player_name,
                "rating_change": attacker_rating_change,
                "rating": attacker.rating,
                "rank": attacker.rank.cn_name,
            },
            "defender": {
                "id": defender_id,
                "name": defender.player_name,
                "rating_change": defender_rating_change if not defender_id.startswith("ai_") else 0,
                "rating": defender.rating if not defender_id.startswith("ai_") else defender_rating_before,
                "rank": defender.rank.cn_name if not defender_id.startswith("ai_") else "AI",
            },
            "battle_log": battle.battle_log,
        }
    
    def get_ranking(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取竞技场排名
        
        Args:
            limit: 返回数量
            
        Returns:
            List[Dict]: 排名列表
        """
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: (p.rating, p.win_rate),
            reverse=True
        )
        
        return [
            {
                "rank": i,
                "player_id": p.player_id,
                "player_name": p.player_name,
                "level": p.level,
                "rating": p.rating,
                "rank_name": p.rank.cn_name,
                "win_count": p.win_count,
                "lose_count": p.lose_count,
                "win_rate": round(p.win_rate * 100, 1),
            }
            for i, p in enumerate(sorted_players[:limit], 1)
        ]
    
    def get_player_info(self, player_id: str) -> Optional[Dict[str, Any]]:
        """获取玩家竞技场信息
        
        Args:
            player_id: 玩家ID
            
        Returns:
            Optional[Dict]: 玩家信息
        """
        if player_id not in self.players:
            return None
        
        p = self.players[player_id]
        
        # 获取排名
        ranking = self.get_ranking(1000)
        player_rank = 0
        for r in ranking:
            if r["player_id"] == player_id:
                player_rank = r["rank"]
                break
        
        return {
            "player_id": p.player_id,
            "player_name": p.player_name,
            "level": p.level,
            "rating": p.rating,
            "highest_rating": p.highest_rating,
            "rank": p.rank.cn_name,
            "rank_level": p.rank.level,
            "win_count": p.win_count,
            "lose_count": p.lose_count,
            "win_rate": round(p.win_rate * 100, 1),
            "streak": p.streak,
            "current_rank": player_rank,
            "season": self.current_season.season_name if self.current_season else None,
        }
    
    def get_battle_history(self, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """获取玩家战斗历史
        
        Args:
            player_id: 玩家ID
            limit: 返回数量
            
        Returns:
            List[Dict]: 战斗历史
        """
        player_battles = [
            b for b in self.battle_history
            if b.attacker_id == player_id or b.defender_id == player_id
        ]
        
        # 按时间倒序
        player_battles.sort(key=lambda b: b.battle_time, reverse=True)
        
        return [
            {
                "battle_id": b.battle_id,
                "opponent_name": self.players.get(
                    b.defender_id if b.attacker_id == player_id else b.attacker_id,
                    ArenaPlayer(player_id="unknown", player_name="未知")
                ).player_name,
                "is_attacker": b.attacker_id == player_id,
                "is_winner": b.winner_id == player_id,
                "rating_change": b.attacker_rating_change if b.attacker_id == player_id else b.defender_rating_change,
                "battle_time": b.battle_time,
            }
            for b in player_battles[:limit]
        ]
    
    def get_season_info(self) -> Dict[str, Any]:
        """获取当前赛季信息
        
        Returns:
            Dict: 赛季信息
        """
        if not self.current_season:
            return {"error": "当前没有进行中的赛季"}
        
        # 计算剩余时间
        end_time = datetime.fromisoformat(self.current_season.end_time)
        remaining = end_time - datetime.now()
        
        return {
            "season_id": self.current_season.season_id,
            "season_name": self.current_season.season_name,
            "start_time": self.current_season.start_time,
            "end_time": self.current_season.end_time,
            "days_remaining": remaining.days,
            "is_active": self.current_season.is_active,
        }
