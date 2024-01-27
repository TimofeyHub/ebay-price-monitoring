from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.scale_model.schemas import (
    ScaleModelCreateSchema,
    ScaleModelSchema,
)
from core.config import TEMPLATES, settings
from core.models import db_helper
from . import crud
from .collection_price.crud import calculate_collection_price_by_collection_id

TEST_COLLECTION_ID = 1


router = APIRouter(tags=["collection"])


@router.get("/", response_model=list[ScaleModelSchema])
async def get_all_scale_models_by_collection_id(
    session: AsyncSession = Depends(db_helper.session_dependency),
    # collection_id: int = TEST_COLLECTION_ID,
):
    return await crud.get_all_scale_models_by_collection_id(
        session=session,
        collection_id=TEST_COLLECTION_ID,
    )


@router.get("/scale_model/add/")
async def add_scale_model_in_collection(
    request: Request,
):
    return TEMPLATES.TemplateResponse(
        name="add_scale_model_in_collection.html",
        request=request,
    )


@router.post("/scale_model/add/", response_class=RedirectResponse)
async def add_scale_model_in_collection(
    keywords: Annotated[str, Form()],
    year: Annotated[int, Form()],
    scale: Annotated[str, Form()],
    brand: Annotated[str, Form()],
    search_url_created_by_user: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    scale_info = ScaleModelCreateSchema(
        keywords=keywords,
        year=year,
        scale=scale,
        brand=brand,
        search_url_created_by_user=search_url_created_by_user,
    )
    await crud.add_scale_model_in_collection(
        session=session,
        scale_model_info=scale_info,
        collection_id=TEST_COLLECTION_ID,
        activate_ebay_search=True,
    )
    return RedirectResponse(
        url=f"{settings.api_v1_prefix}/collection/",
        status_code=status.HTTP_302_FOUND,
    )


@router.patch("/update_all/")
async def update_all_collection(
    # collection_id: int = TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_all_collection(
        session=session,
        collection_id=TEST_COLLECTION_ID,
    )


@router.delete("/scale_model/delete_from_collection/")
async def delete_scale_model_from_collection_by_id(
    scale_model_id: int,
    # collection_id: int = TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.delete_scale_model_from_collection_by_id(
        collection_id=TEST_COLLECTION_ID,
        scale_model_id=scale_model_id,
        session=session,
    )


@router.get("/{collection_id}/price/")
async def get_collection_price(
    collection_id=TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await calculate_collection_price_by_collection_id(
        session=session,
        collection_id=collection_id,
    )
