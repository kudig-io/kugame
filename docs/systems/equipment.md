# 装备系统文档

## 概述

装备系统是 KuGame 的核心成长系统之一，玩家通过战斗、商店购买等方式获取装备，提升角色属性，增强战斗力。

## 核心概念

### 装备类型

| 类型 | 英文 | 主属性 | 说明 |
|-----|------|-------|------|
| 武器 | `weapon` | 攻击力 | 提升角色的攻击伤害 |
| 护甲 | `armor` | 防御力、生命值 | 提升生存能力 |
| 饰品 | `accessory` | 综合属性 | 提供经验加成、连击加成等特殊效果 |

### 装备品质

品质由低到高，属性加成依次提升：

| 品质 | 颜色 | 属性倍率 | 最高强化等级 |
|-----|------|---------|-------------|
| 普通 | 白色 | 1.0x | +5 |
| 精良 | 绿色 | 1.3x | +6 |
| 稀有 | 蓝色 | 1.6x | +7 |
| 史诗 | 紫色 | 2.0x | +8 |
| 传说 | 橙色 | 2.5x | +9 |

### 装备属性

基础属性：
- `attack_bonus`: 攻击加成
- `defense_bonus`: 防御加成
- `health_bonus`: 生命值加成

特殊属性：
- `exp_bonus`: 经验值加成百分比
- `streak_bonus`: 连击加成百分比

## 系统架构

### 类图

```
Equipment
├── id: str
├── name: str
├── equipment_type: EquipmentType
├── quality: EquipmentQuality
├── level: int
├── attack_bonus: int
├── defense_bonus: int
├── health_bonus: int
├── exp_bonus: float
├── streak_bonus: float
├── description: str
├── equipped: bool
├── total_attack(): int
├── total_defense(): int
├── total_health(): int
├── display_name(): str
├── upgrade(): bool
└── get_upgrade_cost(): int

EquipmentManager
├── equipment_counter: int
├── _generate_equipment_id(): str
├── generate_equipment(): Equipment
├── _calculate_quality(): EquipmentQuality
├── generate_drop(): Optional[Equipment]
├── get_shop_equipment(): List[Equipment]
├── _calculate_shop_quality(): EquipmentQuality
├── calculate_sell_price(): int
└── calculate_buy_price(): int
```

## 使用指南

### 1. 生成装备

```python
from kugame.equipment import EquipmentManager, EquipmentType, EquipmentQuality

manager = EquipmentManager()

# 随机生成装备
equipment = manager.generate_equipment(player_level=10)

# 指定类型和品质
equipment = manager.generate_equipment(
    equipment_type=EquipmentType.武器,
    quality=EquipmentQuality.史诗,
    player_level=20
)
```

### 2. 装备掉落

```python
# 战斗胜利后调用
equipment = manager.generate_drop(monster_level=5, player_level=10)
if equipment:
    print(f"掉落装备: {equipment.display_name}")
```

### 3. 商店购买

```python
# 获取商店物品列表
shop_items = manager.get_shop_equipment(player_level=15)

# 计算价格
buy_price = manager.calculate_buy_price(equipment)
sell_price = manager.calculate_sell_price(equipment)
```

### 4. 装备强化

```python
# 强化装备
success = equipment.upgrade()
if success:
    print(f"强化成功！当前等级: +{equipment.level - 1}")
    print(f"升级费用: {equipment.get_upgrade_cost()} 经验值")
```

## 装备模板

系统内置了 24 件装备模板（每种类型 8 件）：

### 武器列表

| 名称 | 基础攻击 | 特殊效果 |
|-----|---------|---------|
| 木剑 | 5 | 无 |
| 铁剑 | 10 | 无 |
| 精钢剑 | 15 | 无 |
| 青云剑 | 20 | 经验+5% |
| 玄铁重剑 | 25 | 防御+5 |
| 赤焰刀 | 30 | 连击+10% |
| 龙吟剑 | 40 | 生命+10, 经验+10% |
| 诛仙剑 | 60 | 经验+15%, 连击+10% |

### 护甲列表

| 名称 | 基础防御 | 基础生命 | 特殊效果 |
|-----|---------|---------|---------|
| 布衣 | 3 | 10 | 无 |
| 皮甲 | 6 | 20 | 无 |
| 铁甲 | 10 | 30 | 无 |
| 精钢甲 | 15 | 50 | 无 |
| 玄天战甲 | 20 | 80 | 经验+5% |
| 金刚护体 | 30 | 100 | 无 |
| 龙鳞甲 | 40 | 150 | 经验+8% |
| 不朽金身 | 50 | 200 | 经验+10% |

