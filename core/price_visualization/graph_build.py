from dataclasses import dataclass
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from static.images import COLLECTION_IMAGE_PATH_DIR, SCALE_MODEL_IMAGE_PATH_DIR
from core.models import ScaleModel, SoldAd


@dataclass
class GraphInfo:
    image_save_path: str
    graph_title: str
    x_label: str
    y_label: str


COLLECTION_GRAPH_INFO = {
    "image_save_path": COLLECTION_IMAGE_PATH_DIR,
    "graph_title": "Цена колекции",
    "x_label": "Дата подсчета",
    "y_label": "Общая цена (руб.)",
}


async def build_price_graph(
    date_list: list,
    price_list: list[int],
    graph_info: GraphInfo,
    save_in_file: bool = True,
):
    plt.plot(date_list, price_list, "s-b")

    for date, price in zip(date_list, price_list):
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
    plt.title(graph_info.graph_title, fontsize=20)
    plt.xlabel(graph_info.x_label)
    plt.ylabel(graph_info.y_label)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))

    if save_in_file:
        plt.savefig(graph_info.image_save_path)
        plt.close()


async def build_scale_model_price_graph(
    scale_model: ScaleModel,
    ads_list: list[SoldAd],
    image_save_path: str = SCALE_MODEL_IMAGE_PATH_DIR,
    graph_title: str = "Цена модели",
    x_label: str = "Дата продажи",
    y_label: str = "Цена (руб.)",
    file_name="scale_model_{}.png",
    html_dir_path="/static/images/scale_model/",
) -> str:
    file_name = file_name.format(scale_model.id)

    graph_info = GraphInfo(
        image_save_path=os.path.join(image_save_path, file_name),
        graph_title=graph_title,
        x_label=x_label,
        y_label=y_label,
    )

    sold_date_list = []
    sold_price_list = []
    for ad in ads_list:
        sold_date_list.append(ad.sold_date)
        sold_price_list.append(ad.price)

    await build_price_graph(
        date_list=sold_date_list,
        price_list=sold_price_list,
        graph_info=graph_info,
        save_in_file=True,
    )
    return os.path.join(html_dir_path, file_name)
