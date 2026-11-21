"""Brawl Stars-inspired counterfactual Starr Drop rarity exercise.

The A probabilities are published by Supercell. B probabilities and ALL tier
values are hypothetical, invented purely for a controlled expected-value demo.
The values are teaching units, NOT in-game Coins, Gems, USD or an official payout.

No behavioral effects are estimated. Only reward-distribution properties.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "reward_design.csv"
REPORTS = ROOT / "reports"
OPENINGS = 10


@dataclass(frozen=True)
class Tier:
    name: str
    official_probability: float
    concept_probability: float
    teaching_value: int


def load_tiers(csv_path: Path = DATA_FILE) -> list[Tier]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    tiers = [Tier(
        name=r["rarity"],
        official_probability=float(r["official_odds_pct"]) / 100,
        concept_probability=float(r["jackpot_concept_odds_pct"]) / 100,
        teaching_value=int(r["illustrative_value_units"]),
    ) for r in rows]
    if len(tiers) != 5 or [x.name for x in tiers] != [
        "Rare", "Super Rare", "Epic", "Mythic", "Legendary"
    ]:
        raise ValueError("Expected five Starr Drop rarity tiers in known order")
    for col in ("official_probability", "concept_probability"):
        if abs(sum(getattr(t, col) for t in tiers) - 1) > 1e-12:
            raise ValueError(f"Probabilities in {col} do not sum to one")
        if any(not 0 <= getattr(t, col) <= 1 for t in tiers):
            raise ValueError(f"Invalid probability in {col}")
    if any(t.teaching_value <= 0 for t in tiers):
        raise ValueError("Teaching values must be positive")
    return tiers


def exact_total_distribution(tiers: list[Tier], prob_col: str, n: int = OPENINGS) -> dict[int, float]:
    """Probability distribution of sum of n independent drop value proxies."""
    if n < 1:
        raise ValueError("n must be positive")
    dist: dict[int, float] = {0: 1.0}
    for _ in range(n):
        nxt: dict[int, float] = defaultdict(float)
        for old_total, old_prob in dist.items():
            for tier in tiers:
                nxt[old_total + tier.teaching_value] += old_prob * getattr(tier, prob_col)
        dist = dict(nxt)
    return dist


def lower_median(dist: dict[int, float]) -> int:
    cum = 0.0
    for value, mass in sorted(dist.items()):
        cum += mass
        if cum >= 0.5 - 1e-12:
            return value
    raise AssertionError("Invalid distribution")


def metrics(tiers: list[Tier], col: str) -> dict:
    probs = [getattr(t, col) for t in tiers]
    values = [t.teaching_value for t in tiers]
    ev = sum(p * v for p, v in zip(probs, values))
    variance = sum(p * (v - ev)**2 for p, v in zip(probs, values))
    dist = exact_total_distribution(tiers, col)
    if abs(sum(dist.values()) - 1) > 1e-9:
        raise AssertionError("Convolution lost probability mass")
    return {
        "probabilities_pct": {t.name: round(getattr(t, col) * 100, 2) for t in tiers},
        "expected_units_per_drop": round(ev, 6),
        "expected_units_per_ten": round(ev * OPENINGS, 6),
        "sd_units_per_drop": round(variance**0.5, 4),
        "chance_legendary_in_ten_pct": round(100 * (1 - (1 - probs[-1])**OPENINGS), 4),
        "chance_first_five_all_rare_pct": round(100 * probs[0]**5, 4),
        "median_units_in_ten": lower_median(dist),
        "chance_ten_below_1080_pct": round(100 * sum(m for amount, m in dist.items() if amount < 1080), 4),
    }


def build_summary() -> dict:
    tiers = load_tiers()
    a = metrics(tiers, "official_probability")
    b = metrics(tiers, "concept_probability")
    if abs(a["expected_units_per_drop"] - b["expected_units_per_drop"]) > 1e-9:
        raise AssertionError("The thought experiment does not preserve expected value")
    return {
        "metadata": {
            "game": "Brawl Stars (independent portfolio case study)",
            "mechanic": "Regular Starr Drop rarity", "n_openings": OPENINGS,
            "source": "https://sc-brawlstars.zendesk.com/hc/en-us/articles/49526642756507-Starr-Drop-Chances",
            "source_checked": "2026-11-21",
            "warning": "A rarity odds are published by Supercell; B odds and ALL reward values are invented. No player-feeling data."
        },
        "teaching_value_by_rarity": {t.name: t.teaching_value for t in tiers},
        "A_official_rarity_mix_with_toy_values": a,
        "B_hypothetical_jackpot_mix_with_toy_values": b,
    }


def write_outputs() -> dict:
    REPORTS.mkdir(parents=True, exist_ok=True)
    result = build_summary()
    (REPORTS / "summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    tiers = load_tiers()
    with (REPORTS / "ten_drop_total_distribution.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["ten_drop_total_teaching_units", "A_probability", "B_probability"])
        a = exact_total_distribution(tiers, "official_probability")
        b = exact_total_distribution(tiers, "concept_probability")
        for total in sorted(set(a) | set(b)):
            writer.writerow([total, f"{a.get(total, 0):.12f}", f"{b.get(total, 0):.12f}"])
    return result


if __name__ == "__main__":
    data = write_outputs()
    a = data["A_official_rarity_mix_with_toy_values"]
    b = data["B_hypothetical_jackpot_mix_with_toy_values"]
    print("Same expected value: %.0f vs %.0f illustration units/drop" % (
        a["expected_units_per_drop"], b["expected_units_per_drop"]))
    print("Legendary within 10: %.1f%% vs %.1f%%" % (
        a["chance_legendary_in_ten_pct"], b["chance_legendary_in_ten_pct"]))
    print("First 5 all Rare: %.1f%% vs %.1f%%" % (
        a["chance_first_five_all_rare_pct"], b["chance_first_five_all_rare_pct"]))
    print("Median 10 drops: %.0f vs %.0f units" % (
        a["median_units_in_ten"], b["median_units_in_ten"]))
