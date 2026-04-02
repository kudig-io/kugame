# 成就系统文档

## 概述

成就系统是KuGame的核心激励机制之一，记录玩家在游戏中的各种里程碑，提供经验值和称号奖励，激励玩家持续学习和探索。

## 成就类型

系统包含10种成就类型，共20+个成就：

### 1. 命令掌握 (`command_mastery`)
奖励玩家学习和掌握Kubernetes命令的进度。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| cmd_master_10 | 入门弟子 | 掌握10个命令 | 500经验 + 称号 |
| cmd_master_30 | 熟练弟子 | 掌握30个命令 | 1500经验 + 称号 |
| cmd_master_50 | 命令专家 | 掌握50个命令 | 3000经验 + 称号 |
| cmd_master_all | 命令大师 | 掌握所有命令 | 10000经验 + 称号 |

### 2. 故事进度 (`story_progress`)
奖励玩家推进游戏故事剧情。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| story_chapter_3 | 初入江湖 | 完成第3章 | 1000经验 + 称号 |
| story_chapter_6 | 江湖少侠 | 完成第6章 | 2500经验 + 称号 |
| story_chapter_9 | 武林高手 | 完成第9章 | 5000经验 + 称号 |

### 3. 挑战完成 (`challenge_completion`)
奖励玩家完成各种挑战任务。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| challenge_10 | 挑战新手 | 完成10个挑战 | 800经验 + 称号 |
| challenge_50 | 挑战达人 | 完成50个挑战 | 4000经验 + 称号 |

### 4. 连续成功 (`streak_success`)
奖励玩家连续正确回答的连击表现。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| streak_5 | 小有成就 | 连续答对5次 | 300经验 + 称号 |
| streak_10 | 势如破竹 | 连续答对10次 | 800经验 + 称号 |
| streak_20 | 无人能挡 | 连续答对20次 | 2000经验 + 称号 |

### 5. 收集成就 (`collection`)
奖励玩家收集装备的数量和品质。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| equipment_10 | 装备收集者 | 收集10件装备 | 500经验 + 称号 |
| equipment_50 | 装备收藏家 | 收集50件装备 | 2000经验 + 称号 |
| equipment_orange | 传说装备 | 获得传说品质装备 | 3000经验 + 称号 |

### 6. 等级成就 (`level_achievement`)
奖励玩家角色等级的提升。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| level_10 | 初出茅庐 | 达到10级 | 300经验 + 称号 |
| level_30 | 小有所成 | 达到30级 | 1000经验 + 称号 |
| level_50 | 一代宗师 | 达到50级 | 3000经验 + 称号 |
| level_100 | 修仙巅峰 | 达到100级 | 10000经验 + 称号 |

### 7. 挑战塔成就 (`tower_achievement`)
奖励玩家在挑战塔中的进度。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| tower_10 | 塔之新人 | 达到10层 | 500经验 + 称号 |
| tower_50 | 塔之勇士 | 达到50层 | 3000经验 + 称号 |
| tower_100 | 通天塔主 | 达到100层 | 10000经验 + 称号 |

### 8. 战斗成就 (`combat_achievement`)
奖励玩家参与战斗和取得胜利。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| combat_100 | 百战老兵 | 参加100场战斗 | 1000经验 + 称号 |
| combat_win_50 | 常胜将军 | 赢得50场战斗 | 2000经验 + 称号 |

### 9. 特殊成就 (`special_achievement`)
特殊条件下获得的独特成就。

| 成就ID | 名称 | 条件 | 奖励 |
|--------|------|------|------|
| first_login | 初入仙门 | 首次登录游戏 | 100经验 + 称号 |
| perfect_answer | 完美答题 | 单次答对10道题 | 1000经验 + 称号 |

### 10. 门派专精 (`sect_specialization`)
奖励玩家对特定门派的精通程度。

## API接口

### Player类成就方法

#### 检查成就
```python
# 检查并解锁所有符合条件的成就
unlocked = player.check_and_unlock_achievements()

# 检查特定类型成就
unlocked = player.check_level_achievements()
unlocked = player.check_equipment_achievements(equipment_count, has_orange)
unlocked = player.check_tower_achievements(highest_level)
unlocked = player.check_combat_achievements(total_combats, wins)

# 检查特殊成就
success = player.unlock_first_login()
unlocked = player.check_perfect_answer(correct_count)
```

#### 获取成就信息
```python
# 获取成就进度
progress = player.get_achievement_progress()

# 获取成就统计
stats = player.get_achievement_stats()
# 返回: {
#     "total_achievements": 25,
#     "unlocked_count": 5,
#     "locked_count": 20,
#     "completion_percentage": 20.0,
#     "by_type": {...},
#     "recent_unlocked": [...]
# }
```

### GameEngine集成

成就系统在以下游戏事件中自动检查和解锁：

1. **学习命令时**: 检查命令掌握成就
2. **完成故事章节时**: 检查故事进度成就
3. **完成挑战时**: 检查挑战完成成就
4. **答题正确/错误时**: 检查连续成功成就、完美答题成就
5. **战斗胜利时**: 更新战斗统计，检查战斗成就
6. **获得装备时**: 检查装备收集成就
7. **完成挑战塔层时**: 检查挑战塔成就
8. **升级时**: 检查等级成就

## 战斗统计

Player类包含以下战斗统计属性：

```python
player.total_combats      # 总战斗次数
player.combats_won        # 胜利次数
player.combats_lost       # 失败次数
player.highest_tower_level # 最高挑战塔层数
```

这些统计用于成就检查，并在游戏过程中自动更新。

## 成就通知

当玩家解锁新成就时，系统会显示：
- 成就名称
- 成就描述
- 获得奖励（经验值、称号等）
- 解锁动画效果

## 未来扩展

计划添加的成就类型：

1. **签到成就**: 连续签到天数奖励
2. **社交成就**: 分享游戏、邀请好友等
3. **探索成就**: 发现隐藏内容、完成彩蛋等
4. **精通成就**: 完美掌握特定命令或概念
5. **限时成就**: 特定时间内完成的挑战
