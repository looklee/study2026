# 用户认证与安全模块

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.config import settings
from app.core.database import get_db
from app.models import User, Session, Device


# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


class Token(BaseModel):
    """访问令牌"""
    access_token: str
    token_type: str
    expires_in: int


class TokenData(BaseModel):
    """令牌数据"""
    user_id: Optional[int] = None
    username: Optional[str] = None


class UserCreate(BaseModel):
    """用户创建"""
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    """用户登录"""
    username: str
    password: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
    """认证用户"""
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == token_data.user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    return user


async def create_user_session(
    db: AsyncSession,
    user_id: int,
    device_id: str,
    session_data: Dict[str, Any] = None
) -> Session:
    """创建用户会话"""
    expires_at = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRE_DAYS)
    
    session = Session(
        session_id=f"sess_{datetime.utcnow().timestamp()}",
        user_id=user_id,
        device_id=device_id,
        session_data=session_data or {},
        is_active=True,
        expires_at=expires_at
    )
    
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return session


async def get_user_device(db: AsyncSession, device_id: str) -> Optional[Device]:
    """获取用户设备"""
    result = await db.execute(select(Device).where(Device.device_id == device_id))
    return result.scalar_one_or_none()


async def create_or_update_device(
    db: AsyncSession,
    device_id: str,
    platform: str = "unknown",
    browser: str = None,
    language: str = "zh-CN",
    timezone: str = "Asia/Shanghai",
    user_id: int = None
) -> Device:
    """创建或更新设备"""
    device = await get_user_device(db, device_id)
    
    if device:
        device.last_seen_at = datetime.utcnow()
        device.login_count += 1
        if user_id:
            device.user_id = user_id
    else:
        device = Device(
            device_id=device_id,
            platform=platform,
            browser=browser,
            language=language,
            timezone=timezone,
            user_id=user_id
        )
        db.add(device)
    
    await db.commit()
    await db.refresh(device)
    return device
