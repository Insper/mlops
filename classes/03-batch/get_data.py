import sys
import os
import numpy as np
import random
import datetime
import calendar
import pandas as pd


class Config:
    stores = {
        5000: {
            "avg_n": 100,
            "avg_price": 350.0,
            "std": 10.0,
            "boost_weekday": [6, 7],
            "boost_months": [5, 12],
        },
        5001: {
            "avg_n": 10,
            "avg_price": 500.0,
            "std": 20.0,
            "boost_weekday": [7],
            "boost_months": [5, 12],
        },
        5002: {
            "avg_n": 25,
            "avg_price": 400.0,
            "std": 10.0,
            "boost_weekday": [7],
            "boost_months": [4, 10, 12],
        },
        5003: {
            "avg_n": 200,
            "avg_price": 220.0,
            "std": 12.0,
            "boost_weekday": [1, 3, 7],
            "boost_months": [],
        },
        5004: {
            "avg_n": 140,
            "avg_price": 415.0,
            "std": 17.0,
            "boost_weekday": [4, 6, 7],
            "boost_months": [4, 10, 12],
        },
        5005: {
            "avg_n": 50,
            "avg_price": 890.0,
            "std": 15.0,
            "boost_weekday": [6, 7],
            "boost_months": [5, 12],
        },
    }
    product_ids = np.random.randint(1000, 3000, size=30)


def generate_day_sales(store_id, year, month, day):
    config = Config.stores[store_id]
    n_sales = np.random.poisson(lam=config["avg_n"], size=1)[0]

    wk_day = datetime.date(year, month, day).weekday()

    if wk_day in config["boost_weekday"]:
        n_sales = int(n_sales * random.uniform(1.6, 1.7))

    if month in config["boost_months"]:
        n_sales = int(n_sales * random.uniform(1.45, 1.50))

    stores = [store_id] * n_sales

    products = random.choices(Config.product_ids, k=n_sales)

    prices = np.random.normal(
        loc=config["avg_price"], scale=config["std"], size=n_sales
    )

    dates = [f"{year}-{month:02d}-{day:02d}"] * n_sales

    client_ids = np.random.randint(100000, 400000, size=n_sales)

    df = pd.DataFrame(
        {
            "store_id": stores,
            "date": dates,
            "client_id": client_ids,
            "product_id": products,
            "price": prices,
        }
    )
    return df


def generate_predict_register(store_id, year, month, day):
    return pd.DataFrame(
        {
            "store_id": [store_id],
            "year": [year],
            "month": [month],
            "day": [day],
            "weekday": [datetime.date(year, month, day).weekday()],
        }
    )


def generate_data(year_from, month_from, day_from, year_to, month_to, day_to, type_):
    df = None
    for store in Config.stores:
        for year in range(year_from, year_to + 1):
            if year != year_from:
                month_from = 1
            for month in range(month_from, month_to + 1):
                if year != year_from or month != month_from:
                    day_from = 1

                if year != year_to or month != month_to:
                    day_to_ = calendar.monthrange(year, month)[1]
                else:
                    day_to_ = day_to

                for day in range(day_from, day_to_ + 1):
                    if type_ == "train":
                        new_df = generate_day_sales(
                            store_id=store, year=year, month=month, day=day
                        )
                    else:
                        new_df = generate_predict_register(
                            store_id=store, year=year, month=month, day=day
                        )
                    df = pd.concat([df, new_df])
    return df


if __name__ == "__main__":
    print("Simulate data ingestion!")

    out_type = sys.argv[-1]

    if len(sys.argv) != 8 or out_type not in ["train", "predict"]:
        print(
            "USAGE: python get_data.py <year_from> <month_from> <day_from> <year_to> <month_to> <day_to> <train/predict>"
        )
    else:
        date_args = sys.argv[1:-1]
        date_args = [int(x) for x in date_args]
        df = generate_data(*date_args, out_type)
        st_date = "-".join(sys.argv[4:-1])
        if out_type == "train":
            file_name = f"{out_type}-{st_date}.csv"
        else:
            file_name = f"{out_type}-{st_date}.parquet"

        file_path = os.path.join("../data/", file_name)
        print(f"Saving to {file_path} file...")

        if out_type == "train":
            df.to_csv(file_path, index=False)
        else:
            df.to_parquet(file_path.replace(".csv", ".parquet"), index=False)
