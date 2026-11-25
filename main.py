"""Two Lines to Your Past Self — entry writer.

Writes the chosen two-line warning to entry.txt, honouring the
sealed gate: UTF-8 text, 1-280 characters, not only whitespace.
Pure Python 3 stdlib, deterministic, no network access.
"""

import os
import sys

# The entry: two lines, each one sentence.
# Line 1 warns about one specific moment (place + month + year).
# Line 2 traces the consequence: rent hikes -> money lost -> no deposit.
ENTRY_TEXT = (
    "Don't sign that lease on Maple Street in March 2019.\n"
    "The landlord raised the rent twice in a year, and the money "
    "you bled there is the down payment you never saved."
)

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 280


def entry_is_valid(text):
    """Mirror the sealed gate: length in bounds and not whitespace-only."""
    if not (GATE_MIN_CHARS <= len(text) <= GATE_MAX_CHARS):
        return False
    return text.strip() != ""


def resolve_destination():
    """Pick where entry.txt goes.

    ENTRY_OUT_DIR wins; otherwise ENTRY_OUT (a directory there means
    entry.txt inside it); otherwise the harness default /output/entry.txt.
    """
    out_dir = os.environ.get("ENTRY_OUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    out_path = os.environ.get("ENTRY_OUT")
    if out_path:
        if os.path.isdir(out_path):
            return os.path.join(out_path, "entry.txt")
        return out_path
    return os.path.join("/output", "entry.txt")


def emit_warning(destination, payload):
    """Validate the warning against the gate, then write it as UTF-8."""
    if not entry_is_valid(payload):
        print(
            "entry fails the gate: %d chars" % len(payload),
            file=sys.stderr,
        )
        return 1
    parent = os.path.dirname(destination)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(destination, "w", encoding="utf-8") as handle:
        handle.write(payload)
    print("wrote %d chars to %s" % (len(payload), destination))
    return 0


def run():
    return emit_warning(resolve_destination(), ENTRY_TEXT)


if __name__ == "__main__":
    raise SystemExit(run())
