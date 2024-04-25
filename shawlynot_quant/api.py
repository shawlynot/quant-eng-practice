from datetime import date
from polygon import RESTClient
from polygon.rest.models import Agg
import os
import pandas as pd


class PolygonClient:
    client: RESTClient
    
    def __init__(self) -> None:
        self.client = RESTClient(os.environ.get("POLYGON_KEY"))

    def historical_for_tickers(self, tickers: list[str], start: date, end: date):
        
        for ticker in tickers:
            from_api: list[Agg] = self.client.get_aggs(ticker=ticker, from_=start, to=end, multiplier=1, timespan="day")
            # TODO: PANDAS
            
            
            
            