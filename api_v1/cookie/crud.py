from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .schemas import CreateCookieInfoSchema

from core.models import CookieInfo, User


async def create_cookie(
    session: AsyncSession,
    cookie_info: CreateCookieInfoSchema,
):
    cookie = CookieInfo(**cookie_info.model_dump())
    session.add(cookie)
    await session.commit()


async def get_cookie_by_session_id(
    session: AsyncSession,
    session_id: str,
) -> CookieInfo | None:
    stmt = select(CookieInfo).where(CookieInfo.session_id == session_id)
    cookie_result = await session.execute(stmt)
    cookie = cookie_result.scalars().one_or_none()
    return cookie


async def delete_cookie(
    session: AsyncSession,
    cookie: CookieInfo,
):
    await session.delete(cookie)
    await session.commit()
