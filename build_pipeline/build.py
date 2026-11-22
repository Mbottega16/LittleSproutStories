"""
The one command the README asks for: rebuild books/*.html from
build_pipeline/specs/*.json.

    python build_pipeline/build.py            # rebuild every book from its spec
    python build_pipeline/build.py Book1_Maya_Marcus_FireStation   # rebuild one

Round trip: re-rendering the 18 specs produces books/ byte for byte
(re-verified 2026-11-22; `python scripts/pipeline_roundtrip.py` checks it and
CI runs it). If that check fails because a book was edited by hand, run
`python build_pipeline/extract_spec.py --all` first, to copy the edit back
into the specs. Otherwise this command overwrites the hand edit.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import main as render_main  # noqa: E402


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--all":
        sys.argv = [sys.argv[0], "--all"]
    else:
        name = sys.argv[1]
        spec_path = Path(__file__).resolve().parent / "specs" / f"{name}.json"
        if not spec_path.exists():
            print(f"No spec found at {spec_path}")
            raise SystemExit(1)
        sys.argv[1] = str(spec_path)
    raise SystemExit(render_main())
