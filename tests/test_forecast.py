from datetime import datetime, timedelta, timezone

import pytest

from .adapters import pinball, seasonal, valid_origins

pytestmark = pytest.mark.assignment


def test_window_can_borrow_history_across_split():
    start = datetime(2023, 1, 1, tzinfo=timezone.utc)
    hours = [start + timedelta(hours=i) for i in range(-168, 24)]
    flags = [True] * len(hours)
    assert list(valid_origins(hours, flags, start, start + timedelta(hours=24))) == [start]
    flags[0] = False
    assert not list(valid_origins(hours, flags, start, start + timedelta(hours=24)))


@pytest.mark.parametrize("period", [24, 168])
def test_seasonal_lead_alignment(period):
    history = [[h, 0, 2*h] for h in range(168)]
    actual = seasonal(history, period)
    assert len(actual) == 24
    assert list(actual[0]) == history[-period]
    assert list(actual[-1]) == history[-period + 23]


def test_asymmetric_loss():
    assert pinball([4., 3.], [2., 4.], .75) == pytest.approx(.875)
