from core.models import ScaleModel

F1_SEARCH_BASE_URL = "https://www.ebay.com/sch/180270/i.html?_nkw="
AD_COMPLETE_STATUS = 1
ITEM_SOLD_STATUS = 1
F1_model_ebay_category = 180270

COMPLETE_URL_PARAM = f"LH_Complete={AD_COMPLETE_STATUS}"
SOLD_STATUS_URL_PARAM = f"LH_Sold={ITEM_SOLD_STATUS}"
BRAND_URL_PARAM = "Brand="
SCALE_URL_PARM = "Scale=1%253A"
CATEGORY_URL_PARAM = f"_dcat={F1_model_ebay_category}"


def create_search_url(scale_model: ScaleModel) -> str:
    keywords = "+".join(scale_model.keywords.split())
    base_url_and_keywords = f"{F1_SEARCH_BASE_URL}{keywords}"
    ad_complete = COMPLETE_URL_PARAM
    sold_status = SOLD_STATUS_URL_PARAM
    brand = f"{BRAND_URL_PARAM}{scale_model.brand}"
    scale = f"{SCALE_URL_PARM}{scale_model.scale}"
    category = CATEGORY_URL_PARAM

    param_list = [
        base_url_and_keywords,
        ad_complete,
        sold_status,
        brand,
        scale,
        category,
    ]

    return "&".join(param_list)
