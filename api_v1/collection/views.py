from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.scale_model.schemas import ScaleModelCreateSchema, ScaleModelSchema
from core.models import db_helper
from . import crud
from .collection_price.crud import calculate_collection_price_by_collection_id

TEST_COLLECTION_ID = 1


router = APIRouter(tags=["Collection"])


@router.get("/{collection_id}", response_model=list[ScaleModelSchema])
async def get_all_scale_models_by_collection_id(
    session: AsyncSession = Depends(db_helper.session_dependency),
    collection_id: int = TEST_COLLECTION_ID,
):
    return await crud.get_all_scale_models_by_collection_id(
        session=session,
        collection_id=collection_id,
    )


@router.post("/{collection_id}/scale_model/add")
async def add_scale_model_in_collection(
    scale_model_info: ScaleModelCreateSchema,
    collection_id: int = TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.add_scale_model_in_collection(
        session=session,
        scale_model_info=scale_model_info,
        collection_id=collection_id,
        activate_ebay_search=True,
    )


@router.patch("/{collection_id}/update_all")
async def update_all_collection(
    collection_id: int = TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_all_collection(
        session=session,
        collection_id=collection_id,
    )


@router.delete("/{collection_id}/scale_model/delete_from_collection")
async def delete_scale_model_from_collection_by_id(
    scale_model_id: int,
    collection_id: int = TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.delete_scale_model_from_collection_by_id(
        collection_id=collection_id,
        scale_model_id=scale_model_id,
        session=session,
    )


@router.get("/{collection_id}/price")
async def get_collection_price(
    collection_id=TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await calculate_collection_price_by_collection_id(
        session=session,
        collection_id=collection_id,
    )
