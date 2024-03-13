import uuid
from typing import Annotated

import bcrypt
from fastapi import (
    APIRouter,
    Request,
    Depends,
    Form,
    status,
    HTTPException,
    Response,
    Cookie,
)
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.cookie import (
    create_cookie,
    delete_cookie,
    CreateCookieInfoSchema,
)
from core.config import TEMPLATES, settings
from core.models import db_helper, User, CookieInfo
from .config import COOKIE_SESSION_ID_KEY
from .session_data import get_cookie_data

router = APIRouter(tags=["Auth Demo"])


@router.get(path="/login/")
async def user_login(
    request: Request,
):
    return TEMPLATES.TemplateResponse(
        name="login_form.html",
        request=request,
    )


async def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post(path="/login/")
async def user_login(
    response: Response,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    stmt = (
        select(User).options(selectinload(User.collection)).where(User.email == email)
    )
    user_result = await session.execute(stmt)
    user = user_result.scalars().one_or_none()

    if user:
        check = bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=user.password,
        )
        if check:
            session_id = await generate_session_id()
            await create_cookie(
                session=session,
                cookie_info=CreateCookieInfoSchema(
                    session_id=session_id,
                    user_id=user.id,
                ),
            )
            redirect_response = RedirectResponse(
                url=f"{settings.api_v1_prefix}/collection/{user.collection.id}/",
                status_code=status.HTTP_302_FOUND,
            )
            redirect_response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
            return redirect_response
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Wrong password for user {user.email}",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} not found!",
        )


@router.get("/check-cookie/")
async def check_cookie(
    session_info: CookieInfo = Depends(get_cookie_data),
):
    if session_info:
        return session_info
    else:
        return {"message": "Кука не найдена, пользователь не залогинен"}


@router.get("/logout/")
async def logout(
    response: Response,
    session: AsyncSession = Depends(db_helper.session_dependency),
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    session_info: CookieInfo = Depends(get_cookie_data),
):
    redirect = RedirectResponse(
        url=f"/",
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )
    response.delete_cookie(session_id)
    await delete_cookie(
        session=session,
        cookie=session_info,
    )

    return redirect
