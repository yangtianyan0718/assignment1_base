import pytest
from course.physics import State, advance

pytestmark = pytest.mark.smoke


def test_noon_surplus():
    end = advance(State(), pump=10, charge=5)
    assert end.battery_mwh == pytest.approx(14.75)
    assert end.upper_water_m3 == pytest.approx(110000 + 9 * 3.6e9 / 1962000)


def test_hydro_round_trip():
    start = State()
    pumped = advance(start, pump=20)
    assert pumped.upper_water_m3 - start.upper_water_m3 == pytest.approx(33027.52, abs=.01)
    assert advance(pumped, generate=16.2).upper_water_m3 == pytest.approx(start.upper_water_m3)


@pytest.mark.parametrize("state,action", [
    (State(upper_water_m3=0), {"generate": 1}),
    (State(upper_water_m3=220000), {"pump": 1}),
    (State(battery_mwh=2), {"discharge": 1}),
    (State(), {"pump": 1, "generate": 1}),
    (State(), {"charge": 1, "discharge": 1}),
])
def test_infeasible_action(state, action):
    with pytest.raises(ValueError):
        advance(state, **action)
