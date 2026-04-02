# 技能系统文档

## 概述

技能系统为每个门派提供独特的主动和被动技能，增强游戏的策略性和门派特色。每个门派拥有 3 个技能：1 个被动技能和 2 个主动技能。

## 核心概念

### 技能类型

| 类型 | 说明 | 示例 |
|-----|------|------|
| 攻击 | 提升伤害输出 | 狂暴、剑气 |
| 防御 | 减少受到伤害 | 减伤、闪避 |
| 恢复 | 恢复生命值 | 吸血、治疗 |
| 特殊 | 其他特殊效果 | 提示、逃跑 |

### 技能分类

- **被动技能**：无需手动触发，持续生效，冷却为 0
- **主动技能**：需要手动使用，有冷却时间，持续一定回合

## 门派技能详情

### 青云宗

| 技能 | 类型 | 冷却 | 效果 |
|-----|------|------|------|
| 稳如泰山 | 被动 | - | 受到的伤害减少 20% |
| 道法自然 | 主动 | 5回合 | 接下来3场战斗获得30%额外经验 |
| 以柔克刚 | 主动 | 4回合 | 反弹下一次受到的伤害 |

**门派特色**：稳健防守，经验获取

### 炼狱门

| 技能 | 类型 | 冷却 | 效果 |
|-----|------|------|------|
| 狂暴 | 主动 | 3回合 | 本回合攻击力翻倍 |
| 嗜血 | 被动 | - | 造成伤害的20%恢复为生命值 |
| 不屈 | 被动 | - | 死亡时有30%概率复活，恢复30%生命 |

**门派特色**：高风险高回报，生存能力

### 玄天宗

| 技能 | 类型 | 冷却 | 效果 |
|-----|------|------|------|
| 变化莫测 | 主动 | 4回合 | 接下来2回合有50%概率闪避攻击 |
| 天机洞察 | 主动 | 3回合 | 下一道题目的正确答案会高亮显示 |
| 乾坤挪移 | 主动 | 5回合 | 将下一次受到的伤害转移给怪物 |

**门派特色**：灵活多变，策略性强

### 逍遥派

| 技能 | 类型 | 冷却 | 效果 |
|-----|------|------|------|
| 逍遥游 | 被动 | - | 逃跑成功率提升至100% |
| 因材施教 | 被动 | - | 学习新命令时额外获得50%经验 |
| 随性而为 | 主动 | 3回合 | 随机获得攻击+50%/防御+50%/恢复30%生命/经验+50% |

**门派特色**：自由灵活，随机应变

## 系统架构

### 类图

```
Skill
├── id: str
├── name: str
├── description: str
├── sect: Sect
├── skill_type: SkillType
├── cooldown: int
├── effect_value: int
├── duration: int
├── mana_cost: int
├── current_cooldown: int
├── is_available(): bool
├── use(): bool
└── tick_cooldown(): void

SkillManager
├── sect: Sect
├── skills: Dict[str, Skill]
├── active_effects: Dict[str, Dict]
├── _initialize_skills(): void
├── get_skill(): Optional[Skill]
├── get_all_skills(): List[Skill]
├── use_skill(): Dict[str, Any]
├── tick_all_cooldowns(): void
├── has_active_effect(): bool
├── get_active_effects(): List[Dict]
└── apply_passive_effects(): Dict[str, Any]
```

## 使用指南

### 1. 初始化技能管理器

```python
from kugame.skills import SkillManager, Sect

# 为玩家创建技能管理器
skill_manager = SkillManager(sect=Sect.青云宗)

# 获取所有技能
skills = skill_manager.get_all_skills()
for skill in skills:
    print(f"{skill.name}: {skill.description}")
```

### 2. 使用技能

```python
# 使用技能
result = skill_manager.use_skill("qingyun_dao")
if result["success"]:
    print(f"使用成功！{result['message']}")
else:
    print(f"使用失败：{result['message']}")

# 检查技能是否可用
skill = skill_manager.get_skill("qingyun_dao")
if skill.is_available():
    print("技能已就绪")
else:
    print(f"冷却中，还剩 {skill.current_cooldown} 回合")
```

### 3. 回合结算

