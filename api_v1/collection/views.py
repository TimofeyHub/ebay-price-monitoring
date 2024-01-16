from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api_v1.scale_model.schemas import ScaleModelCreateSchema
from . import crud

router = APIRouter(tags=["Collection"])


@router.post("/")
async def add_scale_model_in_collection(
    scale_model_info: ScaleModelCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.add_scale_model_in_collection(
        session=session,
        scale_model_info=scale_model_info,
        collection_id=1,
    )
