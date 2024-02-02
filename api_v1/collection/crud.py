from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.scale_model.crud import (
    create_scale_model,
    get_scale_model,
)
from api_v1.scale_model.schemas import ScaleModelCreateSchema
from api_v1.sold_ad.crud import find_sold_ad_on_ebay
from core.models import ScaleModel, Collection
from api_v1.collection.collection_price.crud import calculate_price_by_collection_id


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
        search_url_created_by_user=scale_model_info.search_url_created_by_user,
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
        await find_sold_ad_on_ebay(
            session=session,
            scale_model_id=model_for_adding_ads.id,
        )


async def get_all_scale_models_by_collection_id(
    session: AsyncSession,
    collection_id: int,
):
    stmt = (
        select(ScaleModel)
        .join(Collection.scale_models)
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
        await find_sold_ad_on_ebay(session=session, scale_model_id=model.id)

    await calculate_price_by_collection_id(
        session=session,
        collection_id=collection_id,
        force_calculation=True,
    )


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
