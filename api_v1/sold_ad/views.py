from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
    old_ad_info: SoldAdCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_sold_ad(
        session=session,
        sold_ad_info=old_ad_info,
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


@router.delete("/{sold_ad_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sold_ad(
    sold_ad: SoldAd = Depends(get_sold_ad_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    await crud.delete_scale_model(session=session, sold_ad=sold_ad)
