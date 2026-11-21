import math
import unittest
from src.reward_model import load_tiers, metrics, exact_total_distribution, build_summary


class RewardEconomyTests(unittest.TestCase):
    def setUp(self):
        self.tiers = load_tiers()

    def test_official_source_rates(self):
        self.assertEqual([round(t.official_probability * 100) for t in self.tiers], [50, 28, 15, 5, 2])

    def test_both_probability_distributions_sum_to_one(self):
        for col in ("official_probability", "concept_probability"):
            self.assertAlmostEqual(sum(getattr(t, col) for t in self.tiers), 1)

    def test_same_ev_is_exact(self):
        summary = build_summary()
        a = summary["A_official_rarity_mix_with_toy_values"]
        b = summary["B_hypothetical_jackpot_mix_with_toy_values"]
        self.assertEqual(a["expected_units_per_drop"], 108)
        self.assertEqual(b["expected_units_per_drop"], 108)

    def test_legendary_and_rare_streak(self):
        a = metrics(self.tiers, "official_probability")
        b = metrics(self.tiers, "concept_probability")
        self.assertAlmostEqual(a["chance_legendary_in_ten_pct"], 18.2927, places=3)
        self.assertAlmostEqual(b["chance_legendary_in_ten_pct"], 33.5167, places=3)
        self.assertAlmostEqual(a["chance_first_five_all_rare_pct"], 3.125, places=4)
        self.assertAlmostEqual(b["chance_first_five_all_rare_pct"], 23.7305, places=3)

    def test_ten_drop_distribution_reconciles(self):
        for col in ("official_probability", "concept_probability"):
            d = exact_total_distribution(self.tiers, col)
            self.assertAlmostEqual(sum(d.values()), 1, places=8)
            self.assertAlmostEqual(sum(k * v for k, v in d.items()), 1080, places=8)
            self.assertTrue(all(k % 50 == 0 for k in d))

    def test_median_tradeoff(self):
        self.assertEqual(metrics(self.tiers, "official_probability")["median_units_in_ten"], 950)
        self.assertEqual(metrics(self.tiers, "concept_probability")["median_units_in_ten"], 800)


if __name__ == "__main__":
    unittest.main()
