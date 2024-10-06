from tarfile import data_filter
from typing import List, Any, Union

import numpy as np

def calculate_volatility_metrics(data: List[int]) -> dict:
    """
    Calculates various volatility metrics for the provided data.

    Args:
        data: A list of integers representing the dataset for which volatility metrics are computed.

    Returns:
        A dictionary containing the calculated volatility metrics:
            - std_dev: Standard deviation of the data.
            - mean_abs_dev: Mean absolute deviation of the data.
            - range: Range of the data.
            - var: Variance of the data.
            - cv: Coefficient of variation of the data.
            - rolling_std_dev: Rolling standard deviation of the data.
            - iqr: Interquartile range of the data.
            - rmse: Root mean square error of the data.
            - mean_abs_returns: Mean absolute returns of the data.
            - squared_returns: Squared returns of the data.
    """
    return dict(
        std_dev=_std_dev(data),
        mean_abs_dev=_mad(data),
        range=_range(data),
        var=_var(data),
        cv=_cv(data),
        rolling_std_dev=_rolling_std_dev(data),
        iqr=_iqr(data),
        rmse=_rmse(data),
        mean_abs_returns=_mar(data),
        squared_returns=_squared_returns(data)
    )

def _mean(data: Union[List[int], np.ndarray[Any, np.dtype]]) -> float:
    return float(np.mean(data))

def _std_dev(data: Union[List[int], List[float]]) -> float:
    return float(np.std(data))

def _mad(data: List[int]) -> float:
    return np.mean(np.abs(data - np.mean(data)))

def _range(data: List[int]) -> float:
    return np.max(data) - np.min(data)

def _var(data: List[int]) -> float:
    return float(np.var(data))

def _cv(data: List[int]) -> float:
    return _std_dev(data) / _mean(data)

def _rolling_std_dev(data: List[int], window: int=5) -> float:
    return _std_dev([_std_dev(data[i:i+5]) for i in range(len(data) - (window - 1))])

def _iqr(data: List[int]) -> float:
    q75, q25 = np.percentile(data, [75, 25])
    return q75 - q25

def _rmse(data: List[int]) -> float:
    data = np.array(data)  # Convert list to NumPy array for element-wise operations
    mean_data = _mean(data)
    return np.sqrt(np.mean((data - mean_data) ** 2))

def _mar(data: List[int]) -> float:
    absolute_returns = np.abs(np.diff(data))
    return _mean(absolute_returns)

def _squared_returns(data: List[int], lag:int=1) -> float:
    squared_returns = np.diff(data) ** 2
    return float(np.corrcoef(squared_returns[:-lag], squared_returns[lag:])[0, 1])