### 饰品列表

| 名称 | 属性加成 | 特殊效果 |
|-----|---------|---------|
| 木戒指 | 生命+5 | 经验+2% |
| 铁护符 | 攻击+2, 防御+2 | 无 |
| 玉佩 | 生命+20 | 经验+5% |
| 灵珠 | 攻击+3, 生命+15 | 经验+8%, 连击+5% |
| 乾坤戒 | 攻击+5, 防御+5, 生命+30 | 经验+10% |
| 聚灵项链 | 生命+25 | 经验+15%, 连击+5% |
| 龙魂玉 | 攻击+8, 防御+8, 生命+50 | 经验+12%, 连击+8% |
| 混沌至宝 | 攻击+15, 防御+15, 生命+100 | 经验+20%, 连击+15% |

## 品质掉落概率

掉落概率随玩家等级提升而优化：

```
普通装备: 基础概率 50% - 等级加成
精良装备: 基础概率 30% + 等级加成 * 0.5
稀有装备: 基础概率 15% + 等级加成 * 0.3
史诗装备: 基础概率 4% + 等级加成 * 0.1
传说装备: 基础概率 1% + 等级加成 * 0.05
```

## 强化成本

强化消耗经验值，公式为：

```
基础成本 = 100 × 品质等级
等级倍率 = 1.5 ^ (当前等级 - 1)
总成本 = 基础成本 × 等级倍率
```

### 强化成本示例

| 品质 | +1 | +2 | +3 | +4 | +5 |
|-----|----|----|----|----|----|
| 普通 | 100 | 150 | 225 | 337 | 506 |
| 精良 | 200 | 300 | 450 | 675 | 1012 |
| 稀有 | 300 | 450 | 675 | 1012 | 1518 |
| 史诗 | 400 | 600 | 900 | 1350 | 2025 |
| 传说 | 500 | 750 | 1125 | 1687 | 2531 |

## 与玩家系统的集成

Player 类通过以下方式集成装备系统：

```python
class Player:
    equipped_weapon: Optional[Equipment]
    equipped_armor: Optional[Equipment]
    equipped_accessory: Optional[Equipment]
    inventory: List[Equipment]
    
    @property
    def total_attack(self) -> int:
        # 基础攻击 + 武器攻击 + 饰品攻击
        
    @property
    def total_defense(self) -> int:
        # 基础防御 + 护甲防御 + 饰品防御
        
    @property
    def total_max_health(self) -> int:
        # 基础生命 + 护甲生命 + 饰品生命
```

## 存档格式

装备数据在存档中的格式：

```json
{
  "equipped_weapon": {
    "id": "eq_1_1234",
    "name": "青云剑",
    "equipment_type": "weapon",
    "quality": "稀有",
    "level": 3,
    "attack_bonus": 20,
    "defense_bonus": 0,
    "health_bonus": 0,
    "exp_bonus": 0.05,
    "streak_bonus": 0,
    "equipped": true
  },
  "inventory": [...]
}
```

## 扩展指南

### 添加新装备

在 `EQUIPMENT_TEMPLATES` 中添加新条目：

```python
EquipmentType.武器: [
    {
        "name": "新武器名称",
        "attack": 攻击值,
        "defense": 防御值,
        "health": 生命值,
        "exp": 经验加成,
        "streak": 连击加成
    },
]
```

### 自定义装备效果

可以扩展 `Equipment` 类添加特殊效果：

```python
class Equipment:
    # 添加新属性
    special_effect: str = ""
    
    def apply_special_effect(self, context: Dict) -> Dict:
        # 实现特殊效果逻辑
        pass
```

## 注意事项

1. **平衡性**：装备属性直接影响战斗平衡，调整数值需谨慎
2. **存储空间**：大量装备会占用存档空间，建议限制背包容量
3. **性能**：装备计算在战斗中频繁调用，避免复杂计算
4. **兼容性**：新增装备属性需考虑存档兼容性

## 相关文档

- [技能系统](./skills.md)
- [天赋系统](./talent_tree.md)
- [副本系统](./dungeon.md)
- [挑战塔系统](./tower.md)
