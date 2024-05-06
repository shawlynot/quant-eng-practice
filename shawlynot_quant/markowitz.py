from datetime import date
from shawlynot_quant.api import PolygonClient
import pandas as pd
import numpy as np

def calculate_return(data: pd.DataFrame) -> pd.DataFrame:
    log_return = np.log(data/data.shift(1))
    return pd.DataFrame(log_return)[1:]

if __name__ == "__main__":
    data = pd.read_parquet(".cache/stocks")
    data.plot().figure.savefig(".cache/stocks.png")
    calculate_return(data).plot().figure.savefig(".cache/returns.png")
