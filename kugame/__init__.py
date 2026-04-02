"""KuGame - 游戏化学习Kubernetes的命令行工具

通过武侠故事的方式，让学习Kubernetes命令变得有趣且富有挑战性。
"""

__version__ = "1.0.0"
__author__ = "KuGame Team"

from .player import Player
from .game_engine import GameEngine
from .story import StoryManager
from .kubernetes_commands import KubernetesCommandManager
from .equipment import Equipment, EquipmentType, EquipmentQuality, EquipmentManager
from .skills import Skill, SkillType, SkillManager, SECT_SKILLS
from .talent_tree import Talent, TalentBranch, TalentTree, TALENT_TEMPLATES
from .dungeon import Dungeon, DungeonType, DungeonManager, DAILY_DUNGEONS
from .tower import TowerLevel, TowerProgress, ChallengeTower

__all__ = [
    "__version__",
    "Player",
    "GameEngine",
    "StoryManager",
    "KubernetesCommandManager",
    "Equipment",
    "EquipmentType",
    "EquipmentQuality",
    "EquipmentManager",
    "Skill",
    "SkillType",
    "SkillManager",
    "SECT_SKILLS",
    "Talent",
    "TalentBranch",
    "TalentTree",
    "TALENT_TEMPLATES",
    "Dungeon",
    "DungeonType",
    "DungeonManager",
    "DAILY_DUNGEONS",
    "TowerLevel",
    "TowerProgress",
    "ChallengeTower",
]
