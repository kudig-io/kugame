# 天赋系统文档

## 概述

天赋系统为玩家提供长期的角色成长路线。每个门派拥有独立的天赋树，分为攻击、防御、辅助三个分支，玩家通过升级获得天赋点，自由分配以强化角色。

## 核心概念

### 天赋分支

| 分支 | 说明 | 适合玩家 |
|-----|------|---------|
| 攻击 | 提升攻击力、暴击率等输出属性 | 喜欢主动进攻的玩家 |
| 防御 | 提升防御力、生命值等生存属性 | 喜欢稳健打法的玩家 |
| 辅助 | 提升经验获取、掉落率等功能属性 | 喜欢效率升级的玩家 |

### 天赋层级

每个分支有 3 个层级，高等级天赋需要前置投入：

- **Tier 1**：基础天赋，可直接投入
- **Tier 2**：进阶天赋，需要 Tier 1 投入 3 点解锁
- **Tier 3**：终极天赋，需要 Tier 1+2 投入 6 点解锁

## 门派天赋树

### 青云宗

**攻击分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 剑气初成 | 1 | 5 | 攻击力+2/级 |
| 剑意通明 | 2 | 3 | 攻击力+4/级 |
| 剑道通神 | 3 | 1 | 攻击力+8/级 |

**防御分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 气沉丹田 | 1 | 5 | 防御力+2/级 |
| 金刚不坏 | 2 | 3 | 防御力+4/级 |
| 万法不侵 | 3 | 1 | 受到伤害-10%/级 |

**辅助分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 悟道 | 1 | 5 | 经验获取+5%/级 |
| 心法 | 2 | 3 | 连击加成+5%/级 |
| 天人合一 | 3 | 1 | 全属性+10% |

### 炼狱门

**攻击分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 嗜血 | 1 | 5 | 攻击力+3/级 |
| 狂暴 | 2 | 3 | 暴击率+5%/级 |
| 血祭 | 3 | 1 | 攻击力+15%，但每回合损失5%生命 |

**防御分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 铁骨 | 1 | 5 | 防御力+3/级 |
| 不屈 | 2 | 3 | 生命值+10/级 |
| 浴血 | 3 | 1 | 生命低于30%时防御翻倍 |

**辅助分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 掠夺 | 1 | 5 | 战斗经验+8%/级 |
| 威慑 | 2 | 3 | 敌人攻击力-5%/级 |
| 战神 | 3 | 1 | 战斗开始时攻击力+50%，持续3回合 |

### 玄天宗

**攻击分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 灵动 | 1 | 5 | 攻击力+2/级，闪避+2%/级 |
| 幻影 | 2 | 3 | 攻击时有20%概率造成2倍伤害 |
| 瞬杀 | 3 | 1 | 闪避后下一次攻击必暴击 |

**防御分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 轻身 | 1 | 5 | 防御力+1/级，闪避+3%/级 |
| 虚无 | 2 | 3 | 有15%概率完全闪避攻击 |
| 不灭 | 3 | 1 | 受到致命伤害时有50%概率保留1点生命 |

**辅助分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 推演 | 1 | 5 | 答题时间+3秒/级 |
| 洞察 | 2 | 3 | 错误选项有20%概率被标记 |
| 预知 | 3 | 1 | 每5道题可以查看正确答案 |

### 逍遥派

**攻击分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 随性 | 1 | 5 | 攻击力+1~3/级（随机） |
| 逍遥 | 2 | 3 | 每次攻击附加当前经验值1%的伤害 |
| 破天 | 3 | 1 | 有5%概率一击必杀（对BOSS无效） |

**防御分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 自在 | 1 | 5 | 防御力+1~3/级（随机） |
| 逍遥游 | 2 | 3 | 逃跑成功率+15%/级 |
| 无我 | 3 | 1 | 每回合恢复5%生命值 |

**辅助分支**：
| 天赋 | 层级 | 最大点数 | 效果 |
|-----|------|---------|------|
| 机缘 | 1 | 5 | 装备掉落率+10%/级 |
| 造化 | 2 | 3 | 商店价格-10%/级 |
| 超脱 | 3 | 1 | 每升1级额外获得1点天赋点 |

## 系统架构

### 类图

```
Talent
├── id: str
├── name: str
├── description: str
├── branch: TalentBranch
├── tier: int
├── max_points: int
├── current_points: int
├── effect_per_point: float
├── total_effect(): float
├── can_add_point(): bool
└── add_point(): bool

TalentTree
├── sect: Sect
├── talents: Dict[str, Talent]
├── available_points: int
├── _initialize_talents(): void
├── get_talent(): Optional[Talent]
├── get_branch_talents(): List[Talent]
├── add_talent_point(): Dict[str, Any]
├── get_total_bonus(): float
└── on_level_up(): void
```

## 使用指南

### 1. 创建天赋树

```python
from kugame.talent_tree import TalentTree, TalentBranch, Sect

# 创建天赋树
tree = TalentTree(sect=Sect.青云宗)

# 查看天赋点
print(f"可用天赋点: {tree.available_points}")
```

