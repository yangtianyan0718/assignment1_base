import pytest
from .adapters import choose_deterministic

pytestmark = pytest.mark.assignment


class CandidateTools:
    """One synthetic strategy decision with three already-feasible candidates."""

    def __init__(self, outcomes):
        self.outcomes = outcomes
        self.calls = []

    def observe(self):
        return {"state_version": 7, "forecast_id": "public-7",
                "time_utc": "2023-06-21T06:00:00Z", "episode_id": "fixture",
                "battery_mwh": 10., "upper_water_m3": 110000.,
                "available_limits": {"grid_import_max_mw": 35.}}

    def plan_dispatch(self, policy_id):
        assert len(self.calls) < 3
        self.calls.append(policy_id)
        return "plan-" + policy_id

    def simulate(self, plan_id):
        policy = plan_id.removeprefix("plan-")
        assert policy in self.calls
        eens, deficit, cost = self.outcomes[policy]
        return dict(eens_mwh=eens, terminal_deficit_mwh=deficit, cost_with_curtailment_cu=cost)

    def validate(self, plan_id):
        assert plan_id.removeprefix("plan-") in self.calls
        return {"ok": True, "errors": []}

    def commit(self, plan_id, expected_version, key):
        pytest.fail("A candidate comparison must not settle the plant")


@pytest.mark.parametrize("expected", ["flexible", "balanced", "reserve"])
def test_b0_compares_within_one_budget(expected):
    outcomes = dict.fromkeys(("flexible", "balanced", "reserve"), (1., 0., 10.))
    outcomes[expected] = (0., 0., 50.)
    tools = CandidateTools(outcomes)
    assert choose_deterministic(tools.observe(), tools) == expected
    assert set(tools.calls) == set(outcomes)
