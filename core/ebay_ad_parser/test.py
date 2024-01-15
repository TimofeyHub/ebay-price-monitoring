import asyncio

import search_url_base
import html_parser


async def main():
    ad = search_url_base.SearchUrlInfo(
        keywords="bottas 2023",
        brand="Spark",
        scale=43,
    )
    link = search_url_base.create_search_url(search_info=ad)
    ads = await html_parser.get_sold_ebay_ad(link)
    for ad in ads:
        print(ad.id)
        print(ad.price)
        print(ad.sold_date)
        print(ad.ad_link)


asyncio.run(main())