### 2. 获取天赋信息

```python
# 获取所有天赋
all_talents = tree.talents.values()

# 获取指定分支天赋
attack_talents = tree.get_branch_talents(TalentBranch.攻击)

# 获取特定天赋
talent = tree.get_talent("qy_atk_1")
print(f"{talent.name}: 当前{talent.current_points}/{talent.max_points}级")
```

### 3. 投入天赋点

```python
# 尝试加点
result = tree.add_talent_point("qy_atk_1")
if result["success"]:
    print(f"✓ {result['message']}")
    print(f"剩余天赋点: {result['remaining_points']}")
else:
    print(f"✗ {result['message']}")
```

### 4. 升级获得天赋点

```python
# 玩家升级时调用
tree.on_level_up()
print(f"获得1点天赋点！")

# 逍遥派超脱天赋额外获得
if tree.sect == Sect.逍遥派:
    talent = tree.get_talent("xy_sup_3")
    if talent and talent.current_points > 0:
        tree.on_level_up()  # 额外获得1点
```

### 5. 计算属性加成

```python
# 获取攻击加成
attack_bonus = tree.get_total_bonus("atk")

# 获取防御加成
defense_bonus = tree.get_total_bonus("def")

# 获取经验加成
exp_bonus = tree.get_total_bonus("exp")
```

## 天赋模板定义

天赋定义在 `TALENT_TEMPLATES` 中：

```python
TALENT_TEMPLATES = {
    Sect.青云宗: {
        TalentBranch.攻击: [
            Talent("qy_atk_1", "剑气初成", "攻击力+2/级", 
                   TalentBranch.攻击, 1, 5, 0, 2),
            Talent("qy_atk_2", "剑意通明", "攻击力+4/级", 
                   TalentBranch.攻击, 2, 3, 0, 4),
            Talent("qy_atk_3", "剑道通神", "攻击力+8/级", 
                   TalentBranch.攻击, 3, 1, 0, 8),
        ],
        # ... 其他分支
    },
}
```

## 解锁机制

### 前置条件检查

```python
def add_talent_point(self, talent_id: str) -> Dict[str, Any]:
    talent = self.get_talent(talent_id)
    
    # 检查前置条件
    if talent.tier > 1:
        lower_tier_points = sum(
            t.current_points for t in self.get_branch_talents(talent.branch)
            if t.tier < talent.tier
        )
        required_points = (talent.tier - 1) * 3
        
        if lower_tier_points < required_points:
            return {
                "success": False,
                "message": f"需要先在前置天赋投入{required_points}点"
            }
```

## 与玩家系统的集成

Player 类通过 `talent_tree_data` 存储天赋数据：

```python
class Player:
    talent_tree_data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            # ... 其他数据
            "talent_tree_data": self.talent_tree.to_dict() if self.talent_tree else None,
        }
```

## 存档格式

```json
{
  "talent_tree_data": {
    "sect": "青云宗",
    "talents": {
      "qy_atk_1": {
        "id": "qy_atk_1",
        "name": "剑气初成",
        "current_points": 3,
        "max_points": 5
      },
      "qy_atk_2": {
        "current_points": 1
      }
    },
    "available_points": 2
  }
}
```

## 扩展指南

### 添加新天赋

1. 在 `TALENT_TEMPLATES` 中添加：

```python
TALENT_TEMPLATES = {
    Sect.青云宗: {
        TalentBranch.攻击: [
            # 现有天赋...
            Talent(
                id="qy_atk_new",
                name="新天赋名称",
                description="天赋效果描述",
                branch=TalentBranch.攻击,
                tier=2,  # 层级
                max_points=3,
                current_points=0,
                effect_per_point=5.0,
            ),
        ],
    },
}
```

2. 在玩家属性计算中应用新天赋效果

### 自定义天赋效果

```python
class Talent:
    def apply_custom_effect(self, player) -> Dict[str, Any]:
        """应用自定义效果"""
        if self.id == "custom_talent":
            return {
                "bonus_attack": self.total_effect,
                "special_ability": "unlocked" if self.current_points > 0 else None
            }
        return {}
```

## 平衡性建议

1. **天赋点获取**：每升1级获得1点，满级100级共100点
2. **单天赋投入**：Tier 1 最多5点，Tier 2 最多3点，Tier 3 最多1点
3. **满级收益**：单分支满级（9点）应提供约50%的属性提升
4. **多分支**：鼓励玩家分散投入，而非单一点满

## 注意事项

1. **存档兼容**：新增天赋需处理旧存档缺失数据的情况
2. **重置功能**：考虑是否提供天赋重置功能（消耗道具/经验）
3. **效果计算**：天赋效果应在装备加成之后应用
4. **性能优化**：避免频繁计算天赋总加成，可以缓存结果

## 相关文档

- [装备系统](./equipment.md)
- [技能系统](./skills.md)
- [副本系统](./dungeon.md)
- [玩家指南](../player-guide.md)
