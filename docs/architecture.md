# KuGame 系统架构文档

## 项目概述

KuGame 是一款基于 Python 的终端游戏，通过武侠修仙的故事背景，帮助玩家学习 Kubernetes 命令。项目采用模块化设计，便于扩展和维护。

## 技术栈

- **语言**: Python 3.8+
- **UI 库**: Rich（终端美化）
- **数据序列化**: JSON
- **测试框架**: pytest
- **代码规范**: black, mypy, flake8

## 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI 层 (cli.py)                       │
│  负责用户交互、界面展示、菜单处理                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     游戏引擎层 (game_engine.py)               │
│  核心业务逻辑、状态管理、数据流转                              │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   玩家系统     │    │   故事系统     │    │  命令系统      │
│  (player.py)  │    │  (story.py)   │    │ (kubernetes_  │
│               │    │               │    │  commands.py) │
│ • 角色属性    │    │ • 章节管理    │    │ • 命令数据    │
│ • 成长系统    │    │ • 剧情内容    │    │ • 学习进度    │
│ • 存档管理    │    │ • 随机事件    │    │ • 测验生成    │
└───────────────┘    └───────────────┘    └───────────────┘
            │
            ├─────────────────┬─────────────────┐
            ▼                 ▼                 ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   装备系统     │    │   技能系统     │    │  天赋系统      │
│(equipment.py) │    │ (skills.py)   │    │(talent_tree.py)│
└───────────────┘    └───────────────┘    └───────────────┘
            │
            ├─────────────────┬─────────────────┐
            ▼                 ▼                 ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   副本系统     │    │   挑战塔系统   │    │   战斗系统     │
│ (dungeon.py)  │    │  (tower.py)   │    │ (内置于引擎)   │
└───────────────┘    └───────────────┘    └───────────────┘
```

## 模块详解

### 1. CLI 层 (cli.py)

**职责**: 用户界面和交互

**主要功能**:
- 游戏启动和初始化
- 菜单显示和用户输入处理
- 战斗界面
- 装备/商店/副本界面
- 进度展示

**设计要点**:
- 使用 Rich 库美化终端输出
- 遵循单一职责原则，每个界面独立成方法
- 错误处理和用户提示

### 2. 游戏引擎 (game_engine.py)

**职责**: 核心业务逻辑协调

**主要功能**:
- 玩家生命周期管理
- 挑战生成和答案验证
- 战斗系统
- 装备/副本/挑战塔功能集成
- 存档管理

**关键类**:
```python
class GameEngine:
    - player: Player                    # 当前玩家
    - story_manager: StoryManager       # 故事管理
    - command_manager: KubernetesCommandManager  # 命令管理
    - equipment_manager: EquipmentManager         # 装备管理
    - dungeon_manager: DungeonManager             # 副本管理
    - challenge_tower: ChallengeTower             # 挑战塔
    - current_challenge: Challenge     # 当前挑战
    - current_monster: Any             # 当前战斗怪物
```

### 3. 玩家系统 (player.py)

**职责**: 玩家数据和行为

**核心类**:
- `Player`: 玩家角色数据类
- `CultivationLevel`: 修炼境界枚举
- `Sect`: 门派枚举
- `Achievement`: 成就系统

**数据模型**:
```python
@dataclass
class Player:
    # 基础信息
    name, sect, level, experience
    cultivation: CultivationLevel
    
    # 游戏进度
    kubectl_commands_mastered: List[str]
    challenges_completed: List[str]
    current_chapter: str
    
    # 战斗属性
    health, max_health, attack, defense
    
    # 装备系统
    equipped_weapon, equipped_armor, equipped_accessory
    inventory: List[Equipment]
    
    # 扩展系统数据
    skill_manager_data, talent_tree_data
    dungeon_manager_data, tower_progress_data
    
    # 体力系统
    stamina, max_stamina
