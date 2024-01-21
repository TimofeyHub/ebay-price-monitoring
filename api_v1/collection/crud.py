from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.scale_model.crud import create_scale_model, get_scale_model
from api_v1.scale_model.schemas import ScaleModelCreateSchema
from api_v1.sold_ad.crud import create_sold_ad
from api_v1.sold_ad.schemas import SoldAdCreateSchema
from core.ebay_ad_parser.html_parser import get_sold_ebay_ad
from core.ebay_ad_parser.search_url import create_search_url
from core.models import ScaleModel, Collection, SoldAd


async def add_scale_model_in_collection(
    session: AsyncSession,
    scale_model_info: ScaleModelCreateSchema,
    collection_id: int,
    activate_ebay_search: bool,
) -> None:
    # Временная конструкция для тестирования функции
    stmt = select(Collection).where(Collection.id == collection_id)
    result: Result = await session.execute(stmt)
    collection = result.scalars().first()
    print(collection)
    if not collection:
        session.add(Collection())
        await session.commit()
    collection = await session.scalar(
        select(Collection)
        .where(Collection.id == collection_id)
        .options(selectinload(Collection.scale_models))
    )

    create_info = ScaleModelCreateSchema(
        keywords=scale_model_info.keywords,
        year=scale_model_info.year,
        scale=scale_model_info.scale,
        brand=scale_model_info.brand,
    )

    new_scale_model = await create_scale_model(
        session=session,
        scale_model_info=create_info,
    )

    collection.scale_models.append(new_scale_model)

    # На основе полученной инфы формируем url для поиска
    if activate_ebay_search:
        model_for_adding_ads = await session.scalar(
            select(ScaleModel)
            .where(ScaleModel.id == new_scale_model.id)
            .options(selectinload(ScaleModel.sold_ads))
        )
        search_url = create_search_url(new_scale_model)
        # Получаем инфу об объявлениях и записываем их в табицу объявлений
        ad_list = await get_sold_ebay_ad(search_url)
        for ad in ad_list:
            sold_ad_info = SoldAdCreateSchema(
                id_ebay=ad.id,
                sold_date=ad.sold_date,
                price=ad.price,
                ebay_link=ad.ad_link,
                scale_model_id=new_scale_model.id,
            )
            new_ad = await create_sold_ad(session=session, sold_ad_info=sold_ad_info)
            model_for_adding_ads.sold_ads.append(new_ad)


async def get_all_scale_models_by_collection_id(
    session: AsyncSession,
    collection_id: int,
):
    stmt = (
        select(ScaleModel)
        .options(selectinload(ScaleModel.collections))
        .where(Collection.id == collection_id)
    )
    result = await session.scalars(stmt)
    return list(result)


async def update_all_collection(
    session: AsyncSession,
    collection_id: int,
):
    # Получаем все модели из коллекции
    stmt = (
        select(Collection)
        .where(Collection.id == collection_id)
        .options(selectinload(Collection.scale_models))
    )
    result = await session.execute(stmt)
    collection = result.scalars().first()

    for model in collection.scale_models:
        await update_ads_by_scale_model_id(session=session, scale_model_id=model.id)


async def delete_scale_model_from_collection_by_id(
    session: AsyncSession,
    collection_id: int,
    scale_model_id: int,
):
    stmt = (
        select(Collection)
        .where(Collection.id == collection_id)
        .options(selectinload(Collection.scale_models))
    )
    result = await session.execute(stmt)
    collection = result.scalars().first()

    scale_model = await get_scale_model(session=session, scale_model_id=scale_model_id)
    collection.scale_models.remove(scale_model)
    await session.commit()
