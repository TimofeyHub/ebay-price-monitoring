import datetime

from sqlalchemy import select, desc, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.sold_ad.crud import create_sold_ad
from core.ebay_ad_parser import create_search_url, get_sold_ebay_ad
from core.models import ScaleModel, SoldAd
from .schemas import ScaleModelCreateSchema, ScaleModelUpdateSchema


async def get_all_scale_models(session: AsyncSession) -> list[ScaleModel]:
    stmt = select(ScaleModel).order_by(ScaleModel.id)
    result: Result = await session.execute(stmt)
    scale_models = result.scalars().all()
    return list(scale_models)


async def get_scale_model(
    session: AsyncSession,
    scale_model_id: int,
) -> ScaleModel | None:
    return await session.get(ScaleModel, scale_model_id)


async def create_scale_model(
    session: AsyncSession,
    scale_model_info: ScaleModelCreateSchema,
) -> ScaleModel:
    scale_model = ScaleModel(**scale_model_info.model_dump())
    session.add(scale_model)
    await session.commit()
    return scale_model


async def update_scale_model(
    session: AsyncSession,
    scale_model: ScaleModel,
    scale_model_update: ScaleModelUpdateSchema,
) -> ScaleModel:
    for name, value in scale_model_update.model_dump(exclude_unset=True).items():
        setattr(scale_model, name, value)
    await session.commit()
    return scale_model


async def delete_scale_model(
    session: AsyncSession,
    scale_model: ScaleModel,
) -> None:
    await session.delete(scale_model)
    await session.commit()


async def update_ads_by_scale_model_id(
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


async def get_all_ads_by_scale_model_id(
    session: AsyncSession,
    scale_model_id: int,
):
    stmt = (
        select(SoldAd)
        .join(ScaleModel.sold_ads)
        .where(ScaleModel.id == scale_model_id)
        .order_by(desc(SoldAd.sold_date))
    )
    result = await session.scalars(stmt)
    return list(result)


async def get_min_max_prices_by_scale_model_id(
    session: AsyncSession,
    scale_model_id_list: list[int],
    calculation_interval_in_days: int = 90,
):
    stmt = (
        select(ScaleModel.id, func.min(SoldAd.price), func.max(SoldAd.price))
        .join(ScaleModel.sold_ads)
        .where(
            ScaleModel.id.in_(scale_model_id_list),
            SoldAd.sold_date.between(
                datetime.datetime.utcnow()
                - datetime.timedelta(days=calculation_interval_in_days),
                datetime.datetime.utcnow(),
            ),
        )
        .group_by(ScaleModel.id)
    )
    result_dict = {}
    result = list(await session.execute(stmt))

    # Временная конструкция, убрать при достижении оптимального решения
    for price_info in result:
        result_dict[price_info[0]] = {
            "min_price": price_info[1],
            "max_price": price_info[2],
        }

    return result_dict
