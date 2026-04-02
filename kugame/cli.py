"""命令行界面

KuGame的交互式命令行界面。
"""
# -*- coding: utf-8 -*-

import sys
import os

# 设置默认编码为utf-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import box
from .game_engine import GameEngine
from .player import Sect


class CLI:
    """命令行界面"""

    def __init__(self) -> None:
        self.console = Console()
        self.engine = GameEngine()
        self.running = True

    def clear_screen(self) -> None:
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self) -> None:
        """打印游戏横幅"""
        banner = """
        ╔═══════════════════════════════════════════════════════════════════╗
        ║                                                                   ║
        ║      ████████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗                   ║
        ║      ╚══██╔══╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝                   ║
        ║         ██║   ███████║███████║██║     █████╔╝                    ║
        ║         ██║   ██╔══██║██╔══██║██║     ██╔═██╗                    ║
        ║         ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗                   ║
        ║         ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                   ║
        ║                                                                   ║
        ║              游戏化学习 Kubernetes 命令行工具                     ║
        ║                                                                   ║
        ╚═══════════════════════════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold magenta")
        self.console.print()

    def print_menu(self, options: List[Dict[str, str]]) -> None:
        """打印菜单"""
        table = Table(box=box.ROUNDED, show_header=False)
        table.add_column("选项", justify="right", style="cyan")
        table.add_column("名称", style="green")
        table.add_column("描述", style="white")

        for idx, option in enumerate(options, 1):
            table.add_row(
                f"[{idx}]",
                option["name"],
                option["description"]
            )

        self.console.print(Panel(table, title="主菜单", border_style="blue"))

    def get_sect_selection(self) -> Sect:
        """获取门派选择"""
        self.console.print("\n[bold yellow]选择你的门派：[/bold yellow]\n")

        sects = list(Sect)
        for idx, sect in enumerate(sects, 1):
            self.console.print(f"[{idx}] {sect.value}")

        self.console.print()
        choice = Prompt.ask("请输入门派编号", default="1")

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sects):
                return sects[idx]
        except ValueError:
            pass

        return Sect.青云宗

    def start(self) -> None:
        """开始游戏"""
        self.clear_screen()
        self.print_banner()

        if self.engine.load_player():
            player = self.engine.player
            if player:
                self.console.print(f"[green]✓ 欢迎回来，[/green][cyan]{player.title}[/cyan]！")
                self.console.print()
        else:
            self.console.print("[bold yellow]新侠客，欢迎来到KuGame！[/bold yellow]\n")
            name = Prompt.ask("请输入你的侠名", default="无名")
            sect = self.get_sect_selection()
            self.engine.initialize_player(name, sect)
            player = self.engine.player
            if player:
                self.console.print(f"\n[green]✓ 欢迎加入[/green][cyan]{sect.value}[/cyan]，{player.title}侠客！")

        self.main_loop()

    def main_loop(self) -> None:
        """主循环"""
        while self.running:
            self.console.print()
            self.console.print("[bold magenta]─" * 60)
            self.console.print("[bold magenta]│  🏔️  Kubernetes 修仙之旅 🏔️  │")
            self.console.print("[bold magenta]─" * 60)
            self.console.print()

            options = self.engine.get_menu_options()
            self.print_menu(options)

            self.console.print()
            choice = Prompt.ask("[bold yellow]请选择你的行动：[/bold yellow]", default="1")

            self.handle_choice(choice)

    def handle_choice(self, choice: str) -> None:
        """处理用户选择

        Args:
            choice: 用户选择的选项
        """
        options = {f"{idx}": opt["id"] for idx, opt in enumerate(self.engine.get_menu_options(), 1)}

        action = options.get(choice)

        if action == "story":
            self.play_story()
        elif action == "practice":
            self.practice()
        elif action == "challenge":
            self.do_challenge()
        elif action == "quiz":
            self.do_quiz()
        elif action == "progress":
            self.show_progress()
        elif action == "commands":
            self.show_commands()
        elif action == "equipment":
            self.manage_equipment()
        elif action == "shop":
            self.visit_shop()
        elif action == "dungeon":
            self.dungeon_menu()
        elif action == "checkin":
            self.daily_checkin()
        elif action == "help":
            self.show_help()
        elif action == "save":
            self.save_game()
        elif action == "save_manager":
            self.manage_saves()
        elif action == "quit":
            self.quit_game()
        else:
            self.console.print("[red]无效选择，请重新输入[/red]")

    def play_story(self) -> None:
        """播放故事"""
        self.clear_screen()
        story = self.engine.get_story_content()

        # 显示ASCII图片
        if "ascii_image" in story and story["ascii_image"]:
            self.console.print(story["ascii_image"])
            self.console.print()

        # 增加故事播放的沉浸式效果
        self.console.print("[bold magenta]" + "═" * 70)
        self.console.print(f"[bold magenta]│{('第' + story['chapter_id'] + '章 - ' + story['title']).center(68)}│")
        self.console.print("[bold magenta]" + "═" * 70)
        self.console.print()

        # 显示故事介绍，增加神秘感
        self.console.print(Panel(
            "[italic]" + story["introduction"] + "[/italic]",
            border_style="cyan",
            box=box.DOUBLE_EDGE
        ))
        self.console.print()

        # 故事背景展示
        self.console.print("[bold yellow]🌟 故事背景 🌟[/bold yellow]")
        self.console.print("[dim cyan]" + "─" * 60 + "[/dim cyan]")
        self.console.print(story["narrative"])
        self.console.print()

        # 本章节学习内容
        if story["commands"]:
            self.console.print("[bold green]📜 本章节修炼内容 📜[/bold green]")
            self.console.print("[dim cyan]" + "─" * 60 + "[/dim cyan]")
            for idx, cmd in enumerate(story["commands"], 1):
                self.console.print(f"  [{idx}] {cmd}")

            self.console.print()
            self.console.print("[bold cyan]🎁 完成奖励 🎁[/bold cyan]")
            self.console.print(f"  • 经验值：[green]{story['reward_exp']}[/green]")
            self.console.print("  • 境界提升：[yellow]有可能突破当前境界[/yellow]")

        self.console.print()
        self.console.print("[dim cyan]" + "─" * 70 + "[/dim cyan]")

        # 增加更有故事性的提示
        if story["commands"]:
            if Confirm.ask("\n[bold magenta]是否准备好迎接挑战，开始修炼？[/bold magenta]"):
                self.do_challenge()
        else:
            if Confirm.ask("\n[bold magenta]是否准备好继续修炼之旅？[/bold magenta]"):
                self.advance_story()

    def practice(self) -> None:
        """练习模式"""
        self.clear_screen()
        commands = self.engine.get_practice_commands()

        if not commands:
            self.console.print("[yellow]还没有掌握任何命令，请先完成故事章节[/yellow]")
            return

        self.console.print(f"[bold]已掌握 {len(commands)} 个命令[/bold]\n")

        for idx, cmd in enumerate(commands, 1):
            self.console.print(f"[{idx}] {cmd}")

        self.console.print("\n输入命令编号进行练习，输入'q'返回菜单")

        while True:
            choice = Prompt.ask("命令编号")

            if choice.lower() == 'q':
                break

            try:
                idx = int(choice) - 1
                if 0 <= idx < len(commands):
                    self.show_command_practice(commands[idx])
            except ValueError:
                self.console.print("[red]无效输入[/red]")

    def show_command_practice(self, command: str) -> None:
        """显示命令练习"""
        cmd_info = self.engine.command_manager.get_command(command)

        if not cmd_info:
            return

        # 确保只有KubectlCommand类型才能访问kubernetes_concept属性
        from .kubernetes_commands import KubectlCommand
        concept = cmd_info.kubernetes_concept if isinstance(cmd_info, KubectlCommand) else ''

        panel = Panel(
            f"[bold]命令：[/bold]{command}\n\n"
            f"[bold]语法：[/bold]{cmd_info.syntax}\n\n"
            f"[bold]示例：[/bold]\n{cmd_info.example}\n\n"
            f"[bold]说明：[/bold]{cmd_info.description}\n\n"
            f"[bold]相关概念：[/bold]{concept}",
            title=f"练习：{command}",
            border_style="green"
        )

        self.console.print(panel)

    def do_challenge(self) -> None:
        """执行挑战"""
        self.clear_screen()
        challenge = self.engine.generate_challenge()

        if not challenge:
            self.console.print("[yellow]暂无可用挑战[/yellow]")
            return

        # 构建挑战面板内容，包含选项
        challenge_content = f"[bold]挑战：{challenge.title}[/bold]\n\n"
        challenge_content += f"{challenge.description}\n\n"
        challenge_content += f"[bold]问题：[/bold]{challenge.question}\n\n"

        # 添加选项
        challenge_content += "[bold]选项：[/bold]\n"
        for idx, option in enumerate(challenge.options, 1):
            challenge_content += f"  [{idx}] {option}\n"

        challenge_content += f"\n[italic]提示：{challenge.hint}[/italic]"

        self.console.print(Panel(
            challenge_content,
            title="⚔️ 挑战任务",
            border_style="red"
        ))

        # 获取用户选择
        while True:
            try:
                user_input = Prompt.ask("\n请选择你的答案 (1-4)")
                user_choice = int(user_input)
                if 1 <= user_choice <= len(challenge.options):
                    break
                else:
                    self.console.print(f"[red]无效选择，请输入1-{len(challenge.options)}之间的数字[/red]")
            except ValueError:
                self.console.print("[red]无效输入，请输入数字[/red]")

        result = self.engine.check_answer(user_choice)

        self.console.print()
        if result["correct"]:
            self.console.print(Panel(
                f"[bold green]{result['message']}[/bold green]\n\n"
                f"当前连击：{result['streak']}\n"
                f"总得分：{result['score']}",
                title="✓ 挑战成功",
                border_style="green"
            ))

            if Confirm.ask("\n是否继续下一章？"):
                self.advance_story()
        else:
            self.console.print(Panel(
                f"[bold red]{result['message']}[/bold red]\n\n"
                f"[yellow]提示：{result.get('hint', '')}[/yellow]",
                title="✗ 挑战失败",
                border_style="red"
            ))
            self.engine.reset_streak()

    def advance_story(self) -> None:
        """推进故事"""
        if self.engine.advance_chapter():
            self.engine.save_game()
            self.console.print("[bold green]✓ 成功进入下一章节！[/bold green]")
        else:
            self.console.print("[bold yellow]已是最终章节，恭喜你完成全部挑战！[/bold yellow]")

    def do_combat(self, monster: Any) -> None:
        """执行战斗

        Args:
            monster: 要战斗的怪物对象
        """
        self.clear_screen()

        # 开始战斗
        self.engine.start_combat(monster)

        self.console.print(Panel(
            f"[bold red]{monster.name}出现了！[/bold red]\n\n{monster.description}\n\n[bold]怪物属性：[/bold]\n生命值：{monster.health} | 攻击力：{monster.attack} | 防御力：{monster.defense}\n\n[bold]击败奖励：[/bold]{monster.experience_reward} 经验值",
            title="⚔️ 战斗开始",
            border_style="red"
        ))

        # 战斗循环
        player = self.engine.player
        if not player:
            self.console.print("[red]错误：玩家未初始化，无法进行战斗！[/red]")
            return

        while True:
            # 显示战斗状态
            self.console.print("\n[bold]当前战斗状态：[/bold]")
            self.console.print(f"[green]你的生命值：{player.health}/{player.max_health}[/green]")
            self.console.print(f"[red]{monster.name}的生命值：{self.engine.monster_current_health}/{monster.health}[/red]")
            self.console.print()

            # 显示战斗选项
            combat_options = [
                {"id": "attack", "name": "攻击", "description": "回答命令题，对怪物造成伤害"},
                {"id": "flee", "name": "逃跑", "description": "尝试逃离战斗（成功率50%）"}
            ]

            table = Table(box=box.ROUNDED, show_header=False)
            table.add_column("选项", justify="right", style="cyan")
            table.add_column("名称", style="green")
            table.add_column("描述", style="white")

            for idx, option in enumerate(combat_options, 1):
                table.add_row(
                    f"[{idx}]",
                    option["name"],
                    option["description"]
                )

            self.console.print(Panel(table, title="战斗选项", border_style="red"))

            # 获取玩家选择
            choice = Prompt.ask("\n请选择战斗行动", default="1")

            try:
                action_idx = int(choice) - 1
                if 0 <= action_idx < len(combat_options):
                    action = combat_options[action_idx]["id"]

                    if action == "attack":
                        # 生成命令挑战
                        challenge = self.engine.generate_challenge()

                        if not challenge:
                            self.console.print("[yellow]暂无可用挑战，战斗结束[/yellow]")
                            return

                        # 显示挑战问题
                        self.console.print("\n")
                        options_text = "\n".join([f"  [{idx+1}] {option}" for idx, option in enumerate(challenge.options)])
                        self.console.print(Panel(
                            f"[bold]挑战：{challenge.title}[/bold]\n\n{challenge.description}\n\n[bold]问题：[/bold]{challenge.question}\n\n[bold]选项：[/bold]\n{options_text}",
                            title="💡 命令挑战",
                            border_style="blue"
                        ))

                        # 获取答案选择
                        while True:
                            try:
                                answer_choice = int(Prompt.ask("\n请选择你的答案 (1-4)"))
                                if 1 <= answer_choice <= len(challenge.options):
                                    break
                                else:
                                    self.console.print(f"[red]无效选择，请输入1-{len(challenge.options)}之间的数字[/red]")
                            except ValueError:
                                self.console.print("[red]无效输入，请输入数字[/red]")

                        # 检查答案
                        result = self.engine.check_answer(answer_choice)

                        # 处理战斗结果
                        combat_result = self.engine.player_attack(monster, result["correct"])

                        self.console.print("\n")
                        self.console.print(Panel(
                            f"{combat_result['message']}",
                            title="⚔️ 战斗结果",
                            border_style="green" if combat_result["status"] == "combat_won" else "red"
                        ))

                        # 检查战斗是否结束
                        if combat_result["status"] == "combat_won":
                            # 战斗胜利
                            self.console.print(f"\n[bold green]✓ 战斗胜利！[/bold green]获得了{combat_result['exp_gained']}经验值！")
                            return
                        elif combat_result["status"] == "combat_lost":
                            # 战斗失败
                            self.console.print("\n[bold red]✗ 你被击败了！[/bold red]")
                            return

                    elif action == "flee":
                        # 尝试逃跑
                        flee_result = self.engine.flee_combat(monster)

                        self.console.print("\n")
                        self.console.print(Panel(
                            flee_result["message"],
                            title="🏃 逃跑结果",
                            border_style="yellow"
                        ))

                        if flee_result["status"] == "flee_success":
                            # 逃跑成功
                            return

            except ValueError:
                self.console.print("[red]无效输入[/red]")

    def do_quiz(self) -> None:
        """执行测验"""
        self.clear_screen()
        quiz = self.engine.generate_quiz()

        if not quiz or not quiz.get("question"):
            self.console.print("[yellow]请先完成一些故事章节[/yellow]")
            return

        self.console.print(Panel(
            quiz["question"],
            title="📝 知识问答",
            border_style="cyan"
        ))

        for idx, option in enumerate(quiz["options"], 1):
            self.console.print(f"[{idx}] {option}")

        answer = Prompt.ask("\n请选择答案")

        try:
            choice = int(answer) - 1
            if 0 <= choice < len(quiz["options"]):
                correct = choice == quiz["correct_index"]

                if correct:
                    self.console.print("[bold green]✓ 回答正确！[/bold green]")
                else:
                    self.console.print(f"[bold red]✗ 回答错误[/bold red]，正确答案是：{quiz['options'][quiz['correct_index']]}")

                self.console.print(f"\n[yellow]说明：{quiz['explanation']}[/yellow]")
        except ValueError:
            self.console.print("[red]无效输入[/red]")

    def do_pure_quiz(self) -> None:
        """执行纯粹答题模式"""
        self.clear_screen()

        # 获取玩家对象
        player = self.engine.player
        if not player:
            self.console.print("[red]错误：玩家未初始化，无法进行答题！[/red]")
            return

        # 选择答题模式
        mode_options = [
            {"id": "all", "name": "全部命令", "description": "从所有命令中随机出题"},
            {"id": "wrong", "name": "错题集", "description": "只从你答错的命令中出题"}
        ]

        self.console.print(Panel(
            "欢迎进入纯粹答题模式！\n在这里你可以反复练习Kubernetes命令，提高你的技能水平。",
            title="📚 纯粹答题模式",
            border_style="cyan"
        ))

        self.console.print("\n[bold yellow]选择答题模式：[/bold yellow]\n")

        for idx, option in enumerate(mode_options, 1):
            self.console.print(f"[{idx}] {option['name']} - {option['description']}")

        self.console.print()
        mode_choice = Prompt.ask("请选择模式", default="1")

        try:
            mode_idx = int(mode_choice) - 1
            if 0 <= mode_idx < len(mode_options):
                use_wrong_commands_only = mode_idx == 1

                # 开始答题模式
                quiz_state = self.engine.start_quiz_mode(use_wrong_commands_only)

                self.console.print(f"\n[green]已进入{quiz_state['mode']}，共有{quiz_state['total_commands']}个命令可练习[/green]")
                self.console.print("\n输入 'q' 退出答题模式\n")

                # 答题循环
                while True:
                    # 生成题目
                    quiz_question = self.engine.generate_quiz_question(use_wrong_commands_only)

                    if not quiz_question:
                        self.console.print("\n[yellow]所有命令都已掌握，退出答题模式[/yellow]")
                        break

                    # 显示题目
                    options_text = "\n".join([f"  [{idx+1}] {option}" for idx, option in enumerate(quiz_question['options'])])
                    self.console.print(Panel(
                        f"[bold]问题：[/bold]{quiz_question['question']}\n\n{options_text}",
                        title="📝 命令练习",
                        border_style="cyan"
                    ))

                    # 获取答案
                    answer = Prompt.ask("\n请选择答案 (1-4)")

                    if answer.lower() == 'q':
                        break

                    try:
                        answer_idx = int(answer) - 1
                        if 0 <= answer_idx < len(quiz_question['options']):
                            correct = answer_idx == quiz_question['correct_index']

                            if correct:
                                self.console.print("\n[bold green]✓ 回答正确！[/bold green]")
                                # 从错题集中移除（如果存在）
                                if quiz_question['command_info']['name'] in player.wrong_commands:
                                    player.wrong_commands.remove(quiz_question['command_info']['name'])
                            else:
                                self.console.print(f"\n[bold red]✗ 回答错误[/bold red]，正确答案是：{quiz_question['options'][quiz_question['correct_index']]}")
                                # 加入错题集
                                if quiz_question['command_info']['name'] not in player.wrong_commands:
                                    player.wrong_commands.append(quiz_question['command_info']['name'])

                            # 显示命令详情
                            cmd_info = quiz_question['command_info']
                            self.console.print("\n[yellow]命令详情：[/yellow]")
                            self.console.print(f"  名称：{cmd_info['name']}")
                            self.console.print(f"  分类：{cmd_info['category']}")
                            self.console.print(f"  语法：{cmd_info['syntax']}")
                            self.console.print(f"  示例：{cmd_info['example']}")
                            self.console.print(f"  相关概念：{cmd_info['concept']}")

                            self.console.print("\n" + "─" * 60)
                    except ValueError:
                        self.console.print("[red]无效输入，请输入数字[/red]")

                # 保存玩家进度
                self.engine.save_game()
                self.console.print("\n[green]✓ 答题进度已保存[/green]")
        except ValueError:
            self.console.print("[red]无效输入[/red]")

    def show_progress(self) -> None:
        """显示进度"""
        self.clear_screen()
        progress = self.engine.get_progress()

        player = progress["player"]
        story = progress["story"]
        commands = progress["commands"]

        self.console.print(Panel(
            f"[bold]当前境界：[/bold]{player['cultivation']}\n"
            f"[bold]等级：[/bold]Lv.{player['level']}\n"
            f"[bold]经验值：[/bold]{player['experience']}/{player['required_exp']}\n"
            f"[bold]总得分：[/bold]{progress['total_score']}",
            title=f"👤 {player['title']}",
            border_style="yellow"
        ))

        self.console.print()

        self.console.print(Panel(
            f"[bold]当前章节：[/bold]{story['current_title']}\n"
            f"[bold]完成进度：[/bold]{story['completed_chapters']}/{story['total_chapters']}章节\n"
            f"[bold]命令掌握：[/bold]{story['mastered_commands']}/{story['all_commands']}个",
            title="📖 故事进度",
            border_style="magenta"
        ))

        self.console.print()

        table = Table(title="📚 命令分类进度", box=box.ROUNDED)
        table.add_column("分类", style="cyan")
        table.add_column("已掌握", justify="right", style="green")
        table.add_column("总数", justify="right", style="white")
        table.add_column("进度", justify="right", style="yellow")

        for cat, data in commands["by_category"].items():
            table.add_row(
                cat,
                str(data["mastered"]),
                str(data["total"]),
                f"{data['percentage']}%"
            )

        self.console.print(Panel(table, border_style="blue"))

    def show_commands(self) -> None:
        """显示所有命令"""
        self.clear_screen()
        commands = self.engine.get_all_commands_info()

        table = Table(title="📚 Kubernetes命令手册", box=box.ROUNDED)
        table.add_column("命令", style="cyan")
        table.add_column("分类", style="magenta")
        table.add_column("描述", style="white")
        table.add_column("状态", justify="center", style="green")

        for cmd in commands:
            status = "✓ 已掌握" if cmd["mastered"] else "○ 待学习"
            style = "green" if cmd["mastered"] else "dim"
            table.add_row(
                cmd["name"],
                cmd["category"],
                cmd["description"],
                Text(status, style=style)
            )

        self.console.print(Panel(table, border_style="green"))

    def save_game(self, custom_name: Optional[str] = None) -> None:
        """保存游戏

        Args:
            custom_name: 自定义存档名称
        """
        if self.engine.save_game(custom_name):
            self.console.print("[bold green]✓ 游戏进度已保存[/bold green]")
        else:
            self.console.print("[red]保存失败[/red]")

    def manage_saves(self) -> None:
        """档案管理

        提供存档管理功能，包括查看、创建、加载、删除和重命名存档。
        """
        while True:
            self.clear_screen()
            self.console.print("[bold magenta]" + "═" * 50)
            self.console.print("[bold magenta]│  📁  档案管理  📁  │")
            self.console.print("[bold magenta]" + "═" * 50)
            self.console.print()

            # 显示所有存档
            saves = self.engine.get_save_list()

            if saves:
                self.console.print("[bold cyan]当前存档列表：[/bold cyan]")
                self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")

                # 创建表格显示存档信息
                table = Table(show_header=True, header_style="bold green", box=box.SIMPLE)
                table.add_column("编号", justify="right", width=5)
                table.add_column("存档文件名", width=20)
                table.add_column("玩家名称", width=15)
                table.add_column("等级", justify="right", width=5)
                table.add_column("门派", width=10)
                table.add_column("境界", width=10)

                for idx, save in enumerate(saves, 1):
                    table.add_row(
                        str(idx),
                        save["filename"],
                        save["player_name"],
                        str(save["level"]),
                        save["sect"],
                        save["cultivation"]
                    )

                self.console.print(table)
                self.console.print()
            else:
                self.console.print("[yellow]暂无存档文件[/yellow]")
                self.console.print()

            # 显示管理选项
            self.console.print("[bold yellow]管理选项：[/bold yellow]")
            self.console.print("1. 创建新存档")
            self.console.print("2. 加载存档")
            self.console.print("3. 删除存档")
            self.console.print("4. 重命名存档")
            self.console.print("5. 返回主菜单")
            self.console.print()

            # 获取用户选择
            choice = Prompt.ask("请选择操作", default="5")

            if choice == "1":
                self.create_save()
            elif choice == "2":
                self.load_save(saves)
            elif choice == "3":
                self.delete_save(saves)
            elif choice == "4":
                self.rename_save(saves)
            elif choice == "5":
                break
            else:
                self.console.print("[red]无效选择，请重新输入[/red]")
                input("按回车键继续...")

    def create_save(self) -> None:
        """创建新存档

        提示用户输入存档名称，并保存当前游戏进度。
        """
        self.clear_screen()
        self.console.print("[bold green]📝 创建新存档[/bold green]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()

        # 提示用户输入存档名称
        save_name = Prompt.ask("请输入存档名称", default="")

        if not save_name:
            self.console.print("[red]存档名称不能为空[/red]")
            input("按回车键继续...")
            return

        # 保存游戏
        self.save_game(save_name)
        input("按回车键继续...")

    def load_save(self, saves: List[Dict[str, Any]]) -> None:
        """加载存档

        提示用户选择要加载的存档，并加载该存档。

        Args:
            saves: 存档列表
        """
        if not saves:
            self.console.print("[yellow]暂无存档文件[/yellow]")
            input("按回车键继续...")
            return

        self.clear_screen()
        self.console.print("[bold blue]📂 加载存档[/bold blue]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()

        # 显示存档列表供选择
        for idx, save in enumerate(saves, 1):
            self.console.print(f"[{idx}] {save['filename']} - {save['player_name']} (Lv.{save['level']})")

        self.console.print()
        choice = Prompt.ask("请选择要加载的存档编号", default="")

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                save_file = saves[idx]['filename']
                if self.engine.load_player(save_file):
                    self.console.print(f"[bold green]✓ 存档已加载：{save_file}[/bold green]")
                else:
                    self.console.print(f"[red]加载存档失败：{save_file}[/red]")
            else:
                self.console.print("[red]无效的存档编号[/red]")
        except ValueError:
            self.console.print("[red]请输入有效的数字[/red]")

        input("按回车键继续...")

    def delete_save(self, saves: List[Dict[str, Any]]) -> None:
        """删除存档

        提示用户选择要删除的存档，并删除该存档。

        Args:
            saves: 存档列表
        """
        if not saves:
            self.console.print("[yellow]暂无存档文件[/yellow]")
            input("按回车键继续...")
            return

        self.clear_screen()
        self.console.print("[bold red]🗑️  删除存档[/bold red]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()

        # 显示存档列表供选择
        for idx, save in enumerate(saves, 1):
            self.console.print(f"[{idx}] {save['filename']} - {save['player_name']} (Lv.{save['level']})")

        self.console.print()
        choice = Prompt.ask("请选择要删除的存档编号", default="")

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                save_file = saves[idx]['filename']

                # 确认删除
                if Confirm.ask(f"确定要删除存档 {save_file} 吗？"):
                    if self.engine.delete_save(save_file):
                        self.console.print(f"[bold green]✓ 存档已删除：{save_file}[/bold green]")
                    else:
                        self.console.print(f"[red]删除存档失败：{save_file}[/red]")
            else:
                self.console.print("[red]无效的存档编号[/red]")
        except ValueError:
            self.console.print("[red]请输入有效的数字[/red]")

        input("按回车键继续...")

    def rename_save(self, saves: List[Dict[str, Any]]) -> None:
        """重命名存档

        提示用户选择要重命名的存档，并输入新名称。

        Args:
            saves: 存档列表
        """
        if not saves:
            self.console.print("[yellow]暂无存档文件[/yellow]")
            input("按回车键继续...")
            return

        self.clear_screen()
        self.console.print("[bold purple]✏️  重命名存档[/bold purple]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()

        # 显示存档列表供选择
        for idx, save in enumerate(saves, 1):
            self.console.print(f"[{idx}] {save['filename']}")

        self.console.print()
        choice = Prompt.ask("请选择要重命名的存档编号", default="")

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                old_name = saves[idx]['filename']
                new_name = Prompt.ask("请输入新的存档名称", default="")

                if not new_name:
                    self.console.print("[red]存档名称不能为空[/red]")
                    input("按回车键继续...")
                    return

                # 重命名存档
                if self.engine.rename_save(old_name, new_name):
                    self.console.print(f"[bold green]✓ 存档已重命名：{old_name} → {new_name}[/bold green]")
                else:
                    self.console.print("[red]重命名存档失败[/red]")
            else:
                self.console.print("[red]无效的存档编号[/red]")
        except ValueError:
            self.console.print("[red]请输入有效的数字[/red]")

        input("按回车键继续...")

    def manage_equipment(self) -> None:
        """装备管理界面"""
        self.clear_screen()
        self.console.print("[bold magenta]" + "═" * 50)
        self.console.print("[bold magenta]│  🎒  装备管理  🎒  │")
        self.console.print("[bold magenta]" + "═" * 50)
        self.console.print()
        
        player = self.engine.player
        if not player:
            self.console.print("[red]玩家未初始化[/red]")
            return
        
        # 显示当前装备
        self.console.print("[bold cyan]当前装备：[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        
        table = Table(show_header=True, header_style="bold green")
        table.add_column("部位", width=10)
        table.add_column("装备", width=25)
        table.add_column("属性", width=30)
        
        # 武器
        if player.equipped_weapon:
            w = player.equipped_weapon
            table.add_row(
                "武器",
                w.display_name,
                f"攻击+{w.total_attack} 经验+{int(w.exp_bonus*100)}%"
            )
        else:
            table.add_row("武器", "[dim]无[/dim]", "-")
        
        # 护甲
        if player.equipped_armor:
            a = player.equipped_armor
            table.add_row(
                "护甲",
                a.display_name,
                f"防御+{a.total_defense} 生命+{a.total_health}"
            )
        else:
            table.add_row("护甲", "[dim]无[/dim]", "-")
        
        # 饰品
        if player.equipped_accessory:
            acc = player.equipped_accessory
            table.add_row(
                "饰品",
                acc.display_name,
                f"攻击+{acc.total_attack} 防御+{acc.total_defense}"
            )
        else:
            table.add_row("饰品", "[dim]无[/dim]", "-")
        
        self.console.print(table)
        self.console.print()
        
        # 显示总属性
        self.console.print(f"[bold]总攻击：[/bold]{player.total_attack} (基础{player.attack})")
        self.console.print(f"[bold]总防御：[/bold]{player.total_defense} (基础{player.defense})")
        self.console.print(f"[bold]总生命：[/bold]{player.total_max_health} (基础{player.max_health})")
        self.console.print(f"[bold]经验加成：[/bold]+{int(player.exp_bonus * 100)}%")
        self.console.print()
        
        # 装备管理选项
        self.console.print("[bold yellow]操作选项：[/bold yellow]")
        self.console.print("1. 查看背包")
        self.console.print("2. 装备物品")
        self.console.print("3. 卸下装备")
        self.console.print("4. 强化装备")
        self.console.print("5. 返回主菜单")
        self.console.print()
        
        choice = Prompt.ask("请选择操作", default="5")
        
        if choice == "1":
            self.show_inventory()
        elif choice == "2":
            self.equip_from_inventory()
        elif choice == "3":
            self.unequip_item()
        elif choice == "4":
            self.upgrade_equipment()
    
    def show_inventory(self) -> None:
        """显示背包"""
        self.clear_screen()
        self.console.print("[bold cyan]🎒 背包物品[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        player = self.engine.player
        if not player or not player.inventory:
            self.console.print("[yellow]背包是空的[/yellow]")
            input("按回车键继续...")
            return
        
        table = Table(show_header=True, header_style="bold green")
        table.add_column("编号", justify="right", width=5)
        table.add_column("名称", width=20)
        table.add_column("类型", width=8)
        table.add_column("属性", width=25)
        
        for idx, eq in enumerate(player.inventory, 1):
            eq_type = "武器" if eq.equipment_type.value == "weapon" else "护甲" if eq.equipment_type.value == "armor" else "饰品"
            attrs = []
            if eq.attack_bonus > 0:
                attrs.append(f"攻+{eq.total_attack}")
            if eq.defense_bonus > 0:
                attrs.append(f"防+{eq.total_defense}")
            if eq.health_bonus > 0:
                attrs.append(f"血+{eq.total_health}")
            if eq.exp_bonus > 0:
                attrs.append(f"经验+{int(eq.exp_bonus*100)}%")
            
            table.add_row(str(idx), eq.display_name, eq_type, " ".join(attrs))
        
        self.console.print(table)
        input("按回车键继续...")
    
    def equip_from_inventory(self) -> None:
        """从背包装备物品"""
        player = self.engine.player
        if not player or not player.inventory:
            self.console.print("[yellow]背包是空的[/yellow]")
            return
        
        self.show_inventory()
        
        choice = Prompt.ask("请输入要装备的编号（输入0取消）", default="0")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(player.inventory):
                equipment = player.inventory[idx]
                result = self.engine.equip_item(equipment)
                if result["success"]:
                    self.console.print(f"[green]{result['message']}[/green]")
                else:
                    self.console.print(f"[red]{result['message']}[/red]")
            elif idx != -1:
                self.console.print("[red]无效的编号[/red]")
        except ValueError:
            self.console.print("[red]请输入数字[/red]")
        
        input("按回车键继续...")
    
    def unequip_item(self) -> None:
        """卸下装备"""
        self.clear_screen()
        self.console.print("[bold cyan]选择要卸下的装备：[/bold cyan]")
        self.console.print("1. 武器")
        self.console.print("2. 护甲")
        self.console.print("3. 饰品")
        self.console.print("4. 取消")
        
        from .equipment import EquipmentType
        choice = Prompt.ask("请选择", default="4")
        
        eq_type_map = {
            "1": EquipmentType.武器,
            "2": EquipmentType.护甲,
            "3": EquipmentType.饰品
        }
        
        if choice in eq_type_map:
            result = self.engine.unequip_item(eq_type_map[choice])
            if result["success"]:
                self.console.print(f"[green]{result['message']}[/green]")
            else:
                self.console.print(f"[yellow]{result['message']}[/yellow]")
            input("按回车键继续...")
    
    def upgrade_equipment(self) -> None:
        """强化装备"""
        self.clear_screen()
        self.console.print("[bold cyan]选择要强化的装备：[/bold cyan]")
        self.console.print()
        
        player = self.engine.player
        if not player:
            return
        
        # 显示所有可强化的装备（已装备 + 背包）
        all_equipment = []
        if player.equipped_weapon:
            all_equipment.append(player.equipped_weapon)
        if player.equipped_armor:
            all_equipment.append(player.equipped_armor)
        if player.equipped_accessory:
            all_equipment.append(player.equipped_accessory)
        all_equipment.extend(player.inventory)
        
        if not all_equipment:
            self.console.print("[yellow]没有可强化的装备[/yellow]")
            input("按回车键继续...")
            return
        
        table = Table(show_header=True, header_style="bold green")
        table.add_column("编号", justify="right", width=5)
        table.add_column("名称", width=20)
        table.add_column("当前等级", width=10)
        table.add_column("强化费用", width=12)
        
        for idx, eq in enumerate(all_equipment, 1):
            cost = eq.get_upgrade_cost()
            table.add_row(str(idx), eq.display_name, f"+{eq.level - 1}", str(cost))
        
        self.console.print(table)
        self.console.print(f"\n当前经验值：{player.experience}")
        
        choice = Prompt.ask("请输入要强化的装备编号（输入0取消）", default="0")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_equipment):
                equipment = all_equipment[idx]
                result = self.engine.upgrade_equipment(equipment)
                if result["success"]:
                    self.console.print(f"[green]{result['message']}[/green]")
                else:
                    self.console.print(f"[red]{result['message']}[/red]")
            elif idx != -1:
                self.console.print("[red]无效的编号[/red]")
        except ValueError:
            self.console.print("[red]请输入数字[/red]")
        
        input("按回车键继续...")
    
    def visit_shop(self) -> None:
        """商店界面"""
        self.clear_screen()
        self.console.print("[bold magenta]" + "═" * 50)
        self.console.print("[bold magenta]│  🏪  仙缘商店  🏪  │")
        self.console.print("[bold magenta]" + "═" * 50)
        self.console.print()
        
        player = self.engine.player
        if not player:
            self.console.print("[red]玩家未初始化[/red]")
            return
        
        self.console.print(f"[bold]当前经验值：[/bold]{player.experience}")
        self.console.print()
        
        # 获取商店物品
        shop_items = self.engine.get_shop_items()
        
        table = Table(show_header=True, header_style="bold green")
        table.add_column("编号", justify="right", width=5)
        table.add_column("名称", width=20)
        table.add_column("类型", width=8)
        table.add_column("属性", width=20)
        table.add_column("价格", width=10)
        
        for idx, item in enumerate(shop_items, 1):
            eq_type = "武器" if item.equipment_type.value == "weapon" else "护甲" if item.equipment_type.value == "armor" else "饰品"
            price = self.engine.equipment_manager.calculate_buy_price(item)
            
            attrs = []
            if item.attack_bonus > 0:
                attrs.append(f"攻+{item.attack_bonus}")
            if item.defense_bonus > 0:
                attrs.append(f"防+{item.defense_bonus}")
            if item.health_bonus > 0:
                attrs.append(f"血+{item.health_bonus}")
            
            table.add_row(str(idx), item.display_name, eq_type, " ".join(attrs), str(price))
        
        self.console.print(table)
        self.console.print()
        
        self.console.print("[bold yellow]操作选项：[/bold yellow]")
        self.console.print("1-6. 购买对应编号装备")
        self.console.print("7. 出售背包物品")
        self.console.print("8. 刷新商店（消耗100经验）")
        self.console.print("9. 返回主菜单")
        
        choice = Prompt.ask("请选择操作", default="9")
        
        if choice in ["1", "2", "3", "4", "5", "6"]:
            idx = int(choice) - 1
            if 0 <= idx < len(shop_items):
                result = self.engine.buy_equipment(shop_items[idx])
                if result["success"]:
                    self.console.print(f"[green]{result['message']}[/green]")
                else:
                    self.console.print(f"[red]{result['message']}[/red]")
                input("按回车键继续...")
        elif choice == "7":
            self.sell_equipment()
        elif choice == "8":
            if player.experience >= 100:
                player.experience -= 100
                self.console.print("[green]商店已刷新！[/green]")
            else:
                self.console.print("[red]经验值不足！需要100经验值[/red]")
            input("按回车键继续...")
    
    def sell_equipment(self) -> None:
        """出售装备"""
        self.clear_screen()
        self.console.print("[bold cyan]选择要出售的物品：[/bold cyan]")
        
        player = self.engine.player
        if not player or not player.inventory:
            self.console.print("[yellow]背包是空的[/yellow]")
            input("按回车键继续...")
            return
        
        table = Table(show_header=True, header_style="bold green")
        table.add_column("编号", justify="right", width=5)
        table.add_column("名称", width=20)
        table.add_column("出售价格", width=12)
        
        for idx, eq in enumerate(player.inventory, 1):
            price = self.engine.equipment_manager.calculate_sell_price(eq)
            table.add_row(str(idx), eq.display_name, str(price))
        
        self.console.print(table)
        
        choice = Prompt.ask("请输入要出售的物品编号（输入0取消）", default="0")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(player.inventory):
                equipment = player.inventory[idx]
                result = self.engine.sell_equipment(equipment)
                if result["success"]:
                    self.console.print(f"[green]{result['message']}[/green]")
                else:
                    self.console.print(f"[red]{result['message']}[/red]")
            elif idx != -1:
                self.console.print("[red]无效的编号[/red]")
        except ValueError:
            self.console.print("[red]请输入数字[/red]")
        
        input("按回车键继续...")

    def dungeon_menu(self) -> None:
        """副本菜单"""
        self.clear_screen()
        self.console.print("[bold magenta]" + "═" * 50)
        self.console.print("[bold magenta]│  🏰  副本挑战  🏰  │")
        self.console.print("[bold magenta]" + "═" * 50)
        self.console.print()
        
        player = self.engine.player
        if not player:
            self.console.print("[red]玩家未初始化[/red]")
            return
        
        self.console.print(f"[bold]当前体力：[/bold]{player.stamina}/{player.max_stamina}")
        self.console.print(f"[bold]挑战塔最高层：[/bold]{self.engine.tower_progress.highest_level if self.engine.tower_progress else 0}")
        self.console.print(f"[bold]排名：[/bold]{self.engine.get_tower_ranking()}")
        self.console.print()
        
        self.console.print("[bold yellow]操作选项：[/bold yellow]")
        self.console.print("1. 每日副本")
        self.console.print("2. 挑战之塔")
        self.console.print("3. 返回主菜单")
        self.console.print()
        
        choice = Prompt.ask("请选择", default="3")
        
        if choice == "1":
            self.daily_dungeon_menu()
        elif choice == "2":
            self.challenge_tower_menu()
    
    def daily_dungeon_menu(self) -> None:
        """每日副本菜单"""
        self.clear_screen()
        self.console.print("[bold cyan]📅 每日副本[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        dungeons = self.engine.get_available_dungeons()
        
        if not dungeons:
            self.console.print("[yellow]暂无可用副本[/yellow]")
            input("按回车键继续...")
            return
        
        table = Table(show_header=True, header_style="bold green")
        table.add_column("编号", justify="right", width=5)
        table.add_column("名称", width=15)
        table.add_column("类型", width=10)
        table.add_column("推荐等级", width=10)
        table.add_column("体力消耗", width=10)
        table.add_column("状态", width=10)
        
        for idx, dungeon in enumerate(dungeons, 1):
            status = "✓ 已完成" if dungeon.completed else "○ 可挑战"
            dtype = "经验" if dungeon.dungeon_type.value == "exp" else "装备" if dungeon.dungeon_type.value == "equipment" else "极限"
            table.add_row(str(idx), dungeon.name, dtype, str(dungeon.recommended_level), 
                         str(dungeon.stamina_cost), status)
        
        self.console.print(table)
        self.console.print()
        
        choice = Prompt.ask("请选择要挑战的副本（输入0取消）", default="0")
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(dungeons):
                result = self.engine.start_dungeon(dungeons[idx].id)
                if result["success"]:
                    self.console.print(f"[green]{result['message']}[/green]")
                    # 简化：直接给奖励
                    self.console.print("[yellow]副本功能开发中，直接给予奖励...[/yellow]")
                else:
                    self.console.print(f"[red]{result['message']}[/red]")
            elif idx != -1:
                self.console.print("[red]无效的编号[/red]")
        except ValueError:
            self.console.print("[red]请输入数字[/red]")
        
        input("按回车键继续...")
    
    def challenge_tower_menu(self) -> None:
        """挑战之塔菜单"""
        self.clear_screen()
        self.console.print("[bold cyan]🏰 挑战之塔[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        if not self.engine.tower_progress:
            self.console.print("[red]挑战塔系统未初始化[/red]")
            input("按回车键继续...")
            return
        
        highest = self.engine.tower_progress.highest_level
        self.console.print(f"[bold]最高通关层：[/bold]{highest}")
        self.console.print(f"[bold]当前排名：[/bold]{self.engine.get_tower_ranking()}")
        self.console.print()
        
        # 显示可选层数
        start_level = max(1, highest - 2)
        end_level = min(100, highest + 3)
        
        self.console.print(f"[bold]可选层数（{start_level}-{end_level}）：[/bold]")
        for level in range(start_level, end_level + 1):
            info = self.engine.get_tower_level(level)
            if info:
                marker = "→ " if level == highest + 1 else "   "
                self.console.print(f"{marker}第{level:3d}层 - {info['monster_name']:15s} [{info['status']}]")
        
        self.console.print()
        choice = Prompt.ask("请输入要挑战的层数（输入0取消）", default="0")
        try:
            level = int(choice)
            if 1 <= level <= 100:
                result = self.engine.start_tower_challenge(level)
                if result["success"]:
                    self.console.print(f"[green]{result['message']}[/green]")
                    # 简化处理：直接通关给奖励
                    complete_result = self.engine.complete_tower_level()
                    if complete_result["success"]:
                        self.console.print(f"[bold green]🎉 {complete_result['message']}[/bold green]")
                        rewards = complete_result["rewards"]
                        self.console.print(f"获得经验值：{rewards['experience']}")
                        if "equipment_dropped" in complete_result:
                            self.console.print(f"掉落装备：[{complete_result['equipment_dropped']['quality']}]{complete_result['equipment_dropped']['name']}")
                else:
                    self.console.print(f"[red]{result['message']}[/red]")
            elif level != 0:
                self.console.print("[red]无效的层数[/red]")
        except ValueError:
            self.console.print("[red]请输入数字[/red]")
        
        input("按回车键继续...")

    def show_help(self) -> None:
        """显示帮助菜单"""
        self.clear_screen()
        self.console.print("[bold magenta]" + "═" * 60)
        self.console.print("[bold magenta]│  ❓  帮助指南  ❓  │")
        self.console.print("[bold magenta]" + "═" * 60)
        self.console.print()
        
        help_options = [
            {"id": "basics", "name": "🎮 基础操作", "desc": "游戏基本操作和流程"},
            {"id": "combat", "name": "⚔️ 战斗系统", "desc": "战斗机制和技巧"},
            {"id": "equipment", "name": "🎒 装备系统", "desc": "装备获取和强化"},
            {"id": "skills", "name": "⚡ 技能天赋", "desc": "门派技能和天赋树"},
            {"id": "dungeon", "name": "🏰 副本挑战", "desc": "副本和挑战塔"},
            {"id": "commands", "name": "📚 命令学习", "desc": "Kubernetes命令学习建议"},
            {"id": "back", "name": "🔙 返回主菜单", "desc": ""},
        ]
        
        table = Table(box=box.ROUNDED, show_header=False)
        table.add_column("选项", style="cyan", justify="right")
        table.add_column("名称", style="green")
        table.add_column("说明", style="white")
        
        for idx, opt in enumerate(help_options, 1):
            table.add_row(f"[{idx}]", opt["name"], opt["desc"])
        
        self.console.print(table)
        self.console.print()
        
        choice = Prompt.ask("请选择帮助主题", default="7")
        
        if choice == "1":
            self._show_help_basics()
        elif choice == "2":
            self._show_help_combat()
        elif choice == "3":
            self._show_help_equipment()
        elif choice == "4":
            self._show_help_skills()
        elif choice == "5":
            self._show_help_dungeon()
        elif choice == "6":
            self._show_help_commands()
    
    def _show_help_basics(self) -> None:
        """基础操作帮助"""
        self.clear_screen()
        self.console.print("[bold cyan]🎮 基础操作指南[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        self.console.print("[bold]1. 创建角色[/bold]")
        self.console.print("   首次进入游戏需要创建角色，选择门派：")
        self.console.print("   • 青云宗：经验+10%，适合新手")
        self.console.print("   • 炼狱门：经验+20%，攻击凶猛")
        self.console.print("   • 玄天宗：平衡发展，策略性强")
        self.console.print("   • 逍遥派：经验+15%，自由灵活")
        self.console.print()
        
        self.console.print("[bold]2. 主要玩法[/bold]")
        self.console.print("   • 📖 开始故事：学习新的Kubernetes命令")
        self.console.print("   • ⚔️ 修炼场：练习已学命令")
        self.console.print("   • 🏆 挑战关卡：完成挑战获得经验")
        self.console.print("   • 📝 知识问答：测试知识掌握")
        self.console.print()
        
        self.console.print("[bold]3. 修炼境界[/bold]")
        self.console.print("   凡人 → 练气期 → 筑基期 → 金丹期 → 元婴期")
        self.console.print("   → 化神期 → 大乘期 → 渡劫期 → 散仙 → 金仙")
        self.console.print()
        
        self.console.print("[bold]4. 经验获取[/bold]")
        self.console.print("   • 学习命令：+50经验")
        self.console.print("   • 完成挑战：+100经验")
        self.console.print("   • 通关章节：+500经验")
        self.console.print("   • 副本/挑战塔：大量经验")
        self.console.print()
        
        input("按回车键继续...")
    
    def _show_help_combat(self) -> None:
        """战斗系统帮助"""
        self.clear_screen()
        self.console.print("[bold cyan]⚔️ 战斗系统指南[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        self.console.print("[bold]战斗流程：[/bold]")
        self.console.print("1. 遭遇怪物 → 2. 回答问题 → 3. 造成伤害 → 4. 怪物反击")
        self.console.print()
        
        self.console.print("[bold]攻击机制：[/bold]")
        self.console.print("   • 回答正确：攻击力 ×2")
        self.console.print("   • 回答错误：攻击力 ÷2")
        self.console.print("   • 实际伤害 = 攻击 - 怪物防御")
        self.console.print()
        
        self.console.print("[bold]连击系统：[/bold]")
        self.console.print("   连续答对可获得经验加成：")
        self.console.print("   • 1-2连击：+10%")
        self.console.print("   • 3-4连击：+20%")
        self.console.print("   • 5-9连击：+30%")
        self.console.print("   • 10+连击：+50%")
        self.console.print()
        
        self.console.print("[bold]战斗技巧：[/bold]")
        self.console.print("   • 观察敌人属性，评估实力")
        self.console.print("   • 合理使用门派技能")
        self.console.print("   • 打不过时及时逃跑")
        self.console.print("   • 保持连击获得加成")
        self.console.print()
        
        input("按回车键继续...")
    
    def _show_help_equipment(self) -> None:
        """装备系统帮助"""
        self.clear_screen()
        self.console.print("[bold cyan]🎒 装备系统指南[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        self.console.print("[bold]装备类型：[/bold]")
        self.console.print("   • 武器：提升攻击力")
        self.console.print("   • 护甲：提升防御和生命值")
        self.console.print("   • 饰品：提供特殊加成")
        self.console.print()
        
        self.console.print("[bold]装备品质：[/bold]")
        self.console.print("   普通(白) < 精良(绿) < 稀有(蓝) < 史诗(紫) < 传说(橙)")
        self.console.print()
        
        self.console.print("[bold]获取途径：[/bold]")
        self.console.print("   • 战斗掉落：击败怪物有概率掉落")
        self.console.print("   • 商店购买：使用经验值购买")
        self.console.print("   • 副本奖励：通关副本获得")
        self.console.print("   • 挑战塔：高层奖励")
        self.console.print()
        
        self.console.print("[bold]装备强化：[/bold]")
        self.console.print("   • 消耗经验值强化装备")
        self.console.print("   • 每级提升10%属性")
        self.console.print("   • 品质越高，可强化等级越高")
        self.console.print()
        
        input("按回车键继续...")
    
    def _show_help_skills(self) -> None:
        """技能天赋帮助"""
        self.clear_screen()
        self.console.print("[bold cyan]⚡ 技能天赋指南[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        self.console.print("[bold]门派技能（每个门派3个）：[/bold]")
        self.console.print()
        self.console.print("[green]青云宗：[/green]")
        self.console.print("   • 稳如泰山（被动）：减伤20%")
        self.console.print("   • 道法自然（主动）：3场战斗经验+30%")
        self.console.print("   • 以柔克刚（主动）：反弹下次伤害")
        self.console.print()
        self.console.print("[red]炼狱门：[/red]")
        self.console.print("   • 狂暴（主动）：本回合攻击翻倍")
        self.console.print("   • 嗜血（被动）：吸血20%")
        self.console.print("   • 不屈（被动）：30%概率复活")
        self.console.print()
        
        self.console.print("[bold]天赋树：[/bold]")
        self.console.print("   • 攻击分支：提升输出能力")
        self.console.print("   • 防御分支：提升生存能力")
        self.console.print("   • 辅助分支：提升效率收益")
        self.console.print("   升级获得天赋点，自由分配")
        self.console.print()
        
        input("按回车键继续...")
    
    def _show_help_dungeon(self) -> None:
        """副本挑战帮助"""
        self.clear_screen()
        self.console.print("[bold cyan]🏰 副本挑战指南[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        self.console.print("[bold]每日副本：[/bold]")
        self.console.print("   • 修炼秘境：消耗10体力，获得1000经验")
        self.console.print("   • 藏宝洞窟：消耗15体力，获得装备")
        self.console.print("   • 绝境试炼：消耗20体力，获得大量奖励")
        self.console.print()
        
        self.console.print("[bold]体力系统：[/bold]")
        self.console.print("   • 最大体力：100点")
        self.console.print("   • 恢复速度：每6分钟恢复1点")
        self.console.print("   • 体力用于挑战副本")
        self.console.print()
        
        self.console.print("[bold]挑战之塔：[/bold]")
        self.console.print("   • 共100层，难度递增")
        self.console.print("   • 每10层是BOSS层")
        self.console.print("   • 高层奖励更丰厚")
        self.console.print("   • 根据最高层数获得排名")
        self.console.print()
        
        input("按回车键继续...")
    
    def _show_help_commands(self) -> None:
        """命令学习帮助"""
        self.clear_screen()
        self.console.print("[bold cyan]📚 Kubernetes命令学习建议[/bold cyan]")
        self.console.print("[dim cyan]" + "─" * 50 + "[/dim cyan]")
        self.console.print()
        
        self.console.print("[bold]学习路径：[/bold]")
        self.console.print("1. 跟随故事模式逐步学习")
        self.console.print("2. 在修炼场反复练习")
        self.console.print("3. 通过挑战检验掌握程度")
        self.console.print("4. 使用错题集针对性复习")
        self.console.print()
        
        self.console.print("[bold]命令分类：[/bold]")
        self.console.print("   • 基础操作：run, get, describe, delete")
        self.console.print("   • 部署管理：create deployment, scale")
        self.console.print("   • 服务发现：expose, services")
        self.console.print("   • 配置管理：configmap, secret")
        self.console.print("   • 故障排查：logs, exec, port-forward")
        self.console.print()
        
        self.console.print("[bold]实用建议：[/bold]")
        self.console.print("   • 理解命令背后的概念")
        self.console.print("   • 多做练习加深记忆")
        self.console.print("   • 尝试在实际环境使用")
        self.console.print("   • 建立个人命令速查表")
        self.console.print()
        
        input("按回车键继续...")

    def quit_game(self) -> None:
        """退出游戏"""
        if Confirm.ask("\n确定要退出游戏吗？"):
            self.running = False
            self.console.print("\n[bold]感谢游玩KuGame！[/bold]")
            self.console.print("[italic]愿你在Kubernetes之道上一帆风顺！[/italic]\n")

    def daily_checkin(self) -> None:
        """每日签到"""
        self.clear_screen()
        self.console.print("\n[bold yellow]📅 每日签到 📅[/bold yellow]\n")
        
        if not self.engine.player:
            self.console.print("[red]请先创建角色[/red]")
            return
        
        # 获取签到状态
        status = self.engine.player.get_checkin_status()
        
        if not status["can_checkin"]:
            self.console.print("[yellow]今天已经签到过了，明天再来吧！[/yellow]")
            self.console.print(f"[dim]连续签到: {status['consecutive_days']} 天[/dim]")
            self.console.print(f"[dim]总签到次数: {status['total_checkins']} 次[/dim]")
            return
        
        # 显示签到信息
        self.console.print("[green]✨ 签到可获奖励 ✨[/green]\n")
        
        next_reward = status["next_reward"]
        table = Table(box=box.ROUNDED)
        table.add_column("项目", style="cyan")
        table.add_column("数值", style="green")
        
        table.add_row("下次签到天数", f"第 {next_reward['day']} 天")
        table.add_row("经验奖励", str(next_reward["experience"]))
        table.add_row("体力奖励", str(next_reward["stamina"]))
        if next_reward["has_equipment"]:
            table.add_row("额外奖励", "🎁 装备")
        
        self.console.print(table)
        self.console.print()
        
        # 显示连续进度
        weekly_progress = status["weekly_progress"]
        progress_bar = "█" * weekly_progress + "░" * (7 - weekly_progress)
        self.console.print(f"[cyan]本周进度: [{progress_bar}] {weekly_progress}/7[/cyan]")
        self.console.print()
        
        # 确认签到
        if Confirm.ask("[bold yellow]是否进行今日签到？[/bold yellow]"):
            result = self.engine.player.checkin()
            
            if result["success"]:
                self.console.print(f"\n[bold green]✓ {result['message']}[/bold green]\n")
                
                # 显示奖励详情
                rewards = result["rewards"]
                reward_table = Table(box=box.ROUNDED, title="获得奖励")
                reward_table.add_column("类型", style="cyan")
                reward_table.add_column("数值", style="yellow")
                
                reward_table.add_row("经验", f"+{rewards.get('experience', 0)}")
                reward_table.add_row("体力", f"+{rewards.get('stamina', 0)}")
                
                if "equipment_quality" in rewards:
                    quality_names = {2: "精良", 3: "稀有", 4: "史诗"}
                    quality_name = quality_names.get(rewards["equipment_quality"], "装备")
                    reward_table.add_row("装备", f"🎁 {quality_name}装备")
                
                if "bonus_experience" in rewards:
                    reward_table.add_row("额外经验", f"+{rewards['bonus_experience']}")
                
                self.console.print(reward_table)
                self.console.print()
                
                # 显示当前状态
                self.console.print(f"[dim]当前等级: {result['current_level']} | "
                                 f"经验: {result['current_exp']} | "
                                 f"体力: {result['current_stamina']}/"
                                 f"{self.engine.player.max_stamina}[/dim]")
            else:
                self.console.print(f"[red]{result['message']}[/red]")
        else:
            self.console.print("[dim]已取消签到[/dim]")
        
        self.console.print()
        Prompt.ask("[dim]按回车键返回主菜单[/dim]")


def main() -> None:
    """主入口"""
    cli = CLI()
    cli.start()


if __name__ == "__main__":
    main()
