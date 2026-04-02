# PVP竞技场系统文档

## 概述

PVP竞技场系统提供异步玩家对战功能，玩家可以与系统匹配的真人玩家镜像或AI对手进行战斗，通过胜利获得积分提升段位。

## 核心功能

### 段位系统

竞技场共有7个段位，从低到高依次为：

| 段位 | 积分范围 | 说明 |
|------|---------|------|
| 青铜 | 0-1000 | 初入竞技场 |
| 白银 | 1000-1200 | 稍有实力 |
| 黄金 | 1200-1400 | 实力不俗 |
| 铂金 | 1400-1600 | 高手云集 |
| 钻石 | 1600-1800 | 顶尖强者 |
| 大师 | 1800-2000 | 一代宗师 |
| 王者 | 2000+ | 竞技场巅峰 |

### 积分系统

使用ELO算法变种计算积分变化：

- **基础K值**：32分（根据段位调整）
  - 青铜/白银：48分（帮助新手成长）
  - 黄金/铂金：32分（标准）
  - 钻石及以上：16分（高端局稳定）

- **连胜加成**：
  - 3连胜：+5分
  - 5连胜：+10分
  - 7连胜：+20分
  - 10连胜：+50分

### 匹配机制

1. **优先匹配积分相近的对手**（200分以内）
2. **无合适对手时匹配AI**
3. **AI强度根据玩家积分动态调整**

### 赛季系统

- **赛季周期**：30天
- **赛季重置**：
  - 积分重置为1000
  - 保留最高积分记录
  - 连胜/连败重置
- **赛季奖励**：根据赛季排名发放

## API接口

### ArenaSystem类

```python
from kugame.arena import ArenaSystem

# 创建竞技场实例
arena = ArenaSystem()

# 注册/更新玩家
player = arena.register_player({
    "player_id": "player_001",
    "player_name": "玩家名",
    "level": 50,
    "attack": 150,
    "defense": 100,
    "health": 500,
    "equipment_score": 200,
})

# 寻找匹配对手
opponent = arena.find_match("player_001")

# 进行战斗
result = arena.battle("player_001", opponent.player_id)
# 返回:
# {
#     "success": True,
#     "battle_id": "...",
#     "winner_id": "player_001",
#     "attacker": {"rating_change": +25, ...},
#     "defender": {"rating_change": -20, ...},
# }

# 获取竞技场排名
ranking = arena.get_ranking(limit=100)

# 获取玩家信息
info = arena.get_player_info("player_001")

# 获取战斗历史
history = arena.get_battle_history("player_001", limit=10)

# 获取赛季信息
season = arena.get_season_info()
```

### ArenaPlayer类

```python
from kugame.arena import ArenaPlayer

player = ArenaPlayer(
    player_id="player_001",
    player_name="玩家名",
    level=50,
    rating=1500,
)

# 属性
player.rating  # 当前积分
player.rank  # 当前段位（ArenaRank枚举）
player.win_rate  # 胜率
player.streak  # 连胜/连败数

# 方法
player.update_rating(25)  # 更新积分
```

## 战斗机制

战斗采用简化版战力对比：

```
战力 = 攻击×2 + 防御 + 生命÷10 + 装备评分

胜率 = 己方战力 / (己方战力 + 敌方战力)
```

根据胜率随机决定战斗结果。

## 数据存储

竞技场数据存储在 `arena_data.json` 文件中：

```json
{
  "players": {
    "player_id": { ...玩家数据... }
  },
  "battle_history": [ ...战斗记录... ],
  "current_season": { ...赛季信息... }
}
```

## 与Player类集成

在Player类中可以使用竞技场系统：

```python
player = Player(name="Test", sect="青云宗")

# 注册到竞技场
arena = ArenaSystem()
arena_player = arena.register_player({
    "player_id": player.name,
    "player_name": player.name,
    "level": player.level,
    "attack": player.total_attack,
    "defense": player.total_defense,
    "health": player.total_max_health,
})
```

## 后续扩展

1. **实时对战**：WebSocket实现真人对战
2. **观战系统**：观看高手对战
3. **战队赛**：组建战队进行团队对战
4. **锦标赛**：周期性大型比赛
5. **赛季皮肤**：根据段位获得专属外观
