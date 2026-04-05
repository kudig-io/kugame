"""
用户服务层
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """用户服务"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """通过 ID 获取用户"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """通过邮箱获取用户"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    async def create(self, user_data: UserCreate) -> User:
        """创建用户"""
        # 创建用户模型
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=get_password_hash(user_data.password),
            is_active=True,
            is_verified=False,
        )
        
        self.db.add(db_user)
        await self.db.flush()
        await self.db.refresh(db_user)
        
        return db_user
    
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        user = await self.get_by_id(user_id)
        if not user:
            return None
        
        # 更新字段
        update_data = user_data.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(user)
        
        return user
    
    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """更新用户密码"""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(hashed_password=hashed_password)
        )
        await self.db.flush()
        return True
    
    async def update_last_login(self, user_id: int) -> bool:
        """更新最后登录时间"""
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login=datetime.utcnow())
        )
        await self.db.flush()
        return True
    
    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """
        验证用户凭据
        
        支持邮箱或用户名登录
        """
        # 先尝试通过邮箱查找
        user = await self.get_by_email(username)
        
        # 如果找不到，尝试通过用户名查找
        if not user:
            user = await self.get_by_username(username)
        
        if not user:
            return None
        
        # 验证密码
        if not verify_password(password, user.hashed_password):
            return None
        
        return user
    
    async def delete(self, user_id: int) -> bool:
        """删除用户（软删除）"""
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        await self.db.flush()
        return True
