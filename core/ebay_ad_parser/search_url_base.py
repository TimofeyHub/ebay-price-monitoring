from pydantic import BaseModel

import constants


class SearchScaleModelInfo(BaseModel):
    keywords: str
    brand: str
    base_url: str = constants.F1_SEARCH_BASE_URL
    scale: int = 43
    category: int = constants.F1_model_ebay_category
    ad_status: int = constants.AD_COMPLETE_STATUS
    item_status: int = constants.ITEM_SOLD_STATUS


def create_search_url(search_info: SearchScaleModelInfo) -> str:
    keywords = "+".join(search_info.keywords.split())
    base_url_and_keywords = f"{search_info.base_url}{keywords}"
    ad_complete = constants.COMPLETE_URL_PARAM
    sold_status = constants.SOLD_STATUS_URL_PARAM
    brand = f"{constants.BRAND_URL_PARAM}{search_info.brand}"
    scale = f"{constants.SCALE_URL_PARM}{search_info.scale}"
    category = constants.CATEGORY_URL_PARAM

    param_list = [
        base_url_and_keywords,
        ad_complete,
        sold_status,
        brand,
        scale,
        category,
    ]

    return "&".join(param_list)
