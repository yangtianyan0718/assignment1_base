"""Student work for the forecast and forecast_evidence problems."""


def valid_origins(hours, valid, label_start, label_end):
    """Return UTC issue times in chronological order.

    hours is an increasing sequence of aware UTC datetimes; valid is a parallel
    sequence of joint-validity flags. Require consecutive, valid history and
    targets. All target times must fall in [label_start, label_end).
    """
    raise NotImplementedError("Track A: window construction and split audit")


def seasonal(history, period_hours):
    """Return 24 rows of point forecasts in MW, ordered wind, solar, demand.

    Input is 168 chronological triples. Support periods of 24 and 168 hours.
    """
    raise NotImplementedError("Track A: seasonal baseline")


def pinball(targets, quantile_predictions, quantile):
    """Return mean pinball loss across paired scalar sequences in MW."""
    raise NotImplementedError("Track A: probabilistic objective")


def train(config, data_dir, output_dir):
    """Fit baselines and model; persist training evidence in output_dir.

    config is the parsed course JSON; directories are pathlib.Path objects.
    data_dir contains the released development data. Never fit on sealed data.
    """
    raise NotImplementedError("Track A: training, checkpoint and provenance")


def evaluate(config, data_dir, output_dir):
    """Replay frozen A0/A1/A2 on development data with the common controller.

    Load fitted artifacts from output_dir. Export forecast and energy evidence.
    """
    raise NotImplementedError("Track A: validation comparison and ablation")
