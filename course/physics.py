"""One-hour teaching ledger. Inputs are bus-side average MW for one hour."""
from dataclasses import dataclass
from math import isfinite
import json
from pathlib import Path

SYSTEM = json.loads((Path(__file__).resolve().parents[1] / "configs/course.json").read_text())["system"]


@dataclass(frozen=True)
class State:
    battery_mwh: float = SYSTEM["battery"]["initial_energy_mwh"]
    upper_water_m3: float = SYSTEM["hydro"]["upper_initial_water_m3"]


def advance(state, *, charge=0., discharge=0., pump=0., generate=0.):
    """Return end state for a feasible storage action. Reject invalid inputs."""
    b, h = SYSTEM["battery"], SYSTEM["hydro"]
    for value, limit in ((charge, b["charge_max_mw"]), (discharge, b["discharge_max_mw"]),
                         (pump, h["pump_max_mw"]), (generate, h["generate_max_mw"])):
        if not isfinite(value) or not 0 <= value <= limit:
            raise ValueError("Storage power outside operating range")
    if (charge and discharge) or (pump and generate):
        raise ValueError("Conflicting storage modes")
    joules_per_m3 = h["rho_kg_m3"] * h["g_m_s2"] * h["head_m"]
    net_hydro = pump * h["pump_efficiency"] - generate / h["generate_efficiency"]
    end = State(state.battery_mwh + charge * b["charge_efficiency"] - discharge / b["discharge_efficiency"],
                state.upper_water_m3 + net_hydro * 3.6e9 / joules_per_m3)
    for snapshot in (state, end):
        if not b["energy_min_mwh"] <= snapshot.battery_mwh <= b["energy_max_mwh"]:
            raise ValueError("Battery energy outside operating range")
        if not 0 <= snapshot.upper_water_m3 <= h["upper_active_capacity_m3"]:
            raise ValueError("Upper reservoir outside operating range")
    return end
