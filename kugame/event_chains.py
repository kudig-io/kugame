"""事件链系统

提供连续的随机事件，玩家的选择会影响后续事件发展。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import random


class EventRarity(Enum):
    """事件稀有度"""
    普通 = "common"
    稀有 = "rare"
    史诗 = "epic"
    传说 = "legendary"


class EventChoiceResult(Enum):
    """事件选择结果类型"""
    获得经验 = "gain_exp"
    获得金币 = "gain_gold"
    获得装备 = "gain_equipment"
    获得宝石 = "gain_gem"
    获得体力 = "gain_stamina"
    失去体力 = "lose_stamina"
    触发战斗 = "trigger_combat"
    触发事件 = "trigger_event"
    无效果 = "none"


@dataclass
class EventChoice:
    """事件选项
    
    Attributes:
        choice_id: 选项ID
        description: 选项描述
        result_type: 结果类型
        result_value: 结果数值
        result_description: 结果描述
        next_event_id: 后续事件ID（可选）
    """
    choice_id: str
    description: str
    result_type: EventChoiceResult
    result_value: Any = None
    result_description: str = ""
    next_event_id: Optional[str] = None
    success_rate: float = 1.0  # 成功率


@dataclass
class RandomEvent:
    """随机事件
    
    Attributes:
        id: 事件ID
        name: 事件名称
        description: 事件描述
        rarity: 稀有度
        choices: 选项列表
        is_chain_start: 是否是事件链开始
        chain_id: 所属事件链ID
    """
    id: str
    name: str
    description: str
    rarity: EventRarity
    choices: List[EventChoice] = field(default_factory=list)
    is_chain_start: bool = False
    chain_id: Optional[str] = None


# 事件链定义
EVENT_CHAINS = {
    "炼丹奇遇": {
        "rarity": EventRarity.稀有,
        "events": [
            {
                "id": "alchemy_start",
                "name": "炼丹炉前的抉择",
                "description": "你在山中偶遇一位炼丹师，他正在炼制一炉丹药。炼丹师见你资质不错，邀请你帮忙看守丹炉。",
                "is_chain_start": True,
                "choices": [
                    EventChoice(
                        choice_id="help_carefully",
                        description="小心翼翼地看守丹炉",
                        result_type=EventChoiceResult.获得经验,
                        result_value=200,
                        result_description="丹药炼制成功！炼丹师赠你一枚经验丹。",
                        success_rate=0.8,
                        next_event_id="alchemy_success",
                    ),
                    EventChoice(
                        choice_id="add_ingredient",
                        description="偷偷加入自己的材料",
                        result_type=EventChoiceResult.触发事件,
                        result_description="丹炉突然冒出奇异光芒...",
                        success_rate=0.5,
                        next_event_id="alchemy_mystery",
                    ),
                    EventChoice(
                        choice_id="refuse",
                        description="婉言谢绝",
                        result_type=EventChoiceResult.无效果,
                        result_description="你礼貌地离开了。",
                    ),
                ],
            },
            {
                "id": "alchemy_success",
                "name": "炼丹师的馈赠",
                "description": "炼丹师对你的表现非常满意，决定传授你一些炼丹心得。",
                "choices": [
                    EventChoice(
                        choice_id="learn_alchemy",
                        description="认真学习",
                        result_type=EventChoiceResult.获得经验,
                        result_value=500,
                        result_description="你学会了炼丹的基础知识！",
                    ),
                    EventChoice(
                        choice_id="ask_for_reward",
                        description="请求更多奖励",
                        result_type=EventChoiceResult.获得装备,
                        result_value={"quality": 3},  # 稀有装备
                        result_description="炼丹师给了你一件法器。",
                    ),
                ],
            },
            {
                "id": "alchemy_mystery",
                "name": "神秘的变异",
                "description": "丹炉中突然传出一股异香，一枚散发着金光的丹药缓缓升起！",
                "choices": [
                    EventChoice(
                        choice_id="take_immediately",
                        description="立即取走",
                        result_type=EventChoiceResult.获得经验,
                        result_value=1000,
                        result_description="你获得了一枚珍贵的金丹！",
                    ),
                    EventChoice(
                        choice_id="share_with_master",
                        description="与炼丹师分享",
                        result_type=EventChoiceResult.获得宝石,
                        result_value={"quality": 4},  # 史诗宝石
                        result_description="炼丹师感激不已，赠你一颗稀世宝石。",
                    ),
                ],
            },
        ],
    },
    
    "古墓探险": {
        "rarity": EventRarity.史诗,
        "events": [
            {
                "id": "tomb_discovery",
                "name": "古墓现世",
                "description": "你在修炼时发现了一座隐秘的古墓入口，阴冷的气息从中渗出。",
                "is_chain_start": True,
                "choices": [
                    EventChoice(
                        choice_id="enter_bravely",
                        description="勇敢地进入",
                        result_type=EventChoiceResult.触发事件,
                        result_description="你踏入了古墓...",
                        next_event_id="tomb_corridor",
                    ),
                    EventChoice(
                        choice_id="prepare_first",
                        description="先做准备",
                        result_type=EventChoiceResult.失去体力,
                        result_value=10,
                        result_description="你休息了一会儿，恢复了一些体力。",
                        next_event_id="tomb_corridor",
                    ),
                ],
            },
            {
                "id": "tomb_corridor",
                "name": "幽暗的走廊",
                "description": "古墓走廊两侧排列着石像，你的脚步声在空旷的走廊中回荡。",
                "choices": [
                    EventChoice(
                        choice_id="check_statues",
                        description="检查石像",
                        result_type=EventChoiceResult.触发战斗,
                        result_value={"level": 15},
                        result_description="石像突然动了起来！",
                    ),
                    EventChoice(
                        choice_id="move_forward",
                        description="快速通过",
                        result_type=EventChoiceResult.触发事件,
                        result_description="你来到了一个分岔路口...",
                        next_event_id="tomb_crossroad",
                    ),
                ],
            },
            {
                "id": "tomb_crossroad",
                "name": "分岔路口",
                "description": "面前有三条路：左边散发着金光，中间阴风阵阵，右边传来水声。",
                "choices": [
                    EventChoice(
                        choice_id="left_path",
                        description="走金光之路",
                        result_type=EventChoiceResult.获得装备,
                        result_value={"quality": 4},  # 史诗装备
                        result_description="你发现了一个藏宝室！",
                    ),
                    EventChoice(
                        choice_id="middle_path",
                        description="走阴风之路",
                        result_type=EventChoiceResult.触发战斗,
                        result_value={"level": 20, "is_boss": True},
                        result_description="一只千年僵尸挡在面前！",
                    ),
                    EventChoice(
                        choice_id="right_path",
                        description="走水路",
                        result_type=EventChoiceResult.获得体力,
                        result_value=50,
                        result_description="你发现了一处灵泉，恢复了大量体力。",
                    ),
                ],
            },
        ],
    },
    
    "仙人指点": {
        "rarity": EventRarity.传说,
        "events": [
            {
                "id": "immortal_encounter",
                "name": "云游仙人",
                "description": "一位白发仙人在云端向你招手，他的气息深不可测。",
                "is_chain_start": True,
                "choices": [
                    EventChoice(
                        choice_id="pay_respect",
                        description="恭敬行礼",
                        result_type=EventChoiceResult.触发事件,
                        result_description="仙人微笑点头...",
                        next_event_id="immortal_test",
                    ),
                    EventChoice(
                        choice_id="ask_enlightenment",
                        description="求教大道",
                        result_type=EventChoiceResult.获得经验,
                        result_value=2000,
                        result_description="仙人指点迷津，你茅塞顿开！",
                    ),
                ],
            },
            {
                "id": "immortal_test",
                "name": "仙人的考验",
                "description": "仙人决定考验你的心性，出了一道难题。",
                "choices": [
                    EventChoice(
                        choice_id="answer_wisely",
                        description="用心回答",
                        result_type=EventChoiceResult.获得宝石,
                        result_value={"quality": 5},  # 传说宝石
                        result_description="仙人满意地赠你一颗仙石。",
                    ),
                    EventChoice(
                        choice_id="ask_for_power",
                        description="请求力量",
                        result_type=EventChoiceResult.无效果,
                        result_description="仙人摇头叹息，化作清风而去。",
                    ),
                ],
            },
        ],
    },
}


# 独立随机事件
SINGLE_EVENTS = [
    RandomEvent(
        id="treasure_find",
        name="意外之财",
        description="你在路边发现了一个被遗忘的宝箱。",
        rarity=EventRarity.普通,
        choices=[
            EventChoice(
                choice_id="open",
                description="打开宝箱",
                result_type=EventChoiceResult.获得金币,
                result_value=100,
                result_description="你获得了一些金币！",
            ),
        ],
    ),
    RandomEvent(
        id="strange_merchant",
        name="神秘商人",
        description="一个戴着斗篷的神秘商人拦住了你，他有一些稀有物品想要出售。",
        rarity=EventRarity.稀有,
        choices=[
            EventChoice(
                choice_id="buy",
                description="购买物品",
                result_type=EventChoiceResult.获得装备,
                result_value={"quality": 3},
                result_description="你获得了一件稀有装备！",
            ),
            EventChoice(
                choice_id="refuse",
                description="婉拒离开",
                result_type=EventChoiceResult.无效果,
                result_description="商人消失在阴影中。",
            ),
        ],
    ),
    RandomEvent(
        id="fallen_disciple",
        name="落难弟子",
        description="一位受伤的弟子躺在路边，请求你的帮助。",
        rarity=EventRarity.普通,
        choices=[
            EventChoice(
                choice_id="help",
                description="施以援手",
                result_type=EventChoiceResult.获得经验,
                result_value=150,
                result_description="弟子感激不尽，与你分享了一些修炼心得。",
            ),
            EventChoice(
                choice_id="ignore",
                description="视而不见",
                result_type=EventChoiceResult.无效果,
                result_description="你默默地走开了。",
            ),
        ],
    ),
]


class EventChainManager:
    """事件链管理器"""
    
    def __init__(self):
        self.current_chain: Optional[str] = None
        self.current_event_id: Optional[str] = None
        self.chain_history: List[str] = []
    
    def trigger_random_event(self, player_level: int = 1) -> Optional[RandomEvent]:
        """触发随机事件
        
        Args:
            player_level: 玩家等级
            
        Returns:
            Optional[RandomEvent]: 触发的事件
        """
        # 首先检查是否继续事件链
        if self.current_chain and self.current_event_id:
            chain = EVENT_CHAINS.get(self.current_chain)
            if chain:
                for event_data in chain["events"]:
                    if event_data["id"] == self.current_event_id:
                        return self._create_event_from_data(event_data, self.current_chain)
        
        # 随机选择新事件
        # 20%概率触发事件链
        if random.random() < 0.2:
            available_chains = [
                (name, data) for name, data in EVENT_CHAINS.items()
                if self._can_trigger_chain(data, player_level)
            ]
            if available_chains:
                chain_name, chain_data = random.choice(available_chains)
                # 找到链的起始事件
                for event_data in chain_data["events"]:
                    if event_data.get("is_chain_start", False):
                        self.current_chain = chain_name
                        self.current_event_id = event_data["id"]
                        return self._create_event_from_data(event_data, chain_name)
        
        # 触发独立事件
        if SINGLE_EVENTS:
            event = random.choice(SINGLE_EVENTS)
            # 根据稀有度决定是否触发
            rarity_weights = {
                EventRarity.普通: 0.6,
                EventRarity.稀有: 0.3,
                EventRarity.史诗: 0.09,
                EventRarity.传说: 0.01,
            }
            if random.random() < rarity_weights.get(event.rarity, 0.5):
                return event
        
        return None
    
    def _can_trigger_chain(self, chain_data: Dict, player_level: int) -> bool:
        """检查是否可以触发事件链"""
        # 根据稀有度和玩家等级判断
        rarity = chain_data["rarity"]
        level_requirements = {
            EventRarity.普通: 1,
            EventRarity.稀有: 10,
            EventRarity.史诗: 25,
            EventRarity.传说: 40,
        }
        return player_level >= level_requirements.get(rarity, 1)
    
    def _create_event_from_data(self, event_data: Dict, chain_id: str) -> RandomEvent:
        """从数据创建事件"""
        return RandomEvent(
            id=event_data["id"],
            name=event_data["name"],
            description=event_data["description"],
            rarity=EVENT_CHAINS[chain_id]["rarity"],
            choices=event_data.get("choices", []),
            is_chain_start=event_data.get("is_chain_start", False),
            chain_id=chain_id,
        )
    
    def make_choice(self, choice_id: str) -> Dict[str, Any]:
        """做出选择
        
        Args:
            choice_id: 选项ID
            
        Returns:
            Dict: 结果信息
        """
        if not self.current_event_id:
            return {"success": False, "message": "没有进行中的事件"}
        
        # 获取当前事件
        chain = EVENT_CHAINS.get(self.current_chain)
        if not chain:
            return {"success": False, "message": "事件链不存在"}
        
        current_event = None
        for event_data in chain["events"]:
            if event_data["id"] == self.current_event_id:
                current_event = event_data
                break
        
        if not current_event:
            return {"success": False, "message": "事件不存在"}
        
        # 查找选项
        choice = None
        for c in current_event.get("choices", []):
            if c.choice_id == choice_id:
                choice = c
                break
        
        if not choice:
            return {"success": False, "message": "选项不存在"}
        
        # 计算成功率
        import random
        if random.random() > choice.success_rate:
            # 失败
            return {
                "success": False,
                "message": "选择失败，什么都没发生...",
                "result_type": EventChoiceResult.无效果,
            }
        
        # 记录历史
        self.chain_history.append(self.current_event_id)
        
        # 设置下一个事件
        if choice.next_event_id:
            self.current_event_id = choice.next_event_id
        else:
            # 事件链结束
            self.current_chain = None
            self.current_event_id = None
        
        return {
            "success": True,
            "message": choice.result_description,
            "result_type": choice.result_type,
            "result_value": choice.result_value,
            "chain_continues": choice.next_event_id is not None,
        }
    
    def end_current_chain(self):
        """结束当前事件链"""
        self.current_chain = None
        self.current_event_id = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "current_chain": self.current_chain,
            "current_event_id": self.current_event_id,
            "chain_history": self.chain_history,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventChainManager":
        """从字典创建"""
        manager = cls()
        manager.current_chain = data.get("current_chain")
        manager.current_event_id = data.get("current_event_id")
        manager.chain_history = data.get("chain_history", [])
        return manager
