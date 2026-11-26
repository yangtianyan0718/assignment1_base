def predict(history, future_calendar):
    """Return [lead hour, target, quantile] in MW for a 168-hour history.

    Target order: wind, solar, load. Quantile order: 0.1, 0.5, 0.9.
    The 24 future calendar rows contain only information known at issuance.
    """
    raise NotImplementedError("Track A: connect the trained predictor")
