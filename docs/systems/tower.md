# 挑战塔系统文档

## 概述

挑战塔是 KuGame 的终极挑战内容，共100层，每层都有强大的守卫。玩家需要逐层挑战，证明自己的实力。挑战塔提供丰厚的奖励和独特的排名系统。

## 核心概念

### 挑战塔结构

- **总层数**：100层
- **BOSS层**：每10层（10, 20, 30...100）
- **难度递增**：每层怪物属性逐步提升
- **排名系统**：根据最高通关层数排名

### 挑战规则

1. **逐层挑战**：必须从第1层开始，不能跳过
2. **记录最高层**：自动记录最高通关层数
3. **可重复挑战**：已通关层可以重新挑战
4. **奖励递增**：高层奖励更丰厚

## 怪物属性

### 普通层怪物

属性随层数线性增长：

```
生命值 = 50 + 层数 × 8
攻击力 = 5 + 层数 × 1.5
防御力 = 2 + 层数 × 0.5
经验奖励 = 100 + 层数 × 20
```

### BOSS层怪物（每10层）

属性大幅提升：

```
生命值 = 基础值 × 2.5
攻击力 = 基础值 × 2
防御力 = 基础值 × 2
经验奖励 = 500 + 层数 × 50
装备品质 = 随层数提升
```

## 层数详情

### 1-10层（凡人区）

| 层数 | 怪物名称 | 推荐境界 | 经验奖励 |
|-----|---------|---------|---------|
| 1-9 | Pod傀儡 | 凡人 | 120-280 |
| 10 | Pod之王 | 凡人 | 1000 |

### 11-20层（练气期区）

| 层数 | 怪物名称 | 推荐境界 | 经验奖励 |
|-----|---------|---------|---------|
| 11-19 | Service幽灵 | 练气期 | 320-500 |
| 20 | Service女王 | 练气期 | 1500 |

### 21-30层（筑基期区）

| 层数 | 怪物名称 | 推荐境界 | 经验奖励 |
|-----|---------|---------|---------|
| 21-29 | Deployment巨兽 | 筑基期 | 520-700 |
| 30 | Deployment霸主 | 筑基期 | 2000 |

### 后续区域

| 层数 | 区域 | 推荐境界 |
|-----|------|---------|
| 31-40 | 金丹期区 | 金丹期 |
| 41-50 | 元婴期区 | 元婴期 |
| 51-60 | 化神期区 | 化神期 |
| 61-70 | 大乘期区 | 大乘期 |
| 71-80 | 渡劫期区 | 渡劫期 |
| 81-90 | 散仙区 | 散仙 |
| 91-100 | 金仙区 | 金仙 |

## 排名系统

根据最高通关层数，玩家获得不同称号：

| 层数 | 称号 | 颜色 |
|-----|------|------|
| 100 | 🏆 通天塔主 | 金色 |
| 90-99 | 🥇 塔之王者 | 橙色 |
| 80-89 | 🥈 塔之大师 | 紫色 |
| 60-79 | 🥉 塔之勇士 | 蓝色 |
| 40-59 | ⭐ 塔之先锋 | 绿色 |
| 20-39 | ✨ 塔之新秀 | 白色 |
| 1-19 | 💫 初入塔门 | 灰色 |

## 系统架构

### 类图

```
TowerLevel
├── level: int
├── monster_name: str
├── monster_health: int
├── monster_attack: int
├── monster_defense: int
├── experience_reward: int
├── equipment_quality: int
├── recommended_cultivation: int
├── clear_bonus: float
├── create_monster(): Monster
├── to_dict(): Dict[str, Any]
└── from_dict(): TowerLevel

TowerProgress
├── highest_level: int
├── current_level: int
├── total_attempts: int
├── total_clears: int
├── to_dict(): Dict[str, Any]
└── from_dict(): TowerProgress

ChallengeTower
├── levels: List[TowerLevel]
├── current_run: Optional[TowerLevel]
├── get_level(): Optional[TowerLevel]
├── start_challenge(): Dict[str, Any]
├── complete_level(): Dict[str, Any]
├── get_ranking(): str
└── get_level_status(): str
```

## 使用指南

### 1. 初始化挑战塔

```python
from kugame.tower import ChallengeTower, TowerProgress

# 创建挑战塔
tower = ChallengeTower()

# 初始化玩家进度
progress = TowerProgress()
print(f"最高通关: {progress.highest_level}")
```

### 2. 获取层数信息

```python
# 获取指定层信息
level_info = tower.get_level(50)
print(f"第50层守卫: {level_info.monster_name}")
print(f"推荐境界: {level_info.recommended_cultivation}")
print(f"经验奖励: {level_info.experience_reward}")
```

### 3. 开始挑战

