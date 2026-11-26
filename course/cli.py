"""Preview the hand-calculation fixture without network access."""
import argparse
import json
from pathlib import Path
from .evidence import inventory
from dataclasses import asdict
from .physics import State, advance


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Print the synthetic noon ledger")
    demo.add_argument("--provider", choices=["mock"], default="mock")
    for name in ("train", "evaluate"):
        command = commands.add_parser(name, help=f"Run the student {name} implementation")
        command.add_argument("--track", required=True, choices=["A"] if name == "train" else ["A", "B"])
        command.add_argument("--data-dir", required=True, type=Path)
        command.add_argument("--run-dir", required=True, type=Path)
    review = commands.add_parser("evidence", help="Inventory rubric artifacts; exit 1 for missing files")
    review.add_argument("--track", required=True, choices=["A", "B"])
    review.add_argument("--run-dir", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "evidence":
        return 0 if inventory(args.track, args.run_dir) else 1
    if args.command in ("train", "evaluate"):
        if not args.data_dir.is_dir():
            parser.error(f"Missing development data directory: {args.data_dir}")
        from starter.forecast import training
        from starter.harness import replay
        config = json.loads((Path(__file__).resolve().parents[1] / "configs/course.json").read_text())
        entry = {("train", "A"): training.train, ("evaluate", "A"): training.evaluate,
                 ("evaluate", "B"): replay.evaluate}[args.command, args.track]
        try:
            entry(config, args.data_dir, args.run_dir)
        except NotImplementedError as exc:
            parser.exit(2, f"Student implementation pending: {exc}\n")
        return 0
    if args.command == "demo":
        start = State()
        end = advance(start, pump=10, charge=5)
        print(json.dumps(dict(source="synthetic noon fixture", wind_mw=35, solar_mw=20,
                              load_mw=40, pump_mw=10, charge_mw=5,
                              start=asdict(start), end=asdict(end)), indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
