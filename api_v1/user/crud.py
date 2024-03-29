import bcrypt
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, CookieInfo
from .schemas import CreateUserSchema, UserBaseSchema

from api_v1.collection.crud import create_new_collection


async def create_new_user(
    session: AsyncSession,
    user_info: CreateUserSchema,
    create_collection: bool = True,
):
    raw_password = user_info.password.encode("utf-8")
    hash_password = bcrypt.hashpw(raw_password, bcrypt.gensalt())
    new_user = User(
        email=user_info.email,
        password=hash_password,
    )
    session.add(new_user)
    await session.commit()

    if create_collection:
        await create_new_collection(
            session=session,
            user=new_user,
        )
    return new_user


async def get_user_by_session_id(
    session: AsyncSession,
    session_id: str,
) -> User | None:
    stmt = (
        select(User)
        .options(selectinload(User.collection))
        .join(CookieInfo.user)
        .where(CookieInfo.session_id == session_id)
    )

    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    return user
