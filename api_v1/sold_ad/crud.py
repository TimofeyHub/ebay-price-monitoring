from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SoldAd
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


async def delete_sold_ad(
    session: AsyncSession,
    sold_ad: SoldAd,
) -> None:
    await session.delete(sold_ad)
    await session.commit()
