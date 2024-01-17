from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.scale_model.schemas import ScaleModelCreateSchema, ScaleModelSchema
from api_v1.sold_ad.schemas import SoldAdSchema
from . import crud

router = APIRouter(tags=["Collection"])


@router.get("/", response_model=list[ScaleModelSchema])
async def get_all_scale_models(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_models_from_collection(session=session, collection_id=1)


@router.get("/ads", response_model=list[SoldAdSchema])
async def get_all_ads_by_model_id(
    model_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_ads_by_scale_model_id(session=session, model_id=1)


@router.post("/")
async def add_scale_model_in_collection(
    scale_model_info: ScaleModelCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.add_scale_model_in_collection(
        session=session,
        scale_model_info=scale_model_info,
        collection_id=1,
        activate_ebay_search=True,
    )
