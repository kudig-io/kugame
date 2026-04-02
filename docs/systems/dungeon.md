# 副本系统文档

## 概述

副本系统提供每日可挑战的特殊关卡，包括经验副本、装备副本和极限挑战三种类型。副本消耗体力，奖励丰厚，是玩家获取资源的重要途径。

## 核心概念

### 副本类型

| 类型 | 名称 | 体力消耗 | 主要奖励 | 推荐等级 |
|-----|------|---------|---------|---------|
| 经验副本 | 修炼秘境 | 10 | 大量经验值 | 10+ |
| 装备副本 | 藏宝洞窟 | 15 | 高品质装备 | 20+ |
| 极限挑战 | 绝境试炼 | 20 | 稀有装备+大量经验 | 40+ |

### 体力系统

- **最大体力**：100点
- **恢复速度**：每6分钟恢复1点
- **恢复上限**：达到最大值后停止恢复
- **用途**：挑战副本消耗

## 每日副本详情

### 修炼秘境（经验副本）

**描述**：灵气充沛的修炼圣地，可获得大量经验

**属性**：
- 推荐等级：10
- 体力消耗：10
- 经验奖励：1000
- 难度倍率：1.0

**特点**：
- 最适合新手玩家
- 经验收益稳定
- 难度较低

### 藏宝洞窟（装备副本）

**描述**：藏有上古神器的洞窟，可获得高品质装备

**属性**：
- 推荐等级：20
- 体力消耗：15
- 经验奖励：500
- 装备品质：稀有起步
- 难度倍率：1.3

**特点**：
- 装备掉落品质高
- 经验收益较低
- 需要一定实力

### 绝境试炼（极限挑战）

**描述**：只有真正的强者才能通过的试炼

**属性**：
- 推荐等级：40
- 体力消耗：20
- 经验奖励：2000
- 装备品质：史诗起步
- 难度倍率：2.0

**特点**：
- 最高难度
- 最丰厚奖励
- 适合挑战自我

## 系统架构

### 类图

```
Dungeon
├── id: str
├── name: str
├── dungeon_type: DungeonType
├── description: str
├── recommended_level: int
├── stamina_cost: int
├── reward_exp: int
├── reward_equipment_quality: int
├── difficulty_multiplier: float
├── completed: bool
├── to_dict(): Dict[str, Any]
└── from_dict(): Dungeon

DungeonRun
├── dungeon: Dungeon
├── current_wave: int
├── total_waves: int
├── monsters_defeated: int
├── is_complete(): bool
├── next_wave(): Optional[Monster]
└── get_final_reward(): Dict[str, Any]

DungeonManager
├── daily_dungeons: List[Dungeon]
├── last_refresh: Optional[datetime]
├── current_run: Optional[DungeonRun]
├── _refresh_daily_dungeons(): void
├── get_available_dungeons(): List[Dungeon]
├── start_dungeon(): Dict[str, Any]
├── get_next_monster(): Optional[Monster]
├── complete_dungeon(): Dict[str, Any]
├── to_dict(): Dict[str, Any]
└── from_dict(): DungeonManager
```

## 使用指南

### 1. 初始化副本管理器

```python
from kugame.dungeon import DungeonManager

# 创建副本管理器
dungeon_manager = DungeonManager()

# 会自动刷新每日副本
print(f"今日副本数量: {len(dungeon_manager.daily_dungeons)}")
```

### 2. 获取可用副本

```python
# 获取适合当前等级的副本
available = dungeon_manager.get_available_dungeons(player_level=25)

for dungeon in available:
    status = "已完成" if dungeon.completed else "可挑战"
    print(f"{dungeon.name} [{status}] - 消耗{dungeon.stamina_cost}体力")
```

### 3. 开始副本挑战

```python
# 开始指定副本
result = dungeon_manager.start_dungeon("exp_daily", player_stamina=80)

if result["success"]:
    print(f"进入副本: {result['message']}")
    print(f"扣除体力: {result['stamina_cost']}")
    dungeon_run = result["dungeon_run"]
else:
    print(f"无法进入: {result['message']}")
```

### 4. 副本战斗流程

```python
# 获取下一波怪物
while not dungeon_run.is_complete():
    monster = dungeon_manager.get_next_monster()
    if monster:
        print(f"遭遇: {monster.name}")
        # 进行战斗...
        # 战斗胜利后...

# 完成副本
result = dungeon_manager.complete_dungeon()
if result["success"]:
    rewards = result["rewards"]
    print(f"获得经验: {rewards['experience']}")
    print(f"装备品质: {rewards['equipment_quality']}")
```

## 副本配置

副本配置在 `DAILY_DUNGEONS` 列表中定义：

