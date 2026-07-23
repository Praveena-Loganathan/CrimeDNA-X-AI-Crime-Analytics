"""
CrimeDNA-X — Behavioral Crime Linkage (Python CLI version)
Linking crime by behavior, not by identity.

This tool does NOT identify suspects, predict guilt, or recommend arrests.
Human investigators make all final decisions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


# ---------------- data ----------------

FEATURE_KEYS = [
    "crimeType", "timeWindow", "entryMethod", "weaponTool", "targetType",
    "victimProfile", "escapeMethod", "locationChar", "mo",
]

FEATURE_LABELS = {
    "crimeType": "Crime Type",
    "timeWindow": "Time Window",
    "entryMethod": "Entry Method",
    "weaponTool": "Weapon / Tool",
    "targetType": "Target Type",
    "victimProfile": "Victim Profile",
    "escapeMethod": "Escape Method",
    "locationChar": "Location Characteristics",
    "mo": "Modus Operandi",
}

weights: Dict[str, float] = {
    "crimeType": 0.15, "timeWindow": 0.10, "entryMethod": 0.15, "weaponTool": 0.10,
    "targetType": 0.10, "victimProfile": 0.05, "escapeMethod": 0.10,
    "locationChar": 0.10, "mo": 0.15,
}

past_cases = [
    {"id": "A-2291", "title": "Burglary — Maple Court Apartments",
     "crimeType": "Residential burglary", "timeWindow": "01:00–04:00",
     "entryMethod": "Forced entry, rear window", "weaponTool": "Crowbar",
     "targetType": "Residential apartment", "victimProfile": "Elderly resident, absent",
     "escapeMethod": "On foot via rear alley", "locationChar": "Gated colony",
     "mo": "CCTV disabled before entry"},
    {"id": "A-2278", "title": "Burglary — Lakeview Villas",
     "crimeType": "Residential burglary", "timeWindow": "01:00–04:00",
     "entryMethod": "Forced entry, rear window", "weaponTool": "Crowbar",
     "targetType": "Residential villa", "victimProfile": "Family sleeping inside",
     "escapeMethod": "On foot via rear alley", "locationChar": "Gated colony",
     "mo": "CCTV disabled before entry"},
    {"id": "A-2154", "title": "Burglary — Sundar Nagar House",
     "crimeType": "Residential burglary", "timeWindow": "23:00–02:00",
     "entryMethod": "Forced entry, rear window", "weaponTool": "Screwdriver",
     "targetType": "Residential house", "victimProfile": "Family away, travelling",
     "escapeMethod": "Two-wheeler", "locationChar": "Gated colony",
     "mo": "CCTV disabled before entry"},
    {"id": "A-1987", "title": "Theft — Market Road Shop",
     "crimeType": "Commercial theft", "timeWindow": "02:00–04:00",
     "entryMethod": "Shutter lock broken", "weaponTool": "Crowbar",
     "targetType": "Retail shop", "victimProfile": "Premises unoccupied",
     "escapeMethod": "On foot", "locationChar": "Market street",
     "mo": "Targets cash counter only"},
    {"id": "A-2033", "title": "Vehicle Theft — Ashok Nagar Street",
     "crimeType": "Vehicle theft", "timeWindow": "00:00–03:00",
     "entryMethod": "Ignition hotwired", "weaponTool": "None",
     "targetType": "Parked motorcycle", "victimProfile": "Not present",
     "escapeMethod": "Rides vehicle away", "locationChar": "Residential street",
     "mo": "Targets unlocked / older bikes"},
]

incoming_firs = [
    {"key": "fir1", "id": "2026-0731", "title": "Break-in — Rose Garden Bungalow, ward 9",
     "crimeType": "Residential burglary", "timeWindow": "01:00–04:00",
     "entryMethod": "Forced entry, rear window", "weaponTool": "Crowbar",
     "targetType": "Residential bungalow", "victimProfile": "Family away for the weekend",
     "escapeMethod": "On foot via rear alley", "locationChar": "Gated colony",
     "mo": "CCTV disabled before entry"},
    {"key": "fir2", "id": "2026-0714", "title": "Bike theft — Ashok Nagar main road",
     "crimeType": "Vehicle theft", "timeWindow": "23:30–02:30",
     "entryMethod": "Ignition hotwired", "weaponTool": "None",
     "targetType": "Parked motorcycle", "victimProfile": "Not present",
     "escapeMethod": "Rides vehicle away", "locationChar": "Residential street",
     "mo": "Targets unlocked / older bikes"},
]

gap_library = {
    "Residential burglary": [
        "CCTV footage from adjoining streets pending",
        "Fingerprint comparison against entry point not yet run",
        "Vehicle verification for the colony gate log pending",
        "Mobile tower dump for the time window not requested",
        "Neighbor canvass incomplete",
    ],
    "Commercial theft": [
        "Shutter-lock tool mark analysis pending",
        "CCTV footage from adjacent shops not collected",
        "Cash-handling staff statements incomplete",
        "Point-of-sale log cross-check pending",
    ],
    "Vehicle theft": [
        "Chassis/engine number circulation pending",
        "Nearby ANPR camera footage not pulled",
        "Registered-owner statement not recorded",
        "Similar-MO bike theft cluster not cross-checked",
    ],
}

feedback_state: Dict[str, str] = {}  # match case id -> 'confirmed' | 'rejected'


# ---------------- helpers ----------------

def normalize_weights():
    total = sum(weights[k] for k in FEATURE_KEYS)
    for k in FEATURE_KEYS:
        weights[k] = weights[k] / total


def score_case(fir: dict, past_case: dict):
    score = 0.0
    matched = []
    for k in FEATURE_KEYS:
        if fir[k] == past_case[k]:
            score += weights[k]
            matched.append(k)
    return {"score": round(score * 100), "matched": matched}


def confidence_of(score: int):
    if score >= 85:
        return {"label": "High", "symbol": "●●●"}
    if score >= 65:
        return {"label": "Medium", "symbol": "●●○"}
    return {"label": "Low", "symbol": "●○○"}


def compute_matches(fir: dict):
    scored = []
    for pc in past_cases:
        result = score_case(fir, pc)
        scored.append({"pc": pc, **result})
    scored.sort(key=lambda m: m["score"], reverse=True)
    return scored[:3]


# ---------------- rendering (console) ----------------

def render_stamp():
    now = datetime.now().strftime("%b %d, %Y").upper()
    print(f"ANALYSIS SESSION · {now}")
    print("CrimeDNA·X — Linking crime by behavior, not by identity")
    print("=" * 70)


def render_fir_select():
    print("\nIncoming FIRs:")
    for i, f in enumerate(incoming_firs, 1):
        print(f"  [{i}] FIR #{f['id']} — {f['title']}")


def render_ladder(fir: dict):
    print("\n--- Behavioral Crime DNA Profile ---")
    for k in FEATURE_KEYS:
        print(f"  {FEATURE_LABELS[k]:<26}: {fir[k]}")


def render_fir_node(fir: dict):
    print(f"\n[FIR #{fir['id']}] {fir['title']}")


def render_matches(matches: List[dict]):
    print("\n--- ABCS Similarity Engine — Case Board ---")
    for m in matches:
        conf = confidence_of(m["score"])
        state = feedback_state.get(m["pc"]["id"])
        tag = f" ({state})" if state else ""
        print(f"\n  CASE #{m['pc']['id']} — {m['pc']['title']}{tag}")
        print(f"    Match: {m['score']}%  |  Confidence: {conf['label']} {conf['symbol']}")
        matched_labels = [FEATURE_LABELS[k].lower() for k in m["matched"][:3]]
        why = ", ".join(matched_labels) if matched_labels else "none strongly"
        print(f"    Why similar: shares {len(m['matched'])} of {len(FEATURE_KEYS)} "
              f"behavioral features, most notably {why}.")
        traits = []
        for k in FEATURE_KEYS:
            mark = "✓" if k in m["matched"] else " "
            traits.append(f"[{mark}]{FEATURE_LABELS[k]}")
        print("    " + "  ".join(traits))


def render_gaps(fir: dict):
    print("\n--- Investigation Gap Assistant ---")
    gaps = gap_library.get(fir["crimeType"], [])
    if not gaps:
        print("  No known gap template for this crime type.")
        return
    for g in gaps:
        print(f"  ⚠ {g}")


def render_report(fir: dict, matches: List[dict]):
    print("\n--- Explainable Investigation Report ---")
    top = matches[0]
    conf = confidence_of(top["score"])
    print(f"  Top Match Similarity : {top['score']}%")
    print(f"  Confidence Level     : {conf['label']}")
    gap_count = len(gap_library.get(fir["crimeType"], []))
    steps = [
        f"Cross-reference case #{top['pc']['id']} ({top['pc']['title']}) as the "
        f"highest-similarity precedent.",
        f"Review remaining {gap_count} outstanding investigation steps listed in "
        f"the Gap Assistant.",
        f"Compare investigating-officer notes across the top {len(matches)} matches "
        f"for a shared suspect pattern, without treating similarity as identification.",
        "Route confirmed/rejected feedback into ABCS so future comparisons reflect "
        "this investigator's judgment.",
    ]
    for i, s in enumerate(steps, 1):
        print(f"  {i}. {s}")
    print("\n  Note: Feature weights adapt as investigators confirm or reject matches —")
    print("  this only reorders future comparisons, it never assigns guilt.")


def render_all(fir: dict):
    matches = compute_matches(fir)
    render_fir_node(fir)
    render_ladder(fir)
    render_matches(matches)
    render_gaps(fir)
    render_report(fir, matches)
    return matches


def apply_feedback(matches: List[dict], case_id: str, action: str):
    """action: 'confirm' or 'reject'"""
    match = next((m for m in matches if m["pc"]["id"] == case_id), None)
    if not match:
        print("  No such case in current match list.")
        return
    delta = 0.02 if action == "confirm" else -0.02
    for k in match["matched"]:
        weights[k] = max(0.01, weights[k] + delta)
    normalize_weights()
    feedback_state[case_id] = "confirmed" if action == "confirm" else "rejected"


# ---------------- interactive loop ----------------

def main():
    render_stamp()
    render_fir_select()

    while True:
        choice = input(f"\nSelect FIR [1-{len(incoming_firs)}] (or 'q' to quit): ").strip()
        if choice.lower() == "q":
            break
        try:
            idx = int(choice) - 1
            fir = incoming_firs[idx]
        except (ValueError, IndexError):
            print("  Invalid selection.")
            continue

        feedback_state.clear()
        matches = render_all(fir)

        while True:
            fb = input(
                "\nGive feedback? (format: <case_id> confirm|reject, or 'n' for none, "
                "'m' to pick another FIR): "
            ).strip()
            if fb.lower() == "n":
                break
            if fb.lower() == "m":
                break
            parts = fb.split()
            if len(parts) != 2 or parts[1] not in ("confirm", "reject"):
                print("  Format: <case_id> confirm|reject   e.g.  A-2291 confirm")
                continue
            case_id, action = parts
            apply_feedback(matches, case_id, action)
            matches = compute_matches(fir)
            render_matches(matches)
            render_report(fir, matches)

    print("\nSession ended. CrimeDNA-X does not identify suspects, predict guilt, "
          "or recommend arrests — human investigators make all final decisions.")


if __name__ == "__main__":
    main()
