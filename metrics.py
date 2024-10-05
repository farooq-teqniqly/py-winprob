from typing import List

import numpy as np

def _mean(data: List[int]) -> float:
    return np.mean(data)

def _std_dev(data: List[int]) -> float:
    return np.std(data)

def _mad(data: List[int]) -> float:
    return np.mean(np.abs(data - np.mean(data)))

def _range(data: List[int]) -> float:
    return np.max(data) - np.min(data)

def _var(data: List[int]) -> float:
    return np.var(data)

def _cv(data: List[int]) -> float:
    return _std_dev(data) / _mean(data)

def _rolling_std_dev(data: List[int], window: int=5) -> float:
    return _std_dev([_std_dev(data[i:i+5]) for i in range(len(data) - (window - 1))])

def _iqr(data: List[int]) -> float:
    q75, q25 = np.percentile(data, [75, 25])
    return q75 - q25

def _rmse(data: List[int]) -> float:
    return np.sqrt(_mean((data - _mean(data)) ** 2))

def _mar(data: List[int]) -> float:
    absolute_returns = np.abs(np.diff(data))
    return _mean(absolute_returns)

def _squared_returns(data: List[int], lag:int) -> float:
    squared_returns = np.diff(data) ** 2
    return np.corrcoef(squared_returns[:-lag], squared_returns[lag:])[0, 1]