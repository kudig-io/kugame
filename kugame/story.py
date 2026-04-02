"""故事管理

管理武侠故事的章节、任务和剧情发展，增强故事趣味性，丰富人物设定和情节发展
"""
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class Chapter(Enum):
    """故事章节枚举

    定义故事的各个章节，每个章节对应不同的故事内容和学习目标
    """
    序章 = "prologue"       # 入门介绍
    第一章 = "chapter_1"     # 容器基础
    第二章 = "chapter_2"     # 部署管理
    第三章 = "chapter_3"     # 服务发现
    第四章 = "chapter_4"     # 配置管理
    第五章 = "chapter_5"     # 存储管理
    第六章 = "chapter_6"     # 资源管理
    第七章 = "chapter_7"     # 故障排查
    第八章 = "chapter_8"     # 网络与安全
    第九章 = "chapter_9"     # 集群管理
    第十章 = "chapter_10"    # 云厂商管理
    第十一章 = "chapter_11"  # 云厂商高级特性
    终章 = "epilogue"        # 飞升大成


@dataclass
class Character:
    """故事人物数据

    存储故事中的人物信息，包括姓名、身份、性格特点等

    Attributes:
        name: 人物姓名
        identity: 人物身份
        personality: 人物性格
        dialogue_style: 对话风格
        relationship: 与玩家的关系
    """
    name: str
    identity: str
    personality: str
    dialogue_style: str
    relationship: str


@dataclass
class Monster:
    """怪物数据

    存储游戏中的怪物信息

    Attributes:
        name: 怪物名称
        health: 生命
        attack: 攻击
        defense: 防御
        experience_reward: 击败获得的经验
        command_challenge: 关联的命令挑
        description: 怪物描述
        level: 怪物等级
    """
    name: str
    health: int
    attack: int
    defense: int
    experience_reward: int
    command_challenge: Any
    description: str = ""
    level: int = 1


@dataclass
class StoryEvent:
    """故事事件数据

    存储故事中的随机事件信息

    Attributes:
        event_id: 事件ID
        title: 事件标题
        description: 事件描述
        choices: 选择列表
        consequences: 选择后果
        required_level: 触发所需等级
        rewards: 奖励信息
        event_type: 事件类型（normal, combat等）
        monster: 关联的怪物（如果是战斗事件
    """
    event_id: str
    title: str
    description: str
    choices: List[str]
    consequences: List[str]
    required_level: int = 1
    rewards: Dict[str, Any] = field(default_factory=dict)
    event_type: str = "normal"
    monster: Optional[Monster] = None


@dataclass
class StoryChapter:
    """故事章节数据

    存储故事章节的详细信息，包括标题、介绍、叙事、概念、命令等

    Attributes:
        chapter_id: 章节ID
        title: 章节标题
        introduction: 章节介绍
        narrative: 章节叙事内容
        kubernetes_concepts: 相关Kubernetes概念
        commands_to_learn: 本章节要学习的命
        challenge_id: 挑战ID
        reward_exp: 完成奖励经验
        characters: 出场人物列表
        events: 章节事件列表
        boss_fight: 是否boss
        ascii_image: ASCII图片，增强故事的视觉效果
    """
    chapter_id: Chapter
    title: str
    introduction: str
    narrative: str
    kubernetes_concepts: List[str]
    commands_to_learn: List[str]
    challenge_id: str
    reward_exp: int
    characters: List[Character] = field(default_factory=list)
    events: List[StoryEvent] = field(default_factory=list)
    boss_fight: bool = False
    ascii_image: Optional[str] = None

    @property
    def command_count(self) -> int:
        """获取本章节的命令数量"""
        return len(self.commands_to_learn)


