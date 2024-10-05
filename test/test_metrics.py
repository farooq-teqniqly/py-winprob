import pytest
import metrics as m

data = [50, 52, 54, 55, 53, 51, 52, 71, 71, 73, 75, 75, 78, 82, 86, 76, 88, 87, 89, 90, 89, 90, 90, 90, 89, 90, 91,
        90, 92, 91, 91, 91, 85, 87, 88, 89, 88, 88, 87, 83, 76, 83, 70, 36, 37, 38, 35, 32, 30, 32, 30, 33, 35,
        43, 36, 25, 27, 28, 27, 25, 13, 6, 8, 13, 22, 35, 33, 19, 30, 93, 93, 86, 73, 84, 63, 57, 63, 100]

def _assert_approx(want: float, got: float, tolerance=1e-2):
    assert got == pytest.approx(want, abs=tolerance)

def test_std_dev():
    _assert_approx(27.20, m._std_dev(data))

def test_mad():
    _assert_approx(24.74, m._mad(data))

def test_range():
    assert m._range(data) == 94

def test_var():
    _assert_approx(739.91, m._var(data))

def test_cv():
    _assert_approx(0.44, m._cv(data))

def test_rolling_std_dev():
    _assert_approx(7.06, m._rolling_std_dev(data))

def test_iqr():
    _assert_approx(53, m._iqr(data))

def test_rmse():
    _assert_approx(27.20, m._rmse(data))

def test_mean_absolute_returns():
    _assert_approx(5.79, m._mar(data))