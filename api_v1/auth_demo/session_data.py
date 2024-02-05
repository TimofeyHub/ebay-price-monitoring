from fastapi import Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.cookie import get_cookie_by_session_id
from api_v1.user import get_user_by_session_id
from core.models import CookieInfo, db_helper
from .config import COOKIE_SESSION_ID_KEY


async def get_cookie_data(
    session: AsyncSession = Depends(db_helper.session_dependency),
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> CookieInfo | None:
    session_data = await get_cookie_by_session_id(
        session=session,
        session_id=session_id,
    )
    return session_data


async def get_user_by_cookie(
    session: AsyncSession = Depends(db_helper.session_dependency),
    cookie: CookieInfo = Depends(get_cookie_data),
):
    user = await get_user_by_session_id(
        session=session,
        session_id=cookie.session_id,
    )
    return user
