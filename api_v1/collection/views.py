from typing import Annotated

from fastapi import APIRouter, Depends, Request, Form, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.scale_model.crud import get_min_max_prices_by_scale_model_id
from api_v1.scale_model.schemas import (
    ScaleModelCreateSchema,
)
from api_v1.scale_model.views import get_scale_model_by_id
from core.config import TEMPLATES, settings
from core.models import db_helper, Collection
from core.price_visualization import build_collection_price_graph
from . import crud
from .dependecies import get_collection_by_id
from .collection_price.crud import (
    calculate_price_by_collection_id,
    get_all_prices_by_collection_id,
)

TEST_COLLECTION_ID = 1


router = APIRouter(tags=["collection"])


@router.get("/{collection_id}/")
async def get_all_scale_models_by_collection_id(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_dependency),
    collection: Collection = Depends(get_collection_by_id),
):
    prices = None
    collection_price = None
    graph_image_path = None

    scale_list = await crud.get_all_scale_models_by_collection_id(
        session=session,
        collection_id=collection.id,
    )
    if scale_list:
        scale_model_id_list = [scale_model.id for scale_model in scale_list]

        prices = await get_min_max_prices_by_scale_model_id(
            session=session,
            scale_model_id_list=scale_model_id_list,
        )

        collection_price = await calculate_price_by_collection_id(
            session=session,
            collection_id=collection.id,
        )

        collection_price_list = await get_all_prices_by_collection_id(
            session=session,
            collection_id=collection.id,
        )
        graph_image_path = await build_collection_price_graph(
            collection_id=collection.id,
            collection_price_list=collection_price_list,
        )

    return TEMPLATES.TemplateResponse(
        name="collection.html",
        context={
            "request": request,
            "collection": collection,
            "scale_list": scale_list,
            "prices": prices,
            "collection_price": collection_price,
            "graph_image_path": graph_image_path,
        },
    )


@router.get("/scale_model/add/")
async def add_scale_model_in_collection(
    request: Request,
):
    return TEMPLATES.TemplateResponse(
        name="add_scale_model_in_collection.html",
        request=request,
    )


@router.post("/scale_model/add/", response_class=RedirectResponse)
async def add_scale_model_in_collection(
    keywords: Annotated[str, Form()],
    year: Annotated[int, Form()],
    scale: Annotated[str, Form()],
    brand: Annotated[str, Form()],
    search_url_created_by_user: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    scale_info = ScaleModelCreateSchema(
        keywords=keywords,
        year=year,
        scale=scale,
        brand=brand,
        search_url_created_by_user=search_url_created_by_user,
    )
    await crud.add_scale_model_in_collection(
        session=session,
        scale_model_info=scale_info,
        collection_id=TEST_COLLECTION_ID,
        activate_ebay_search=True,
    )
    return RedirectResponse(
        url=f"{settings.api_v1_prefix}/collection/",
        status_code=status.HTTP_302_FOUND,
    )


@router.post("/update_all/")
async def update_all_collection(
    # collection_id: int = TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.update_all_collection(
        session=session,
        collection_id=TEST_COLLECTION_ID,
    )
    return RedirectResponse(
        url=f"{settings.api_v1_prefix}/collection/",
        status_code=status.HTTP_302_FOUND,
    )


@router.api_route("/scale_model/{scale_model_id}/delete/", methods=["GET", "POST"])
async def delete_scale_model_from_collection_by_id(
    request: Request,
    scale_model=Depends(get_scale_model_by_id),
    # collection_id: int = TEST_COLLECTION_ID,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    if request.method == "GET":
        return TEMPLATES.TemplateResponse(
            name="scale_model_delete_confirmation.html",
            context={
                "request": request,
                "scale_model": scale_model,
            },
        )
    else:
        await crud.delete_scale_model_from_collection_by_id(
            collection_id=TEST_COLLECTION_ID,
            scale_model_id=scale_model.id,
            session=session,
        )
        return RedirectResponse(
            url=f"{settings.api_v1_prefix}/collection/",
            status_code=status.HTTP_302_FOUND,
        )
