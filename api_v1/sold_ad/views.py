from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import TEMPLATES, settings
from core.models import db_helper, SoldAd
from . import crud
from .dependecies import get_sold_ad_by_id
from .schemas import SoldAdSchema, SoldAdCreateSchema, SoldAdUpdateSchema

router = APIRouter(tags=["SoldAd"])


@router.get("/", response_model=list[SoldAdSchema])
async def get_all_sold_ads(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_all_sold_ads(session=session)


@router.post(
    "/",
    response_model=SoldAdSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_sold_ad(
    sold_ad_info: SoldAdCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_sold_ad(
        session=session,
        sold_ad_info=sold_ad_info,
    )


@router.get("/{sold_ad_id}/", response_model=SoldAdSchema)
async def get_sold_ad(
    sold_ad: SoldAd = Depends(get_sold_ad_by_id),
):
    return sold_ad


@router.patch("/{sold_ad_id}/")
async def update_sold_ad(
    sold_ad_update: SoldAdUpdateSchema,
    sold_ad: SoldAd = Depends(get_sold_ad_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_sold_ad(
        session=session,
        sold_ad=sold_ad,
        sold_ad_update=sold_ad_update,
    )


@router.api_route(
    "/{sold_ad_id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    methods=["GET", "POST"],
)
async def exclude_sold_ad_from_price_calculation_by_id(
    request: Request,
    sold_ad: SoldAd = Depends(get_sold_ad_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if request.method == "GET":
        return TEMPLATES.TemplateResponse(
            name="sold_ad_delete_confirmation.html",
            context={
                "request": request,
                "sold_ad": sold_ad,
            },
        )
    else:
        await crud.exclude_sold_ad_from_price_calculation(
            session=session,
            sold_ad=sold_ad,
        )
        return RedirectResponse(
            url=f"{settings.api_v1_prefix}/scale-models/{sold_ad.scale_model_id}/all_ads",
            status_code=status.HTTP_302_FOUND,
        )
