from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, ScaleModel
from . import crud
from .dependecies import get_scale_model_by_id
from .schemas import ScaleModelSchema, ScaleModelCreateSchema, ScaleModelUpdateSchema

router = APIRouter(tags=["ScaleModel"])


@router.get("/", response_model=list[ScaleModelSchema])
async def get_all_scale_models(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_scale_models(session=session)


@router.post(
    "/",
    response_model=ScaleModelSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_scale_model(
    scale_model_info: ScaleModelCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_scale_model(
        session=session,
        scale_model_info=scale_model_info,
    )


@router.get("/{product_id}/", response_model=ScaleModelSchema)
async def get_scale_model(
    scale_model: ScaleModel = Depends(get_scale_model_by_id),
):
    return scale_model


@router.patch("/{product_id}/")
async def update_scale_model(
    scale_model_update: ScaleModelUpdateSchema,
    scale_model: ScaleModel = Depends(get_scale_model_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_scale_model(
        session=session,
        scale_model=scale_model,
        scale_model_update=scale_model_update,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scale_model(
    scale_model: ScaleModel = Depends(get_scale_model_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_scale_model(session=session, scale_model=scale_model)
