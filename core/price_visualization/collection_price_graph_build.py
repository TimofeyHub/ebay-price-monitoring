import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from core.models import CollectionPrice
from static.images import COLLECTION_IMAGE_PATH_DIR


async def build_collection_price_graph(
    collection_id: int,
    collection_price_list: list[CollectionPrice],
    image_save_path: str = COLLECTION_IMAGE_PATH_DIR,
    graph_title: str = "Цена коллекции",
    x_label: str = "Дата подсчета",
    y_label: str = "Цена (руб.)",
    file_name="collection_price_{}.png",
    html_dir_path="/static/images/collection/",
    save_in_file: bool = True,
) -> str:
    file_name = file_name.format(collection_id)
    full_save_path = os.path.join(image_save_path, file_name)

    min_price_list = []
    max_price_list = []
    calculation_date_list = []
    for calculation in collection_price_list:
        min_price_list.append(calculation.min_price)
        max_price_list.append(calculation.max_price)
        calculation_date_list.append(calculation.update_date)

    plt.plot(
        calculation_date_list,
        min_price_list,
        label="Мин. цена",
        marker="o",
    )
    plt.plot(
        calculation_date_list,
        max_price_list,
        label="Макс. цена",
        marker="o",
    )

    for date, price in zip(calculation_date_list, min_price_list):
        plt.text(
            date,
            price - 20,
            price,
            fontsize=10,
            horizontalalignment="left",
            verticalalignment="top",
        )

    for date, price in zip(calculation_date_list, max_price_list):
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
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))

    if save_in_file:
        plt.savefig(full_save_path)
        plt.close()

    return os.path.join(html_dir_path, file_name)
