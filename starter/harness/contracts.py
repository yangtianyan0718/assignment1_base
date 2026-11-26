"""Tool boundary for the student supervisor. The evaluator owns the plant."""
from typing import Protocol


class DispatchTools(Protocol):
    def observe(self) -> dict:
        """Return the current public snapshot and forecast identifiers."""
        ...

    def plan_dispatch(self, policy_id: str) -> str:
        """Return a candidate plan ID bound to this snapshot."""
        ...

    def simulate(self, plan_id: str) -> dict:
        """Return forecast-based candidate outcomes without advancing time."""
        ...

    def validate(self, plan_id: str) -> dict:
        """Return ok (bool) and errors (list of strings) after independent checks."""
        ...

    def commit(self, plan_id: str, expected_version: int, key: str) -> dict:
        """Settle the first hour exactly once for a matching idempotency key."""
        ...
