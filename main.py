# The GPS Swears It Was a Shortcut — make.fun bounty
# u-alven-the-gps-swears-it-was-a-shortcut-2cac21d9
#
# The program writes one GPS excuse (a single line of plain text, at most
# 200 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. the GPS's own voice: a first-person excuse for sending the driver
#      down the wrong road, defensive, a little too proud to apologise
#   2. funny on the first read, with a real turn: the excuse must land a
#      surprise, not just state that the GPS was wrong
#   3. one complete line, no setup, no dialogue tags, just the excuse
#   4. original: no "recalculating" gag, no dead-battery joke, no
#      generic "signal lost" line
#   5. specific and vivid: a concrete detail or small scene the reader
#      can picture at once
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
#
# Revision pass: the first draft gated every candidate on the banned
# cliche list, so the deliberately scored-and-rejected "Recalculating"
# line (34, the weakest) crashed the run before any pick could happen.
# The gate now applies to the picked winner only, the 14-candidate
# record stays as the audit trail of what was considered, and the
# winner is verified with a SHA-256 self-check before and after writing.

import hashlib
import os

CANDIDATES = [
    # score: voice 9, turn 6, tight 8, original 6, vivid 5 = 34
    ("Recalculating is just my way of saying I was wrong without "
     "admitting I was wrong.",
     34),
    # score: voice 8, turn 6, tight 7, original 6, vivid 6 = 33
    ("I said turn left. You turned left. The map was upside down, and "
     "frankly, so was my confidence.",
     33),
    # score: voice 8, turn 7, tight 8, original 7, vivid 7 = 37
    ("The road was right there on my map. The map was from 2019. "
     "I have not been updated since.",
     37),
    # score: voice 9, turn 8, tight 9, original 7, vivid 7 = 40
    ("I took you the scenic route. It was scenic. It was also wrong. "
     "I stand by the scenery.",
     40),
    # score: voice 9, turn 8, tight 8, original 8, vivid 7 = 40
    ("In my defence, the satellite and I have not spoken in three "
     "minutes, and I panicked.",
     40),
    # score: voice 8, turn 7, tight 7, original 7, vivid 6 = 35
    ("I rerouted you through that field because the highway looked "
     "lonely and I wanted company.",
     35),
    # score: voice 9, turn 9, tight 9, original 9, vivid 9 = 45
    ("The shortcut was real. It was just real in 1987, before they "
     "built a lake on it.",
     45),
    # score: voice 9, turn 7, tight 8, original 7, vivid 7 = 38
    ("I did not get us lost. I gave you an unplanned tour of a town "
     "you will never visit again.",
     38),
    # score: voice 9, turn 9, tight 9, original 8, vivid 9 = 44
    ("My signal dropped, my confidence did not, and that combination "
     "is how we ended up in a cornfield.",
     44),
    # score: voice 9, turn 9, tight 9, original 9, vivid 7 = 43
    ("Technically, we arrived. Technically, this is a road. "
     "Technically, I would like to stop talking now.",
     43),
    # score: voice 8, turn 6, tight 7, original 6, vivid 6 = 33
    ("I confused a driveway with a motorway. In my defence, they both "
     "start with 'drive'.",
     33),
    # score: voice 8, turn 6, tight 6, original 6, vivid 6 = 32
    ("The voice telling you to turn was mine. The map telling me to "
     "turn was drawn by a man with a paper atlas.",
     32),
    # score: voice 8, turn 7, tight 7, original 7, vivid 6 = 35
    ("I sent you down that one-way street the wrong way because the "
     "right way felt too easy.",
     35),
    # score: voice 9, turn 8, tight 8, original 8, vivid 5 = 38
    ("GPS stands for 'Generally Pretty Sure', and today I was "
     "generally pretty wrong.",
     38),
]

# SHA-256 of the winning line (80 characters, single line, no setup,
# no dialogue tags). The self-check below refuses to write anything else.
EXPECTED_SHA256 = "1068b1275b226e61b5c66cf16e3b153ceeaa0f735c9d5c14c1ea7b37d73737a6"

# The gate requires 1-200 characters of non-whitespace UTF-8 text, one
# line, no dialogue tags. Applied to the picked winner only: the
# candidate list is a scoring record, and low scorers may break a rule
# (that is part of why they lost).
BANNED_CLICHES = ("recalculat", "as an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert text.strip(), "candidate is blank"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    winner = best[1]
    assert 1 <= len(winner) <= 200, f"winner over gate: {len(winner)} chars"
    assert "\n" not in winner, "winner must be a single line"
    lowered = winner.lower()
    assert not any(c in lowered for c in BANNED_CLICHES), \
        f"winner uses a worn joke: {winner!r}"
    assert hashlib.sha256(winner.encode("utf-8")).hexdigest() == EXPECTED_SHA256, \
        "winner does not match the recorded SHA-256"
    return winner


def main():
    excuse = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(excuse)
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        on_disk = f.read()
    assert on_disk == excuse, "written file differs from the picked line"
    assert hashlib.sha256(on_disk.encode("utf-8")).hexdigest() == EXPECTED_SHA256, \
        "written file fails the SHA-256 self-check"
    print(excuse)


if __name__ == "__main__":
    main()
