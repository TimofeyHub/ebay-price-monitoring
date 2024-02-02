from sqlalchemy import select, update
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.ebay_ad_parser import create_search_url, get_sold_ebay_ad
from core.models import ScaleModel, SoldAd
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


async def find_sold_ad_on_ebay(
    session: AsyncSession,
    scale_model_id: int,
):
    # Получаем модель
    stmt = (
        select(ScaleModel)
        .where(ScaleModel.id == scale_model_id)
        .options(selectinload(ScaleModel.sold_ads))
    )
    scale_mode_result = await session.execute(stmt)
    scale_model = scale_mode_result.scalars().first()

    # Получаем все ebay_id объявлений
    stmt = select(SoldAd.id_ebay).where(SoldAd.scale_model_id == scale_model_id)
    ids_ebay_result = await session.execute(stmt)
    id_ebay_list = ids_ebay_result.scalars().all()

    # Получаем инфу об объявлениях и записываем их в табицу объявлений
    search_url = create_search_url(scale_model)
    ad_list = await get_sold_ebay_ad(
        search_url=search_url,
        scale_model_id=scale_model.id,
    )

    # Добавляем новые объявления
    for ad_info in ad_list:
        if ad_info.id_ebay not in id_ebay_list:
            new_ad = await create_sold_ad(
                session=session,
                sold_ad_info=ad_info,
            )
            scale_model.sold_ads.append(new_ad)


async def exclude_sold_ad_from_price_calculation(
    session: AsyncSession,
    sold_ad: SoldAd,
):
    stmt = (
        update(SoldAd)
        .where(SoldAd.id == sold_ad.id)
        .values({"include_in_calculation": False})
    )
    await session.execute(stmt)
    await session.commit()
