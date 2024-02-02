from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.config import TEMPLATES, settings

from .schemas import CreateUserSchema
from .crud import create_new_user

router = APIRouter(tags=["User"])


@router.get(path="/registration/")
async def user_registration(
    request: Request,
):
    return TEMPLATES.TemplateResponse(
        name="registration_form.html",
        request=request,
    )


@router.post(path="/registration/")
async def user_registration(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    new_user_info = CreateUserSchema(
        email=email,
        password=password,
    )
    new_user = await create_new_user(
        session=session,
        user_info=new_user_info,
    )

    return RedirectResponse(
        url=f"{settings.api_v1_prefix}/collection/{new_user.c}",
        status_code=status.HTTP_302_FOUND,
    )
