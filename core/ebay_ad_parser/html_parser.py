import re

import aiohttp
from bs4 import BeautifulSoup
from pydantic import BaseModel


class EbayAdInfo(BaseModel):
    id: str
    price: int
    sold_date: str
    ad_link: str


async def get_sold_ebay_ad(search_url: str) -> list[EbayAdInfo] | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as response:
            final_ad_list = []

            res_text = await response.text()
            base_soup = BeautifulSoup(res_text, "html.parser")
            # Находим список из объявлений
            ad_list_base = str(
                base_soup.find_all("ul", "srp-results srp-list clearfix")[0]
            )
            # Отделяем нужные объявления от "рекомендашек"
            needed_ad_list_base = (
                ad_list_base.split(
                    '<li class="srp-river-answer srp-river-answer--REWRITE_START"'
                )[0]
            ) + "/ul"
            # Разделяем каждое из объявлений на отдельные сущности
            needed_ad_list = (
                BeautifulSoup(needed_ad_list_base, "html.parser")
            ).find_all("li", class_=re.compile("s-item__pl-on-bottom"))

            # Из каждого объявления берем нужную информацию нужную информацию
            for ad_info in needed_ad_list:
                ad_id = ad_info.get("id")
                ad_base_soup = BeautifulSoup(str(ad_info), "html.parser")
                link = ad_base_soup.find("a", class_="s-item__link").get("href")
                raw_price = str(
                    ad_base_soup.find("span", class_=re.compile("s-item__price"))
                )
                price = (
                    re.findall(r"\d[\d\s,]*(?=руб\.|р\.)", raw_price)[0]
                    .replace("\xa0", "")
                    .replace(" ", "")
                    .replace(",", ".")
                )
                price = round(float(price))

                ru_date_pattern = r"\b\d{1,2}\s(?:янв|фев|мар|апр|май|июн|июл|авг|сен|окт|нояб|дек)\.\s\d{4}\b"
                raw_date = str(ad_base_soup.find("span", class_="POSITIVE"))
                print(raw_date)
                sold_date = re.findall(ru_date_pattern, raw_date, flags=re.IGNORECASE)[
                    0
                ]
                ad = EbayAdInfo(
                    id=ad_id,
                    price=price,
                    sold_date=sold_date,
                    ad_link=link,
                )

                final_ad_list.append(ad)
            return final_ad_list
