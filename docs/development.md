# KuGame 开发指南

本文档为开发者提供项目结构说明、代码规范和扩展指南。

## 目录

1. [项目结构](#项目结构)
2. [环境设置](#环境设置)
3. [代码规范](#代码规范)
4. [模块开发](#模块开发)
5. [测试指南](#测试指南)
6. [扩展开发](#扩展开发)

---

## 项目结构

```
kugame/
├── kugame/                      # 主包目录
│   ├── __init__.py             # 包初始化
│   ├── cli.py                  # 命令行界面 (915行)
│   ├── player.py               # 玩家系统 (900+行)
│   ├── story.py                # 故事系统 (450+行)
│   ├── kubernetes_commands.py  # 命令系统 (1000+行)
│   ├── game_engine.py          # 游戏引擎 (900+行)
│   ├── equipment.py            # 装备系统 (400+行)
│   ├── skills.py               # 技能系统 (350+行)
│   ├── talent_tree.py          # 天赋系统 (300+行)
│   ├── dungeon.py              # 副本系统 (250+行)
│   └── tower.py                # 挑战塔系统 (250+行)
├── tests/                       # 测试目录
│   ├── test_game_engine.py
│   ├── test_player.py
│   ├── test_story.py
│   └── test_kubernetes_commands.py
├── docs/                        # 文档目录
│   ├── architecture.md         # 架构文档
│   ├── player-guide.md         # 玩家指南
│   ├── development.md          # 开发指南
│   └── systems/                # 系统文档
│       ├── equipment.md
│       ├── skills.md
│       ├── talent_tree.md
│       ├── dungeon.md
│       └── tower.md
├── pyproject.toml              # 项目配置
├── README.md                   # 项目说明
└── test.bat                    # Windows测试脚本
```

---

## 环境设置

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/kugame.git
cd kugame

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"
```

### 开发工具

- **black**: 代码格式化
- **mypy**: 类型检查
- **pytest**: 测试框架
- **flake8**: 代码风格检查

---

## 代码规范

### 命名规范

- **类名**: PascalCase（如 `EquipmentManager`）
- **函数/方法**: snake_case（如 `generate_equipment`）
- **常量**: UPPER_SNAKE_CASE（如 `MAX_LEVEL`）
- **私有成员**: 前缀下划线（如 `_initialize`）

### 类型注解

所有函数必须使用类型注解：

```python
def generate_equipment(
    self, 
    equipment_type: Optional[EquipmentType] = None,
    player_level: int = 1
) -> Equipment:
    """生成装备"""
    pass
```

### 文档字符串

所有公共类和方法必须有文档字符串：

```python
class Equipment:
    """装备数据类
    
    存储装备的详细信息，包括名称、类型、品质、属性等。
    
    Attributes:
        id: 装备唯一标识
        name: 装备名称
        equipment_type: 装备类型
        quality: 装备品质
    """
```

### 代码格式化

使用 black 格式化代码：

```bash
black kugame/
```

### 类型检查

使用 mypy 检查类型：

```bash
mypy kugame/
```

---

## 模块开发

### 创建新模块的标准流程

以添加"成就系统"为例：

#### 1. 创建模块文件

`kugame/achievement.py`:

```python
"""成就系统

管理玩家成就，提供挑战目标和奖励。
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class AchievementType(Enum):
    """成就类型"""
    战斗 = "combat"
    收集 = "collection"
    探索 = "exploration"


@dataclass
class Achievement:
    """成就数据类"""
    id: str
    name: str
    description: str
    achievement_type: AchievementType
    condition: int
    reward: Dict[str, Any]
    unlocked: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "achievement_type": self.achievement_type.value,
            "condition": self.condition,
            "reward": self.reward,
            "unlocked": self.unlocked,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Achievement":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            achievement_type=AchievementType(data["achievement_type"]),
            condition=data["condition"],
            reward=data["reward"],
            unlocked=data.get("unlocked", False),
        )


class AchievementManager:
    """成就管理器"""
    
    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self._initialize_achievements()
    
    def _initialize_achievements(self) -> None:
        """初始化成就列表"""
        # 定义成就...
        pass
    
    def check_achievement(self, achievement_id: str, progress: int) -> bool:
        """检查并解锁成就"""
        achievement = self.achievements.get(achievement_id)
        if achievement and not achievement.unlocked:
            if progress >= achievement.condition:
                achievement.unlocked = True
                return True
        return False
```

#### 2. 集成到游戏引擎

在 `game_engine.py` 中添加：

```python
from .achievement import AchievementManager

class GameEngine:
    def __init__(self):
        # ... 现有初始化
        self.achievement_manager = AchievementManager()
```

#### 3. 添加 CLI 界面

在 `cli.py` 中添加菜单：

```python
def show_achievements(self) -> None:
    """显示成就列表"""
    self.clear_screen()
    self.console.print("[bold cyan]🏆 成就列表[/bold cyan]")
    # 展示成就...
```

#### 4. 更新 Player 类

在 `player.py` 中添加数据字段：

```python
@dataclass
class Player:
    # ... 现有字段
    achievement_manager_data: Optional[Dict[str, Any]] = None
```

#### 5. 更新存档逻辑

在 `to_dict` 和 `load` 方法中处理新数据。

#### 6. 编写测试

创建 `tests/test_achievement.py`：

```python
from kugame.achievement import Achievement, AchievementManager

class TestAchievement:
    def test_achievement_creation(self):
        achievement = Achievement(
            id="test_achievement",
            name="测试成就",
            description="这是一个测试成就",
            achievement_type=AchievementType.战斗,
            condition=10,
            reward={"experience": 100},
        )
        assert achievement.id == "test_achievement"
        assert not achievement.unlocked
```

#### 7. 更新文档

创建 `docs/systems/achievement.md` 文档。

---

## 测试指南

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_player.py -v

# 运行特定测试用例
pytest tests/test_player.py::TestPlayer::test_level_up -v

# 生成覆盖率报告
pytest tests/ --cov=kugame --cov-report=html
```

### 测试规范

1. **测试类命名**: `Test` + 被测类名
2. **测试方法命名**: `test_` + 被测方法名
3. **setup_method**: 每个测试前的初始化
4. **断言**: 使用 `assert` 语句

示例：

```python
class TestEquipment:
    """测试装备系统"""
    
    def setup_method(self):
        """测试初始化"""
        self.manager = EquipmentManager()
    
    def test_generate_equipment(self):
        """测试生成装备"""
        equipment = self.manager.generate_equipment(player_level=10)
        
        assert equipment is not None
        assert equipment.level >= 1
        assert equipment.quality in list(EquipmentQuality)
    
    def test_equipment_upgrade(self):
        """测试装备强化"""
        equipment = self.manager.generate_equipment()
        initial_level = equipment.level
        
        success = equipment.upgrade()
        
        assert success is True
        assert equipment.level == initial_level + 1
```

### 测试数据

使用 fixture 提供测试数据：

```python
import pytest

@pytest.fixture
def sample_player():
    """提供测试用玩家"""
    return Player(name="测试玩家", sect=Sect.青云宗)

def test_player_level_up(sample_player):
    """测试玩家升级"""
    sample_player.gain_experience(1000)
    assert sample_player.level > 1
```

---

## 扩展开发

### 添加新命令

1. 在 `kubernetes_commands.py` 中添加：

```python
"kubectl new command": KubectlCommand(
    name="kubectl new command",
    category=CommandCategory.基础操作,
    description="命令描述",
    syntax="kubectl new command [OPTIONS]",
    example="kubectl new command --option=value",
    kubernetes_concept="相关概念",
    difficulty=2,
),
```

2. 在对应章节中添加该命令到 `commands_to_learn`。

3. 更新命令速查表文档。

### 添加新装备

在 `EQUIPMENT_TEMPLATES` 中添加：

```python
EquipmentType.武器: [
    # 现有装备...
    {
        "name": "新武器",
        "attack": 50,
        "defense": 0,
        "health": 0,
        "exp": 0.1,
        "streak": 0.05,
    },
],
```

### 添加新技能

在 `SECT_SKILLS` 中添加：

```python
SECT_SKILLS = {
    Sect.青云宗: [
        # 现有技能...
        Skill(
            id="new_skill",
            name="新技能",
            description="技能描述",
            sect=Sect.青云宗,
            skill_type=SkillType.攻击,
            cooldown=3,
            effect_value=50,
            duration=2,
        ),
    ],
}
```

### 添加新天赋

在 `TALENT_TEMPLATES` 中添加：

```python
TALENT_TEMPLATES = {
    Sect.青云宗: {
        TalentBranch.攻击: [
            # 现有天赋...
            Talent(
                id="qy_atk_new",
                name="新天赋",
                description="天赋效果",
                branch=TalentBranch.攻击,
                tier=2,
                max_points=3,
                current_points=0,
                effect_per_point=5.0,
            ),
        ],
    },
}
```

---

## 性能优化

### 缓存策略

使用 `@property` 和缓存避免重复计算：

```python
class Player:
    def __init__(self):
        self._total_attack_cache = None
        self._cache_valid = False
    
    @property
    def total_attack(self) -> int:
        if not self._cache_valid:
            self._total_attack_cache = self._calculate_total_attack()
            self._cache_valid = True
        return self._total_attack_cache
    
    def equip_item(self, equipment: Equipment):
        # ... 装备逻辑
        self._cache_valid = False  # 使缓存失效
```

### 延迟加载

大型数据结构延迟初始化：

```python
class StoryManager:
    def __init__(self):
        self._chapters: Optional[Dict[Chapter, StoryChapter]] = None
    
    @property
    def chapters(self) -> Dict[Chapter, StoryChapter]:
        if self._chapters is None:
            self._chapters = self._initialize_chapters()
        return self._chapters
```

---

## 调试技巧

### 日志输出

使用 print 或 logging 输出调试信息：

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def some_function():
    logger.debug("进入函数")
    # ... 逻辑
    logger.debug(f"计算结果: {result}")
```

### 交互式调试

使用 ipdb 进行断点调试：

```python
import ipdb; ipdb.set_trace()
```

### 存档检查

手动检查存档文件内容：

```bash
cat player_save.json | python -m json.tool
```

---

## 发布流程

1. **版本号更新**: 修改 `__init__.py` 中的 `__version__`
2. **更新 README**: 添加更新日志
3. **运行测试**: 确保所有测试通过
4. **代码检查**: 运行 black 和 mypy
5. **构建发布**: `python -m build`
6. **上传 PyPI**: `twine upload dist/*`

---

## 相关文档

- [系统架构](./architecture.md)
- [玩家指南](./player-guide.md)
- [装备系统](./systems/equipment.md)
- [技能系统](./systems/skills.md)
- [天赋系统](./systems/talent_tree.md)
- [副本系统](./systems/dungeon.md)
- [挑战塔系统](./systems/tower.md)
