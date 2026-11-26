"""Print a track's rubric and inventory the expected evidence in a run folder."""
from pathlib import Path

COMMON = ("reproduce", 15, ("reproduction.md", "versions.json", "report.pdf"))
TRACKS = {
    "A": (
        ("forecast", 35, ("training.csv", "forecast_packet.json", "checkpoint.sha256")),
        ("forecast_energy", 25, ("data_card.md", "hourly.csv", "windows.md")),
        ("forecast_evidence", 25, ("forecast_value.csv", "split_audit.csv", "ablation.md", "failure.md")),
        COMMON,
    ),
    "B": (
        ("supervisor", 35, ("tools.jsonl", "gateway.json", "recovery.md")),
        ("control_energy", 25, ("hourly.csv", "decisions.md")),
        ("control_evidence", 25, ("management_value.csv", "repeats.csv", "ablation.md", "failure.md")),
        COMMON,
    ),
}


def inventory(track: str, directory: Path) -> bool:
    complete = True
    for key, points, filenames in TRACKS[track]:
        print(f"{key} ({points} points)")
        for name in filenames:
            path = directory / name
            present = path.is_file() and path.stat().st_size > 0
            print(f"  {'present' if present else 'missing or empty'}  {name}")
            complete = complete and present
    return complete
