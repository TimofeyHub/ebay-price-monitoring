from fastapi import APIRouter

from .scale_model.views import router as scale_model_router
from .sold_ad.views import router as sold_ad_router
from .collection.views import router as collection_router
from .user.views import router as user_router

router = APIRouter()
router.include_router(router=scale_model_router, prefix="/scale-models")
router.include_router(router=sold_ad_router, prefix="/sold_ad")
router.include_router(router=collection_router, prefix="/collection")
router.include_router(router=user_router, prefix="/user")
