from datetime import date
from polygon import RESTClient
from polygon.rest.models import Agg
import os
import pandas as pd

class PolygonClient:
    client: RESTClient

    def __init__(self) -> None:
        self.client = RESTClient(os.environ.get("POLYGON_KEY"))

    def historical_for_tickers(self, tickers: list[str], start: date, end: date) -> pd.DataFrame:
        out: dict = {}
        for ticker in tickers:
            from_api: list[Agg] = self.client.get_aggs(
                ticker=ticker, from_=start, to=end, multiplier=1, timespan="day")
            out[ticker] = pd.Series([agg.open for agg in from_api], index=[
                                    agg.timestamp for agg in from_api])
        return pd.DataFrame(out)


if __name__ == "__main__":
    stocks = ['AAPL', 'PG', 'GOOG', 'NVO', 'JPM']
    start_date = date(2022, 5, 1)
    end_date = date(2024, 5, 1)

    client = PolygonClient()
    data = client.historical_for_tickers(stocks, start_date, end_date)
    data.to_parquet(".cache/stocks")