class StoryManager:
    """故事管理

    管理武侠故事的章节、任务和剧情发展，提供故事内容、事件生成和进度跟踪功能

    Attributes:
        chapters: 章节字典
        current_chapter: 当前章节
        characters: 所有出场人
        random_events: 随机事件列表
    """
    chapters: Dict[Chapter, StoryChapter]
    current_chapter: Chapter
    characters: Dict[str, Character]
    random_events: List[StoryEvent]

    def __init__(self) -> None:
        self.characters = self._initialize_characters()
        self.random_events = self._initialize_random_events()
        self.chapters = self._initialize_chapters()
        self.current_chapter = Chapter.序章

    def _initialize_characters(self) -> Dict[str, Character]:
        """初始化故事人

        创建故事中所有出场的人物角色

        Returns:
            Dict[str, Character]: 人物字典
        """
        return {
            "掌门真人": Character(
                name="青云子",
                identity="青云宗掌门",
                personality="慈祥睿智，深谋远虑",
                dialogue_style="语重心长，充满哲理",
                relationship="师父"
            ),
            "大师兄": Character(
                name="李青峰",
                identity="青云宗大师兄，执法堂首座",
                personality="严肃认真，一丝不苟",
                dialogue_style="直接明了，严格要求",
                relationship="师兄"
            ),
            "二师兄": Character(
                name="王浩宇",
                identity="青云宗二师兄，外门执事",
                personality="热情开朗，乐于助人",
                dialogue_style="亲切友好，循循善诱",
                relationship="师兄"
            ),
            "三师姐": Character(
                name="林雨竹",
                identity="青云宗三师姐，藏经阁管理员",
                personality="温柔体贴，博学多才",
                dialogue_style="娓娓道来，详细耐心",
                relationship="师姐"
            ),
            "四师妹": Character(
                name="苏灵犀",
                identity="青云宗四师妹，炼丹阁弟子",
                personality="活泼可爱，古灵精怪",
                dialogue_style="俏皮灵动，充满活力",
                relationship="师妹"
            ),
            "魔教教主": Character(
                name="血魔",
                identity="炼狱门教主",
                personality="阴险狡诈，野心勃勃",
                dialogue_style="冷酷无情，充满威胁",
                relationship="敌人"
            ),
            "神秘人": Character(
                name="神秘人",
                identity="来历不明的修真者",
                personality="神秘莫测，亦正亦邪",
                dialogue_style="高深莫测，意味深长",
                relationship="中立"
            )
        }

    def _initialize_random_events(self) -> List[StoryEvent]:
        """初始化随机事件

        创建游戏中可能触发的随机事件列表

        Returns:
            List[StoryEvent]: 随机事件列表
        """
        return [
            # 普通事件
            StoryEvent(
                event_id="treasure_found",
                title="发现宝藏",
                description="你在宗门后山修炼时，意外发现了一个隐藏的宝箱",
                choices=["打开宝箱", "上报宗门", "离开此地"],
                consequences=[
                    "你打开了宝箱，发现了一本修炼秘籍！获得100经验值！",
                    "你将宝箱上报宗门，掌门真人赞赏你的诚实，奖励50经验值！",
                    "你决定不惹麻烦，离开了此地"
                ],
                required_level=1,
                rewards={
                    "0": {"experience": 100},
                    "1": {"experience": 50}
                }
            ),
            StoryEvent(
                event_id="disciple_quarrel",
                title="弟子争执",
                description="你遇到两个弟子正在争执，他们都认为自己的Kubernetes命令是正确的",
                choices=["调解争执", "支持大师兄派", "支持二师兄派"],
                consequences=[
                    "你成功调解了争执，两人都向你道谢。获得了80经验值！",
                    "你支持了大师兄派，大师兄对你好感度提升。获得了50经验值！",
                    "你支持了二师兄派，二师兄对你好感度提升。获得了50经验值！"
                ],
                required_level=3,
                rewards={
                    "0": {"experience": 80},
                    "1": {"experience": 50},
                    "2": {"experience": 50}
                }
            ),
            StoryEvent(
                event_id="mysterious_visitor",
                title="神秘访客",
                description="一位神秘访客来到宗门，想要挑战你的Kubernetes知识",
                choices=["接受挑战", "拒绝挑战", "请教访客"],
                consequences=[
                    "你接受了挑战，成功击败了访客！获得了150经验值！",
                    "你拒绝了挑战，访客失望地离开了",
                    "你向访客请教，学到了不少新知识。获得了30经验值！"
                ],
                required_level=5,
                rewards={
                    "0": {"experience": 150},
                    "2": {"experience": 30}
                }
            ),

            # 战斗事件
            StoryEvent(
                event_id="monster_attack_pod",
                title="Pod魔袭击",
                description="一只Pod魔突然从虚空中出现，它不断吞噬周围的资源，你必须阻止它！",
                choices=["战斗", "逃跑"],
                consequences=[
                    "你与Pod魔展开了激烈的战斗",
                    "你选择了逃跑，Pod魔在身后穷追不舍"
                ],
                required_level=2,
                event_type="combat",
                monster=Monster(
                    name="Pod魔",
                    health=50,
                    attack=8,
                    defense=2,
                    experience_reward=100,
                    command_challenge="kubectl get pods",
                    description="由失控的Pod转化而成的怪物，喜欢吞噬资源",
                    level=2
                )
            ),
            StoryEvent(
                event_id="monster_deployment",
                title="Deployment巨兽",
                description="一只巨大的Deployment巨兽正在破坏宗门的部署，它能够不断分裂出Pod魔！",
                choices=["战斗", "寻找支援"],
                consequences=[
                    "你勇敢地与Deployment巨兽展开了战斗！",
                    "你去寻找同门支援，回来时Deployment巨兽已经破坏了更多部署！"
                ],
                required_level=5,
                event_type="combat",
                monster=Monster(
                    name="Deployment巨兽",
                    health=120,
                    attack=15,
                    defense=5,
                    experience_reward=250,
                    command_challenge="kubectl scale deployment",
                    description="由失控的Deployment转化而成的巨兽，能够不断分裂",
                    level=5
                )
            ),
            StoryEvent(
                event_id="monster_service",
                title="Service幽灵",
                description="一只Service幽灵正在干扰宗门的网络，导致服务无法正常通信",
                choices=["战斗", "修复网络"],
                consequences=[
                    "你与Service幽灵展开了激烈的战斗",
                    "你尝试修复网络，但Service幽灵不断干扰你的工作"
                ],
                required_level=8,
                event_type="combat",
                monster=Monster(
                    name="Service幽灵",
                    health=80,
                    attack=12,
                    defense=3,
                    experience_reward=200,
                    command_challenge="kubectl get services",
                    description="由故障的Service转化而成的幽灵，干扰网络通信",
                    level=8
                )
            ),

            # 其他事件
            StoryEvent(
                event_id="sword_dojo",
                title="剑冢试炼",
                description="你来到了宗门的剑冢试炼场，这里有各种Kubernetes命令的剑谱等待你挑战",
                choices=["挑战初级剑谱", "挑战中级剑谱", "挑战高级剑谱"],
                consequences=[
                    "你轻松完成了初级剑谱挑战！获得了50经验值！",
                    "你花费了一些时间，终于完成了中级剑谱挑战！获得了120经验值！",
                    "高级剑谱异常艰难，你勉强通过，获得了200经验值和稀有称号！"
                ],
                required_level=7,
                rewards={
                    "0": {"experience": 50},
                    "1": {"experience": 120},
                    "2": {"experience": 200, "title": "剑谱大师"}
                }
            ),
            StoryEvent(
                event_id="crisis_at_gate",
                title="山门危机",
                description="魔教弟子突然袭击山门，你需要立即采取行动！",
                choices=["正面迎敌", "迂回包抄", "通知师兄师姐"],
                consequences=[
                    "你正面迎敌，虽然受伤，但成功击退了敌人！获得了100经验值！",
                    "你迂回到敌人身后，发动突袭，获得了80经验值和大师兄的赞赏",
                    "你通知了师兄师姐，大家一起轻松击退了敌人！获得了50经验值！"
                ],
                required_level=9,
                rewards={
                    "0": {"experience": 100},
                    "1": {"experience": 80},
                    "2": {"experience": 50}
                }
            ),
            
            # 新增事件
            StoryEvent(
                event_id="alchemy_accident",
                title="炼丹意外",
                description="四师妹在炼丹时不小心炸炉，需要你帮忙清理",
                choices=["帮忙清理", "提供建议", "避开危险"],
                consequences=[
                    "你帮忙清理了现场，四师妹感激不尽，送你一枚恢复丹药！生命值恢复50！",
                    "你提供了改进建议，四师妹受益匪浅，奖励你30经验值！",
                    "你选择避开，但听说后来大师兄去帮忙了"
                ],
                required_level=4,
                rewards={
                    "0": {"health": 50},
                    "1": {"experience": 30}
                }
            ),
            StoryEvent(
                event_id="ancient_scroll",
                title="古籍发现",
                description="你在藏经阁发现了一本残缺的古籍，似乎是关于Kubernetes的秘籍",
                choices=["尝试修复", "请教三师姐", "自己研究"],
                consequences=[
                    "你成功修复了古籍，学会了一个新命令！",
                    "三师姐帮你解读，你们共同获得了80经验值！",
                    "你自己研究有所收获，获得了40经验值！"
                ],
                required_level=6,
                rewards={
                    "1": {"experience": 80},
                    "2": {"experience": 40}
                }
            ),
            StoryEvent(
                event_id="com petition",
                title="宗门大比",
                description="宗门举办Kubernetes命令大赛，你是否参加？",
                choices=["参加初赛", "参加决赛", "旁观学习"],
                consequences=[
                    "你在初赛中脱颖而出，获得了60经验值！",
                    "你在决赛中夺得冠军！获得了200经验值和稀有装备！",
                    "你旁观学习，获得了20经验值和一些技巧"
                ],
                required_level=10,
                rewards={
                    "0": {"experience": 60},
                    "1": {"experience": 200},
                    "2": {"experience": 20}
                }
            ),
            StoryEvent(
                event_id="elder_guidance",
                title="前辈指点",
                description="一位隐世前辈路过宗门，愿意指点你修炼",
                choices=["请教攻击技巧", "请教防御心法", "请教学习效率"],
                consequences=[
                    "前辈传授你攻击技巧，攻击力永久+2！",
                    "前辈传授你防御心法，防御力永久+2！",
                    "前辈传授你学习方法，获得100经验值！"
                ],
                required_level=12,
                rewards={
                    "0": {"attack": 2},
                    "1": {"defense": 2},
                    "2": {"experience": 100}
                }
            ),
            StoryEvent(
                event_id="stray_pet",
                title="走失的灵兽",
                description="一只可爱的ConfigMap小精灵在宗门走失了",
                choices=["帮忙寻找主人", "喂食安抚", "带它游览宗门"],
                consequences=[
                    "你找到了主人，获得50经验值和一件随机装备！",
                    "你安抚了小精灵，它送你一颗灵珠，生命值上限+10！",
                    "你带它游览宗门，度过了愉快的时光，获得30经验值！"
                ],
                required_level=3,
                rewards={
                    "0": {"experience": 50},
                    "1": {"max_health": 10},
                    "2": {"experience": 30}
                }
            ),
            StoryEvent(
                event_id="night_mission",
                title="夜间巡逻",
                description="大师兄邀请你一起进行夜间巡逻",
                choices=["欣然接受", "询问详情", "婉言谢绝"],
                consequences=[
                    "巡逻中发现潜入者，成功击退！获得120经验值！",
                    "了解详情后做好准备，巡逻顺利，获得60经验值！",
                    "你谢绝了邀请，但听说那晚很平静"
                ],
                required_level=7,
                rewards={
                    "0": {"experience": 120},
                    "1": {"experience": 60}
                }
            )
        ]

    def _initialize_chapters(self) -> Dict[Chapter, StoryChapter]:
        """初始化所有章节

        创建故事的所有章节，包括章节内容、概念、命令和人物。

        Returns:
            Dict[Chapter, StoryChapter]: 章节字典
        """
        return {
            Chapter.序章: StoryChapter(
                chapter_id=Chapter.序章,
                title="踏入仙门",
                introduction="凡人之躯，亦可问道苍穹。你站在青云宗山门前，心中充满对修真大道的好奇与向往",
                narrative="""
                青云宗，乃修真界第一大宗，以"道法自然，容器之道"闻名于世。宗门建在云海之上，
                弟子们修炼的是将万物化为容器的神通，可随心所欲地操控各种资源。

                山门前，一位白发苍苍的老者正在清扫落叶。他抬头看了你一眼，眼中闪过一丝精光：
                "年轻人，你可见过那云端之上的仙境？"

                "弟子未曾见过，但心向往之。"你恭敬地回答道。

                老者微微一笑："要想踏入仙境，需先学习'容器'之术。此术可将万物装入方寸之间，
                随取随用，来去自如。我是青云宗的掌门青云子，你可愿拜入我门下？"

                你毫不犹豫地跪下："弟子愿意！"

                青云子满意地点点头，手中拂尘一挥，一行金色文字浮现空中：

                ┌─────────────────────────────────────────────────────────
                                   容器化入门心
                ├─────────────────────────────────────────────────────────
                 kubectl run nginx --image=nginx
                 （创建名为nginx的容器，如意金箍棒般随心所欲）
                └─────────────────────────────────────────────────────────

                "此乃'kubectl run'心法，可创建世间万物。去吧，在心中默念此咒，
                感受容器化之术的奇妙。待你掌握此术，便正式成为我青云宗的弟子
                """,
                kubernetes_concepts=["容器化基础", "Pod概念", "容器运行"],
                commands_to_learn=["kubectl run", "kubectl get pods", "kubectl describe pod"],
                challenge_id="prologue_challenge",
                reward_exp=200,
                characters=[self.characters["掌门真人"]],
                events=[],
                boss_fight=False,
                ascii_image=r"""
                ┌─────────────────────────────────────────────────────────┐
                │                                                        │
                │    ______  ______  ______  ______  ______  ______     │
                │   /\  __ \/\  __ \/\  __ \/\  __ \/\  __ \/\  __ \    │
                │   \ \  __ \/\ \ \ \ \  __ \/\  __ \/\  __ \/\  __ \/   │
                │    \ \_____\/\ \___\/\_____\/\_\/_\/\_____\/\/_____\  │
                │                                                        │
                └─────────────────────────────────────────────────────────┘
                """
            )
        }

    def get_current_chapter(self) -> StoryChapter:
        """获取当前章节
        
        Returns:
            StoryChapter: 当前章节对象
        """
        return self.chapters[self.current_chapter]
    
    def get_chapter(self, chapter: Chapter) -> Optional[StoryChapter]:
        """获取指定章节
        
        Args:
            chapter: 章节枚举
            
        Returns:
            Optional[StoryChapter]: 章节对象，如果不存在返回None
        """
        return self.chapters.get(chapter)
    
    def advance_chapter(self) -> bool:
        """推进到下一章节
        
        Returns:
            bool: 成功推进返回True，已到终章返回False
        """
        chapters_list = list(Chapter)
        current_idx = chapters_list.index(self.current_chapter)
        
        if current_idx < len(chapters_list) - 1:
            self.current_chapter = chapters_list[current_idx + 1]
            return True
        return False
    
    def get_all_commands(self) -> List[str]:
        """获取所有章节的命令
        
        Returns:
            List[str]: 所有命令列表
        """
        commands = []
        for chapter in self.chapters.values():
            commands.extend(chapter.commands_to_learn)
        return commands
    
    def get_chapter_commands(self, chapter: Chapter) -> List[str]:
        """获取指定章节的命令
        
        Args:
            chapter: 章节枚举
            
        Returns:
            List[str]: 命令列表
        """
        ch = self.chapters.get(chapter)
        return ch.commands_to_learn if ch else []
    
    def get_total_chapters(self) -> int:
        """获取总章节数
        
        Returns:
            int: 章节总数
        """
        return len(self.chapters)
    
    def get_completed_chapters(self, current_chapter_value: str) -> int:
        """获取已完成章节数
        
        Args:
            current_chapter_value: 当前章节的值
            
        Returns:
            int: 已完成章节数
        """
        try:
            current = Chapter(current_chapter_value)
            chapters_list = list(Chapter)
            return chapters_list.index(current)
        except ValueError:
            return 0
    
    def get_story_progress(self, player) -> Dict[str, Any]:
        """获取故事进度
        
        Args:
            player: 玩家对象
            
        Returns:
            Dict[str, Any]: 故事进度信息
        """
        current = self.get_current_chapter()
        total_chapters = self.get_total_chapters()
        completed = self.get_completed_chapters(player.current_chapter)
        
        return {
            "current_chapter": player.current_chapter,
            "current_title": current.title,
            "total_chapters": total_chapters,
            "completed_chapters": completed,
            "progress_percentage": round(completed / total_chapters * 100, 1) if total_chapters > 0 else 0,
            "mastered_commands": len(player.kubectl_commands_mastered),
            "all_commands": len(self.get_all_commands()),
        }