```

### 4. 装备系统 (equipment.py)

**职责**: 装备生成、管理和强化

**核心类**:
- `Equipment`: 装备数据
- `EquipmentType`: 装备类型枚举（武器/护甲/饰品）
- `EquipmentQuality`: 装备品质枚举（普通~传说）
- `EquipmentManager`: 装备管理器

**关键特性**:
- 24件预设装备模板
- 5级品质系统
- 装备强化（最高+9）
- 掉落概率算法

### 5. 技能系统 (skills.py)

**职责**: 门派技能管理

**核心类**:
- `Skill`: 技能数据
- `SkillType`: 技能类型枚举
- `SkillManager`: 技能管理器

**设计特点**:
- 12个技能（4门派 × 3技能）
- 冷却时间机制
- 被动/主动技能分类
- 效果持续时间和叠加

### 6. 天赋系统 (talent_tree.py)

**职责**: 角色长期成长

**核心类**:
- `Talent`: 天赋节点
- `TalentBranch`: 天赋分支枚举
- `TalentTree`: 天赋树管理

**结构**:
- 3个分支：攻击/防御/辅助
- 3个层级，每层需要前置投入
- 每级获得1点天赋点

### 7. 副本系统 (dungeon.py)

**职责**: 每日副本挑战

**核心类**:
- `Dungeon`: 副本数据
- `DungeonType`: 副本类型枚举
- `DungeonRun`: 副本进行状态
- `DungeonManager`: 副本管理器

**副本类型**:
- 修炼秘境（经验）
- 藏宝洞窟（装备）
- 绝境试炼（极限挑战）

### 8. 挑战塔系统 (tower.py)

**职责**: 100层无尽挑战

**核心类**:
- `TowerLevel`: 层数数据
- `TowerProgress`: 玩家进度
- `ChallengeTower`: 挑战塔管理

**特点**:
- 100层渐进难度
- BOSS层（每10层）
- 排名系统
- 奖励递增

### 9. 故事系统 (story.py)

**职责**: 剧情内容和章节管理

**核心类**:
- `StoryManager`: 故事管理器
- `StoryChapter`: 章节数据
- `Chapter`: 章节枚举
- `Character`: NPC角色
- `Monster`: 怪物数据

### 10. 命令系统 (kubernetes_commands.py)

**职责**: Kubernetes命令数据和管理

**核心类**:
- `KubernetesCommandManager`: 命令管理器
- `KubectlCommand`: 命令数据
- `CommandCategory`: 命令分类枚举

**数据**:
- 90+ Kubernetes命令
- 12个功能分类
- 难度评级（1-5星）

## 数据流

### 战斗流程

```
1. 玩家选择挑战
   CLI.do_challenge()
   ↓
2. 生成挑战
   GameEngine.generate_challenge()
   ↓
3. 显示题目
   CLI 展示问题和选项
   ↓
4. 玩家回答
   CLI 接收输入
   ↓
5. 验证答案
   GameEngine.check_answer()
   ↓
6. 更新状态
   Player 更新经验/连击
   Equipment 处理掉落
   ↓
7. 显示结果
   CLI 展示反馈
```

### 装备获取流程

```
1. 战斗胜利
   GameEngine._handle_combat_victory()
   ↓
2. 触发掉落
   GameEngine.handle_equipment_drop()
   ↓
3. 生成装备
   EquipmentManager.generate_drop()
   ↓
4. 确定品质
   _calculate_quality() 基于玩家等级
   ↓
5. 选择模板
   从 EQUIPMENT_TEMPLATES 选择
   ↓
6. 创建装备
   Equipment.__init__()
   ↓
7. 加入背包
   Player.add_to_inventory()
```

## 存档格式

```json
{
  "name": "玩家名称",
  "sect": "青云宗",
  "level": 25,
  "experience": 5000,
  "cultivation": "筑基期",
  
  "kubectl_commands_mastered": ["kubectl run", "kubectl get pods"],
  "challenges_completed": ["challenge_1"],
  "current_chapter": "第一章",
  
  "health": 100,
  "max_health": 100,
  "attack": 15,
  "defense": 8,
  
  "equipped_weapon": {...},
  "equipped_armor": {...},
  "equipped_accessory": {...},
  "inventory": [...],
  
  "skill_manager_data": {...},
  "talent_tree_data": {...},
  "dungeon_manager_data": {...},
  "tower_progress_data": {...},
  
  "stamina": 85,
  "max_stamina": 100,
  "last_stamina_refresh": "2026-04-01T12:00:00"
}
```

## 扩展性设计

### 添加新系统

1. **创建模块文件**: `new_system.py`
2. **定义数据类**: 使用 `@dataclass`
3. **实现管理器类**: 处理业务逻辑
4. **集成到引擎**: 在 `GameEngine` 中初始化
5. **添加 CLI 界面**: 在 `cli.py` 中添加菜单
6. **更新存档**: 在 `Player` 中添加数据字段

### 扩展现有系统

以添加新装备为例：

1. 在 `EQUIPMENT_TEMPLATES` 中添加模板
2. 无需修改其他代码，系统自动支持

## 性能考虑

1. **装备计算**: 使用 `@property` 缓存计算结果
2. **存档加载**: 延迟初始化大型数据结构
3. **命令查询**: 使用字典存储，O(1) 查找
4. **战斗计算**: 避免重复的属性计算

## 安全考虑

1. **存档验证**: 加载时检查必要字段
2. **数值校验**: 防止负数/超界值
3. **作弊防范**: 关键计算在服务端（单机版不适用）

## 测试策略

- **单元测试**: 每个模块独立测试
- **集成测试**: 测试模块间交互
- **存档测试**: 验证存档/加载的完整性
- **边界测试**: 测试极限值处理

## 相关文档

- [装备系统](./systems/equipment.md)
- [技能系统](./systems/skills.md)
- [天赋系统](./systems/talent_tree.md)
- [副本系统](./systems/dungeon.md)
- [挑战塔系统](./systems/tower.md)
- [玩家指南](./player-guide.md)
- [开发指南](./development.md)
