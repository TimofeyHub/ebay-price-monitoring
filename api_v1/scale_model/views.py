from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.sold_ad.schemas import SoldAdSchema
from api_v1.sold_ad import crud
from core.config import TEMPLATES
from core.models import db_helper, ScaleModel
from core.price_visualization import build_scale_model_price_graph
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


@router.get("/{scale_model_id}/", response_model=ScaleModelSchema)
async def get_scale_model(
    scale_model: ScaleModel = Depends(get_scale_model_by_id),
):
    return scale_model


@router.patch("/{scale_model_id}/")
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


@router.delete("/{scale_model_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scale_model(
    scale_model: ScaleModel = Depends(get_scale_model_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_scale_model(session=session, scale_model=scale_model)


@router.patch("/{scale_model_id}/update_ads/")
async def update_ads_by_scale_model_id(
    scale_model: ScaleModel = Depends(get_scale_model_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.find_sold_ad_on_ebay(
        session=session,
        scale_model_id=scale_model.id,
    )


@router.get("/{scale_model_id}/all_ads/", response_model=list[SoldAdSchema])
async def get_all_ads_by_scale_model_id(
    request: Request,
    scale_model: ScaleModel = Depends(get_scale_model_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    ads_list = await crud.get_all_ads_by_scale_model_id(
        session=session,
        scale_model_id=scale_model.id,
    )

    graph_image_path = await build_scale_model_price_graph(
        scale_model=scale_model,
        ads_list=ads_list,
    )

    return TEMPLATES.TemplateResponse(
        name="all_ads_of_scale_model.html",
        context={
            "request": request,
            "scale_model": scale_model,
            "ads_list": ads_list,
            "graph_image_path": graph_image_path,
        },
    )
