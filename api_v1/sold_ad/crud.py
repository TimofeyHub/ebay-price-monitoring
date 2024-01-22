from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.ebay_ad_parser import get_sold_ebay_ad
from core.models import SoldAd, ScaleModel
from .schemas import SoldAdCreateSchema, SoldAdUpdateSchema


async def get_all_sold_ads(session: AsyncSession) -> list[SoldAd]:
    stmt = select(SoldAd).order_by(SoldAd.id)
    result: Result = await session.execute(stmt)
    sold_ads = result.scalars().all()
    return list(sold_ads)


async def get_sold_ad(
    session: AsyncSession,
    sold_ad_id: int,
) -> SoldAd | None:
    return await session.get(SoldAd, sold_ad_id)


async def create_sold_ad(
    session: AsyncSession,
    sold_ad_info: SoldAdCreateSchema,
) -> SoldAd:
    sold_ad = SoldAd(**sold_ad_info.model_dump())
    session.add(sold_ad)
    await session.commit()
    return sold_ad


async def update_sold_ad(
    session: AsyncSession,
    sold_ad: SoldAd,
    sold_ad_update: SoldAdUpdateSchema,
) -> SoldAd:
    for name, value in sold_ad_update.model_dump(exclude_unset=True).items():
        setattr(sold_ad, name, value)
    await session.commit()
    return sold_ad


async def delete_scale_model(
    session: AsyncSession,
    sold_ad: SoldAd,
) -> None:
    await session.delete(sold_ad)
    await session.commit()


async def create_ads_from_url(
    url: str,
    scale_model: ScaleModel,
    session: AsyncSession,
):
    ad_list = await get_sold_ebay_ad(url)
    for sold_ad_info in ad_list:
        new_ad = await create_sold_ad(session=session, sold_ad_info=sold_ad_info)
        scale_model.sold_ads.append(new_ad)
