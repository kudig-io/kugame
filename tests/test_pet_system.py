"""宠物系统测试

测试宠物系统的各项功能。
"""
# -*- coding: utf-8 -*-

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kugame.pet_system import (
    Pet, PetType, PetRarity, PetStatus, PetSkill,
    PetManager, create_pet, generate_random_pet,
    PET_TEMPLATES
)


class TestPetSkill:
    """测试宠物技能"""
    
    def test_skill_creation(self):
        """测试技能创建"""
        skill = PetSkill(
            skill_id="test_skill",
            name="测试技能",
            description="这是一个测试技能",
            effect_type="attack",
            effect_value=50,
            cooldown=3,
        )
        
        assert skill.skill_id == "test_skill"
        assert skill.name == "测试技能"
        assert skill.cooldown == 3
        assert skill.current_cooldown == 0
    
    def test_skill_cooldown(self):
        """测试技能冷却"""
        skill = PetSkill("test", "测试", "描述", "attack", 50, cooldown=3)
        skill.current_cooldown = 3
        
        assert skill.current_cooldown == 3


class TestPet:
    """测试宠物"""
    
    def test_pet_creation(self):
        """测试宠物创建"""
        pet = Pet(
            id="pet_001",
            name="测试宠物",
            pet_type=PetType.攻击型,
            rarity=PetRarity.稀有,
            level=1,
            attack=15,
            defense=10,
            health=100,
        )
        
        assert pet.id == "pet_001"
        assert pet.name == "测试宠物"
        assert pet.pet_type == PetType.攻击型
        assert pet.rarity == PetRarity.稀有
    
    def test_pet_display_name(self):
        """测试宠物显示名称"""
        pet = Pet(
            id="pet_001",
            name="灵狐",
            pet_type=PetType.辅助型,
            rarity=PetRarity.稀有,
        )
        
        assert "[稀有]" in pet.display_name
        assert "灵狐" in pet.display_name
        assert "Lv.1" in pet.display_name
    
    def test_pet_total_stats(self):
        """测试宠物总属性计算"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.稀有,  # 1.2倍
            attack=10,
            defense=10,
            max_health=100,
        )
        
        assert pet.total_attack == 12  # 10 * 1.2
        assert pet.total_defense == 12
        assert pet.total_health == 120
    
    def test_gain_exp(self):
        """测试获得经验"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            exp=0,
            exp_to_level=100,
        )
        
        # 获得少量经验
        leveled = pet.gain_exp(50)
        assert leveled is False
        assert pet.exp == 50
        assert pet.level == 1
        
        # 获得足够经验升级
        leveled = pet.gain_exp(60)
        assert leveled is True
        assert pet.level == 2
    
    def test_level_up(self):
        """测试升级"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            level=1,
            attack=10,
            defense=5,
            max_health=100,
            attack_growth=2,
            defense_growth=1,
            health_growth=10,
        )
        
        initial_attack = pet.attack
        pet.level_up()
        
        assert pet.level == 2
        assert pet.attack > initial_attack
    
    def test_evolve(self):
        """测试进化"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            level=20,
            attack=100,
            evolution_stage=0,
        )
        
        result = pet.evolve()
        assert result is True
        assert pet.evolution_stage == 1
        assert pet.attack > 100  # 属性提升
    
    def test_feed(self):
        """测试喂食"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            loyalty=50,
            mood=50,
            health=50,
            max_health=100,
        )
        
        result = pet.feed(food_quality=2)
        
        assert result["loyalty_gain"] == 10  # 5 * 2
        assert pet.loyalty == 60
        assert pet.mood == 70
        assert pet.health == 90  # 50 + 20*2
    
    def test_play(self):
        """测试玩耍"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            mood=50,
        )
        
        result = pet.play()
        
        assert result["mood_gain"] > 0
        assert pet.mood > 50
    
    def test_train(self):
        """测试训练"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            mood=50,
            exp=0,
        )
        
        result = pet.train("attack")
        
        assert result["success"] is True
        assert result["exp_gain"] == 50
        assert pet.attack > 10  # 攻击提升
    
    def test_train_low_mood(self):
        """测试心情低落时训练"""
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            mood=10,  # 心情低落
        )
        
        result = pet.train("attack")
        
        assert result["success"] is False
    
    def test_use_skill(self):
        """测试使用技能"""
        skill = PetSkill("skill_1", "火焰爪", "造成火焰伤害", "attack", 25, cooldown=3)
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            skills=[skill],
        )
        
        result = pet.use_skill(0)
        
        assert result is not None
        assert result["success"] is True
        assert result["skill_name"] == "火焰爪"
        assert pet.skills[0].current_cooldown == 3
    
    def test_use_skill_on_cooldown(self):
        """测试使用冷却中的技能"""
        skill = PetSkill("skill_1", "火焰爪", "造成火焰伤害", "attack", 25, cooldown=3)
        skill.current_cooldown = 2
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            skills=[skill],
        )
        
        result = pet.use_skill(0)
        
        assert result["success"] is False
    
    def test_update_cooldowns(self):
        """测试更新冷却"""
        skill = PetSkill("skill_1", "火焰爪", "", "attack", 25, cooldown=3)
        skill.current_cooldown = 2
        pet = Pet(
            id="pet_001",
            name="测试",
            pet_type=PetType.攻击型,
            rarity=PetRarity.普通,
            skills=[skill],
        )
        
        pet.update_cooldowns()
        
        assert pet.skills[0].current_cooldown == 1


class TestPetTemplates:
    """测试宠物模板"""
    
    def test_templates_exist(self):
        """测试模板存在"""
        assert len(PET_TEMPLATES) > 0
        
        for template_id, template in PET_TEMPLATES.items():
            assert "name" in template
            assert "type" in template
            assert "rarity" in template
    
    def test_create_pet_from_template(self):
        """测试从模板创建宠物"""
        pet = create_pet("spirit_fox")
        
        assert pet.name == "灵狐"
        assert pet.pet_type == PetType.辅助型
        assert len(pet.skills) > 0
    
    def test_generate_random_pet(self):
        """测试生成随机宠物"""
        pet = generate_random_pet()
        
        assert pet is not None
        assert pet.name is not None


class TestPetManager:
    """测试宠物管理器"""
    
    def test_manager_creation(self):
        """测试管理器创建"""
        manager = PetManager()
        
        assert len(manager.pets) == 0
        assert manager.active_pet_id is None
    
    def test_add_pet(self):
        """测试添加宠物"""
        manager = PetManager()
        pet = create_pet("spirit_fox")
        
        result = manager.add_pet(pet)
        
        assert result is True
        assert len(manager.pets) == 1
        assert manager.active_pet_id == pet.id  # 第一个宠物自动出战
    
    def test_add_pet_max_limit(self):
        """测试宠物数量上限"""
        manager = PetManager()
        manager.MAX_PETS = 2  # 临时降低上限
        
        manager.add_pet(create_pet("spirit_fox", "pet_1"))
        manager.add_pet(create_pet("flame_tiger", "pet_2"))
        
        # 尝试添加第三个
        result = manager.add_pet(create_pet("steel_turtle", "pet_3"))
        assert result is False
    
    def test_get_pet(self):
        """测试获取宠物"""
        manager = PetManager()
        pet = create_pet("spirit_fox", "pet_001")
        manager.add_pet(pet)
        
        found = manager.get_pet("pet_001")
        not_found = manager.get_pet("non_existent")
        
        assert found is not None
        assert found.id == "pet_001"
        assert not_found is None
    
    def test_set_active_pet(self):
        """测试设置出战宠物"""
        manager = PetManager()
        pet1 = create_pet("spirit_fox", "pet_1")
        pet2 = create_pet("flame_tiger", "pet_2")
        
        manager.add_pet(pet1)
        manager.add_pet(pet2)
        
        result = manager.set_active_pet("pet_2")
        
        assert result is True
        assert manager.active_pet_id == "pet_2"
        assert pet2.is_active is True
        assert pet1.is_active is False
    
    def test_get_pets_by_type(self):
        """测试按类型获取宠物"""
        manager = PetManager()
        manager.add_pet(create_pet("spirit_fox", "pet_1"))  # 辅助型
        manager.add_pet(create_pet("flame_tiger", "pet_2"))  # 攻击型
        
        support_pets = manager.get_pets_by_type(PetType.辅助型)
        attack_pets = manager.get_pets_by_type(PetType.攻击型)
        
        assert len(support_pets) == 1
        assert len(attack_pets) == 1
    
    def test_get_summary(self):
        """测试获取摘要"""
        manager = PetManager()
        manager.add_pet(create_pet("spirit_fox"))
        
        summary = manager.get_summary()
        
        assert summary["total_pets"] == 1
        assert "by_type" in summary
        assert "by_rarity" in summary
