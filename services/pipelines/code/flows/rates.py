from io import StringIO

import polars as pl
import requests
from prefect import flow, get_run_logger, task
from prefect.blocks.system import String
from hooks.postgres.hook import copy_to_db, PostgresConnection
import datetime

import typing as t


@task(name="Get FX rates from API")
def get_rates(date: str) -> pl.DataFrame:
    """
    
    https://agicap.com/en/article/base-currency-and-quote-currency/#:~:text=Base%20currency%20and%20quote%20currency%20are%20two%20common%20expressions%20in,counter%20currency)%20is%20given%20second.
    """

    logger = get_run_logger()
    logger.info(f"Getting rates for date {date}")

    API_KEY = String.load("eod-api-key").value  # type: ignore

    URL = f"https://eodhd.com/api/eod-bulk-last-day/FOREX?api_token={API_KEY}&date={date}"

    res = requests.get(URL)

    if res.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {res.status_code}")

    return pl.read_csv(StringIO(res.text), has_header=True, try_parse_dates=True)

COLS = ["base_currency", "quote_currency", "date", "rate"]


@task(name="Transform FX rates")
def transform_rates(data: pl.DataFrame) -> pl.DataFrame:

    transformed_data = data.with_columns(
        base_currency=pl.col("Code").str.slice(0, 3),
        quote_currency=pl.col("Code").str.slice(3, 3),
        rate=pl.col("Adjusted_close"),
        date=pl.col("Date"),
    ).select(COLS)

    return transformed_data



@task(name="Sink FX rates to database")
def sink_rates(data: pl.DataFrame) -> None:
    """
    Copy the data to the database using the provided connection by a block.
    """

    conn = PostgresConnection(dbname="app", user="app_user", password="password", host="db", port=5432)

    copy_to_db(connection=conn, table="currency_rate", columns=COLS, records=data.rows())


@flow(name="Retrieve historical FX rates", log_prints=True)
def rates_by_dates(dates: t.Optional[list[str]] = None):


    # If no dates are provided as parameters, get the rates for the last day
    if dates is None:
        dates = [(datetime.date.today() - datetime.timedelta(days=1)).isoformat()]

    for date in dates:
        rates_raw = get_rates(date=date)
        transformed_rates = transform_rates(data=rates_raw)  # type: ignore
        sink_rates(data=transformed_rates)
