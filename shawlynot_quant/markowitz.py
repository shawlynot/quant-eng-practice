from typing import Any, Tuple
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize

TRADING_DAYS = 252

NUM_PORTFOLIOS = 10000


def calculate_return(data: pd.DataFrame) -> pd.DataFrame:
    log_returns: Any = np.log(data / data.shift(1))
    return log_returns[1:]


def calculate_statistics(log_returns: pd.DataFrame) -> Tuple[pd.Series, pd.DataFrame]:
    mean_yearly_return = log_returns.mean() * TRADING_DAYS
    yearly_covariance = log_returns.cov() * TRADING_DAYS
    return mean_yearly_return, yearly_covariance


def weighted_statistics(log_returns: pd.DataFrame, weights: np.array) -> Tuple[float, float]:
    portfolio_return = (log_returns.mean() * weights).sum() * TRADING_DAYS
    portfolio_volatility = np.sqrt(weights.T @ log_returns.cov() @ weights * TRADING_DAYS)
    return portfolio_return, portfolio_volatility


def generate_portfolios(data: pd.DataFrame):
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = []
    for _ in range(NUM_PORTFOLIOS):
        weight_set = np.random.random(len(data.columns))
        weight_set /= np.sum(weight_set)
        portfolio_weights.append(weight_set)
        mean, vol = weighted_statistics(log_returns, weight_set)
        portfolio_means.append(mean)
        portfolio_risks.append(vol)
    return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risks)


def min_function_sharpe(weights, returns) -> float:
    mean, vol = weighted_statistics(returns, weights)
    return -mean / vol


def optimize_portfolio(log_returns) -> np.ndarray:
    num_stocks = len(data.columns)
    init_weights = np.random.random(num_stocks)
    # weights must sum to 1. 'eq' means the constraint function must evaluate to 0
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    # each var (i.e. weight) must be constrained between 0 and 1
    bounds = tuple((0, 1) for _ in range(num_stocks))
    result = optimize.minimize(fun=min_function_sharpe, constraints=constraints, bounds=bounds, args=log_returns,
                               x0=init_weights, method='SLSQP')
    return result['x']


def show_portfolios(returns, volatilities):
    plt.figure(figsize=(10, 6))
    plt.scatter(volatilities, returns, c=returns / volatilities, marker='o')
    plt.grid(True)
    plt.xlabel('Vol')
    plt.ylabel('Return')
    plt.colorbar(label='Sharpe Ratio')
    plt.savefig('sharpe.png')


if __name__ == "__main__":
    data = pd.read_parquet(".cache/stocks")
    data.plot().figure.savefig(".cache/stocks.png")
    log_returns = calculate_return(data)
    log_returns.plot().figure.savefig(".cache/log_returns.png")
    pweights, means, risks = generate_portfolios(log_returns)
    show_portfolios(means, risks)
    optimal_portfolio = optimize_portfolio(log_returns).round(3)
    optimal_return, optimal_risk = weighted_statistics(log_returns, optimal_portfolio)
    print(
        f"Expected return {optimal_return}, volatility {optimal_risk}, sharpe {optimal_return / optimal_risk} for "
        f"optimal portfolio {optimal_portfolio}")