```python
# 每回合结束时调用
skill_manager.tick_all_cooldowns()

# 检查激活的效果
effects = skill_manager.get_active_effects()
for effect in effects:
    skill = effect["skill"]
    remaining = effect["remaining_duration"]
    print(f"{skill.name} 效果还剩 {remaining} 回合")
```

### 4. 应用被动效果

```python
# 在战斗中应用被动技能
context = {
    "damage_received": 100,
    "damage_dealt": 50,
    "experience_gain": 200,
}

result = skill_manager.apply_passive_effects(context)
print(f"实际受到伤害: {result['damage_received']}")
print(f"实际吸血: {result.get('heal_amount', 0)}")
```

## 技能数据定义

技能定义在 `SECT_SKILLS` 字典中：

```python
SECT_SKILLS = {
    Sect.青云宗: [
        Skill(
            id="qingyun_steady",
            name="稳如泰山",
            description="【被动】受到的伤害减少20%",
            sect=Sect.青云宗,
            skill_type=SkillType.防御,
            cooldown=0,  # 被动技能冷却为0
            effect_value=20,
        ),
        # ... 更多技能
    ],
}
```

## 冷却机制

### 冷却规则

1. **使用技能**：`current_cooldown = cooldown`
2. **回合结束**：`current_cooldown -= 1`
3. **可用判断**：`current_cooldown <= 0`

### 效果持续时间

主动技能的效果持续时间与冷却时间独立：

```python
# 使用技能时添加效果
active_effects[skill_id] = {
    "skill": skill,
    "remaining_duration": skill.duration,
}

# 效果过期自动移除
if effect["remaining_duration"] <= 0:
    del active_effects[skill_id]
```

## 被动技能效果实现

### 当前实现的被动效果

```python
# 稳如泰山：减伤20%
if skill.id == "qingyun_steady":
    result["damage_received"] = int(result["damage_received"] * 0.8)

# 嗜血：吸血20%
if skill.id == "liyu_lifesteal":
    lifesteal = int(result["damage_dealt"] * 0.2)
    result["heal_amount"] = result.get("heal_amount", 0) + lifesteal

# 因材施教：经验加成50%
if skill.id == "xiaoyao_teach":
    result["experience_gain"] = int(result["experience_gain"] * 1.5)
```

## 存档与加载

### 存档格式

```json
{
  "skill_manager_data": {
    "sect": "青云宗",
    "skills": {
      "qingyun_steady": {
        "id": "qingyun_steady",
        "name": "稳如泰山",
        "current_cooldown": 0
      },
      "qingyun_dao": {
        "current_cooldown": 2
      }
    },
    "active_effects": {
      "qingyun_dao": {
        "skill": {...},
        "remaining_duration": 2
      }
    }
  }
}
```

### 加载方式

```python
# 从存档恢复
if player.skill_manager_data:
    skill_manager = SkillManager.from_dict(player.skill_manager_data)
```

## 扩展指南

### 添加新技能

1. 在 `SECT_SKILLS` 中添加技能定义：

```python
SECT_SKILLS = {
    Sect.青云宗: [
        # 现有技能...
        Skill(
            id="new_skill_id",
            name="新技能名称",
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

2. 如果是被动技能，在 `apply_passive_effects` 中添加效果逻辑

### 自定义技能效果

```python
class Skill:
    def apply_effect(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """应用技能效果"""
        result = context.copy()
        
        if self.id == "custom_skill":
            # 自定义效果逻辑
            result["custom_bonus"] = self.effect_value
        
        return result
```

## 平衡性建议

1. **冷却时间**：主动技能冷却不宜过短，避免 spam
2. **效果数值**：被动技能效果控制在 20-50% 之间
3. **持续时间**：效果持续 1-3 回合较为合理
4. **门派特色**：确保每个门派技能风格明显不同

## 注意事项

1. **冷却同步**：确保 `tick_all_cooldowns` 在正确的时机调用
2. **效果叠加**：相同技能的效果是否可以叠加需要明确
3. **存档兼容**：新增技能需考虑旧存档的兼容性
4. **性能优化**：避免在战斗中频繁创建 Skill 对象

## 相关文档

- [装备系统](./equipment.md)
- [天赋系统](./talent_tree.md)
- [副本系统](./dungeon.md)
- [玩家指南](../player-guide.md)
