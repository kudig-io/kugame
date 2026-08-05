"""Web 后端共享依赖：封装 kugame 核心包

提供进程级单例 GameEngine 与默认玩家，使各路由复用真实游戏核心逻辑，
取代原先的硬编码 mock 数据。所有路由通过 get_engine() 获取同一引擎实例。
"""
import os
import sys
import threading
from typing import Any, Dict, Optional

# 将项目根目录加入路径，以复用 kugame 核心包
_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from kugame.game_engine import GameEngine  # noqa: E402
from kugame.player import Player, Sect  # noqa: E402

_lock = threading.Lock()
_engine: Optional[GameEngine] = None

# 商店货架缓存：保证同一玩家等级下商品ID稳定（核心每次随机生成）
_shop_cache: Dict[str, Any] = {"level": None, "items": []}

# 默认玩家与存档（Web 单用户演示场景）
DEFAULT_PLAYER_NAME = "web_player"
DEFAULT_SECT = Sect.青云宗
SAVE_PATH = os.path.join(_PROJECT_ROOT, "web_player_save.json")


def get_engine() -> GameEngine:
    """获取进程级单例 GameEngine，并确保已初始化玩家

    优先从存档恢复，失败则创建默认玩家。
    """
    global _engine
    if _engine is not None:
        return _engine
    with _lock:
        if _engine is None:
            engine = GameEngine()
            loaded: Optional[Player] = None
            if os.path.exists(SAVE_PATH):
                loaded = engine.load_player(SAVE_PATH)
            if loaded is None:
                engine.initialize_player(DEFAULT_PLAYER_NAME, DEFAULT_SECT)
            _engine = engine
    return _engine


def get_player() -> Player:
    """获取当前玩家（引擎已保证初始化）"""
    engine = get_engine()
    assert engine.player is not None
    return engine.player


def persist() -> bool:
    """将当前玩家状态持久化到 Web 存档"""
    engine = get_engine()
    if not engine.player:
        return False
    return engine.player.save(SAVE_PATH)


def get_shop_items() -> list:
    """获取商店货架（按玩家等级缓存，保证商品ID稳定）"""
    engine = get_engine()
    if not engine.player:
        return []
    level = engine.player.level
    if _shop_cache["level"] != level or not _shop_cache["items"]:
        _shop_cache["level"] = level
        _shop_cache["items"] = engine.get_shop_items()
    return _shop_cache["items"]


def player_view(player: Player) -> Dict[str, Any]:
    """玩家信息的 Web 公开视图"""
    return {
        "name": player.name,
        "sect": player.sect.value,
        "level": player.level,
        "cultivation_realm": player.cultivation.name,
        "cultivation_desc": player.cultivation.value[1],
        "exp": player.experience,
        "max_exp": player._calculate_required_exp(),
        "hp": player.health,
        "max_hp": player.total_max_health,
        "attack": player.total_attack,
        "defense": player.total_defense,
        "streak": player.streak,
        "title": player.title,
        "commands_mastered": len(player.kubectl_commands_mastered),
    }
