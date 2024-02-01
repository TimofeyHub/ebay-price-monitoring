import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from core.models import ScaleModel, SoldAd
from static.images import SCALE_MODEL_IMAGE_PATH_DIR


async def build_scale_model_price_graph(
    scale_model: ScaleModel,
    ads_list: list[SoldAd],
    image_save_path: str = SCALE_MODEL_IMAGE_PATH_DIR,
    graph_title: str = "Цена модели",
    x_label: str = "Дата продажи",
    y_label: str = "Цена (руб.)",
    file_name: str = "scale_model_{}.png",
    html_dir_path: str = "/static/images/scale_model/",
    save_in_file: bool = True,
) -> str:
    file_name = file_name.format(scale_model.id)
    full_save_path = os.path.join(image_save_path, file_name)

    sold_date_list = []
    sold_price_list = []
    for ad in ads_list:
        sold_date_list.append(ad.sold_date)
        sold_price_list.append(ad.price)

    plt.plot(sold_date_list, sold_price_list, "s-b")

    for date, price in zip(sold_date_list, sold_price_list):
        plt.text(
            date,
            price - 20,
            price,
            fontsize=10,
            horizontalalignment="left",
            verticalalignment="top",
        )
    for pos in ["right", "top"]:
        plt.gca().spines[pos].set_visible(False)
    plt.title(graph_title, fontsize=20)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))

    if save_in_file:
        plt.savefig(full_save_path)
        plt.close()

    return os.path.join(html_dir_path, file_name)