```python
# 挑战第51层（最高通关+1）
result = tower.start_challenge(51, progress)

if result["success"]:
    print(f"开始挑战！{result['message']}")
    monster = result["monster"]
    print(f"遭遇: {monster.name}")
    print(f"生命值: {monster.health}")
else:
    print(f"无法挑战: {result['message']}")
```

### 4. 完成挑战

```python
# 战斗胜利后
result = tower.complete_level(progress)

if result["success"]:
    print(f"🎉 {result['message']}")
    rewards = result["rewards"]
    print(f"获得经验: {rewards['experience']}")
    
    if "equipment_dropped" in result:
        eq = result["equipment_dropped"]
        print(f"掉落装备: [{eq['quality']}]{eq['name']}")
    
    if rewards.get("is_new_record"):
        print("⭐ 新纪录！")
```

### 5. 查看排名

```python
# 获取当前排名
ranking = tower.get_ranking(progress)
print(f"当前排名: {ranking}")

# 查看附近层数状态
for level in range(45, 56):
    info = engine.get_tower_level(level)
    if info:
        print(f"第{level}层: {info['status']}")
```

## 奖励机制

### 经验奖励

基础经验 × 通关倍率：

```python
if is_boss_level:
    clear_bonus = 2.0
else:
    clear_bonus = 1.0

total_exp = level.experience_reward * clear_bonus
```

### 装备奖励

| 层数范围 | 装备品质 |
|---------|---------|
| 1-25 | 普通 ~ 精良 |
| 26-50 | 精良 ~ 稀有 |
| 51-75 | 稀有 ~ 史诗 |
| 76-100 | 史诗 ~ 传说 |

BOSS层额外提升装备品质。

### 首通奖励

首次通关某层时，获得额外奖励：

```python
if level > previous_highest:
    bonus_exp = level * 10
    print(f"首通奖励: {bonus_exp} 经验值！")
```

## 与玩家系统的集成

Player 类存储挑战塔进度：

```python
class Player:
    tower_progress_data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            # ... 其他数据
            "tower_progress_data": self.tower_progress.to_dict() if self.tower_progress else None,
        }
```

## 存档格式

```json
{
  "tower_progress_data": {
    "highest_level": 42,
    "current_level": 43,
    "total_attempts": 56,
    "total_clears": 42
  }
}
```

## 怪物名称列表

系统内置了12种怪物名称：

1. Pod傀儡
2. Service幽灵
3. Deployment巨兽
4. ConfigMap守护者
5. Secret潜伏者
6. Volume吞噬者
7. Namespace领主
8. Node支配者
9. Cluster核心
10. Ingress看门人
11. Scheduler裁决者
12. Controller管理者

BOSS名称（每10层）：

1. Pod之王
2. Service女王
3. Deployment霸主
4. ConfigMap贤者
5. Secret魔王
6. Volume巨龙
7. Namespace主宰
8. Node泰坦
9. Cluster之神
10. Ingress天尊

## 扩展指南

### 添加更多层数

修改 `generate_tower_levels` 函数：

```python
def generate_tower_levels(total_levels: int = 200):  # 改为200层
    levels = []
    for i in range(1, total_levels + 1):
        # 现有逻辑...
    return levels
```

### 自定义层数属性

```python
# 添加特殊层
special_level = TowerLevel(
    level=50,
    monster_name="特殊守卫",
    monster_health=10000,
    monster_attack=200,
    monster_defense=50,
    experience_reward=10000,
    equipment_quality=5,  # 传说
    recommended_cultivation=5,
    clear_bonus=3.0,  # 3倍奖励
)
```

### 添加新的排名等级

```python
def get_ranking(self, progress: TowerProgress) -> str:
    level = progress.highest_level
    
    if level >= 150:
        return "👑 塔之神明"  # 新增等级
    # ... 现有等级
```

## 平衡性建议

1. **难度曲线**：每10层难度应该有明显提升
2. **奖励递增**：高层奖励应显著优于低层
3. **境界匹配**：推荐境界应与实际难度匹配
4. **BOSS强度**：BOSS应该是该区域的巅峰挑战

## 注意事项

1. **存档安全**：挑战塔进度是重要的玩家数据，需确保存档可靠
2. **作弊防范**：最高层数验证应在服务端完成
3. **性能优化**：100层数据预生成，避免实时计算
4. **界面展示**：高层可能需要滚动查看，考虑分页

## 未来扩展

1. **赛季系统**：定期重置挑战塔，提供赛季奖励
2. **排行榜**：全服排行榜，展示顶尖玩家
3. **组队挑战**：多人协作挑战高层
4. **特殊事件**：限时开放特殊层数，奖励翻倍

## 相关文档

- [装备系统](./equipment.md)
- [技能系统](./skills.md)
- [副本系统](./dungeon.md)
- [玩家指南](../player-guide.md)
