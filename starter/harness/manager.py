def choose_policy(snapshot, tools):
    """Select flexible, balanced or reserve for this immutable snapshot.

    The evaluator owns execution. Candidate planning, simulation and validation
    share the snapshot version and forecast ID. Return the selected policy ID.
    """
    raise NotImplementedError("Track B: implement the bounded supervisor")


def choose_deterministic(snapshot, tools):
    """Return the B0 policy ID after comparing the three public candidates.

    Candidate outcomes carry eens_mwh, terminal_deficit_mwh and
    cost_with_curtailment_cu. All candidates share one snapshot. A policy
    decision does not commit a plan or advance plant time.
    """
    raise NotImplementedError("Track B: deterministic comparison")
