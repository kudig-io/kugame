"""API Routes Package"""
from .player import router as player_router
from .game import router as game_router
from .combat import router as combat_router
from .shop import router as shop_router
from .inventory import router as inventory_router
from .k8s import router as k8s_router

__all__ = [
    "player_router",
    "game_router",
    "combat_router",
    "shop_router",
    "inventory_router",
    "k8s_router",
]