```python
DAILY_DUNGEONS = [
    Dungeon(
        id="exp_daily",
        name="修炼秘境",
        dungeon_type=DungeonType.经验副本,
        description="灵气充沛的修炼圣地",
        recommended_level=10,
        stamina_cost=10,
        reward_exp=1000,
        difficulty_multiplier=1.0,
    ),
    # ... 其他副本
]
```

## 刷新机制

### 自动刷新

副本每天凌晨 4:00 自动刷新：

```python
def _refresh_daily_dungeons(self) -> None:
    now = datetime.now()
    
    if self.last_refresh:
        last_date = self.last_refresh.date()
        current_date = now.date()
        
        # 检查是否需要刷新
        if last_date == current_date and now.hour >= 4:
            return  # 今天已刷新
    
    # 刷新所有副本
    for template in DAILY_DUNGEONS:
        dungeon = Dungeon.from_dict(template.to_dict())
        dungeon.completed = False
        self.daily_dungeons.append(dungeon)
    
    self.last_refresh = now
```

### 手动刷新

玩家可以消耗经验值手动刷新商店（相关功能），但副本每日自动刷新，不支持手动刷新。

## 难度计算

副本难度根据玩家等级和副本推荐等级计算：

```python
def calculate_difficulty(player_level: int, dungeon: Dungeon) -> float:
    level_diff = player_level - dungeon.recommended_level
    
    if level_diff >= 10:
        return 0.8  # 等级压制，难度降低
    elif level_diff >= 0:
        return 1.0  # 正常难度
    elif level_diff >= -10:
        return 1.3  # 略有难度
    else:
        return 2.0  # 极具挑战
```

## 奖励计算

### 经验奖励

```
基础经验 × 难度倍率 × 技能加成 × 装备加成
```

### 装备奖励

| 副本类型 | 最低品质 | 最高品质 |
|---------|---------|---------|
| 经验副本 | 普通 | 精良 |
| 装备副本 | 稀有 | 史诗 |
| 极限挑战 | 史诗 | 传说 |

## 与玩家系统的集成

Player 类存储副本数据：

```python
class Player:
    dungeon_manager_data: Optional[Dict[str, Any]] = None
    stamina: int = 100
    max_stamina: int = 100
    last_stamina_refresh: Optional[str] = None
```

### 体力恢复

```python
from datetime import datetime, timedelta

def recover_stamina(self) -> None:
    if not self.last_stamina_refresh:
        return
    
    last = datetime.fromisoformat(self.last_stamina_refresh)
    now = datetime.now()
    elapsed = (now - last).total_seconds()
    
    # 每6分钟恢复1点
    recovery = int(elapsed / 360)
    self.stamina = min(self.max_stamina, self.stamina + recovery)
    self.last_stamina_refresh = now.isoformat()
```

## 存档格式

```json
{
  "dungeon_manager_data": {
    "daily_dungeons": [
      {
        "id": "exp_daily",
        "name": "修炼秘境",
        "dungeon_type": "exp",
        "completed": false
      }
    ],
    "last_refresh": "2026-04-01T04:00:00"
  },
  "stamina": 85,
  "max_stamina": 100,
  "last_stamina_refresh": "2026-04-01T12:30:00"
}
```

## 扩展指南

### 添加新副本

在 `DAILY_DUNGEONS` 中添加：

```python
DAILY_DUNGEONS = [
    # 现有副本...
    Dungeon(
        id="new_dungeon",
        name="新副本名称",
        dungeon_type=DungeonType.经验副本,
        description="副本描述",
        recommended_level=30,
        stamina_cost=25,
        reward_exp=1500,
        reward_equipment_quality=3,
        difficulty_multiplier=1.5,
    ),
]
```

### 自定义副本机制

```python
class CustomDungeon(Dungeon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.special_rule = "特殊规则"
    
    def apply_special_rule(self, player) -> Dict[str, Any]:
        """应用特殊规则"""
        if self.special_rule == "限时":
            return {"time_limit": 300}  # 5分钟限时
        return {}
```

### 添加更多波次

```python
# 修改 DungeonRun 的 total_waves
class DungeonRun:
    def __init__(self, dungeon: Dungeon):
        self.dungeon = dungeon
        self.total_waves = 5  # 从3波改为5波
        # ...
```

## 平衡性建议

1. **体力消耗**：根据奖励价值设置合理消耗
2. **难度梯度**：确保高难度副本有相应的高回报
3. **每日限制**：通过体力限制每日收益上限
4. **等级适配**：副本推荐等级应略低于玩家当前等级

## 注意事项

1. **刷新时间**：确保刷新逻辑在服务器/客户端一致
2. **并发处理**：防止多次点击导致的体力重复扣除
3. **断线重连**：考虑副本进行中的断线恢复机制
4. **作弊防范**：关键计算应在服务端完成

## 相关文档

- [装备系统](./equipment.md)
- [技能系统](./skills.md)
- [挑战塔系统](./tower.md)
- [玩家指南](../player-guide.md)
