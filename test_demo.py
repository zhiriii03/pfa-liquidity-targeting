"""Checks of the public synthetic example; not validation of the private PFA."""

from math import nan
import unittest

from demo import (Prospect, campaign_economics, percentile_ranks, quantile,
                  rank_prospects, simulate)


class CapacityAndRankingTests(unittest.TestCase):
    def test_buffer_cannot_make_demand_component_negative(self):
        p = Prospect("fictional", 100, 200, 30, 100, .5)
        self.assertEqual(p.capacity(), 130)
        self.assertEqual(p.capacity(0), 330)

    def test_longer_buffer_cannot_increase_capacity(self):
        p = Prospect("fictional", 100, 1000, 30, 100, .5)
        self.assertGreaterEqual(p.capacity(2), p.capacity(3))
        self.assertGreaterEqual(p.capacity(3), p.capacity(5))

    def test_invalid_financial_inputs_are_rejected(self):
        for savings, propensity in [(-1, .5), (nan, .5), (1, 1.1)]:
            with self.assertRaises(ValueError):
                Prospect("invalid", savings, 0, 0, 0, propensity).capacity()

    def test_ties_receive_average_percentile_rank(self):
        self.assertEqual(percentile_ranks([20, 10, 10, 30]), [.75, .375, .375, 1])
        self.assertEqual(percentile_ranks([]), [])

    def test_dominating_prospect_ranks_first(self):
        small = Prospect("small", 100, 0, 0, 0, .2)
        large = Prospect("large", 200, 0, 0, 0, .9)
        self.assertEqual(rank_prospects([small, large])[0][0], large)


class SimulationTests(unittest.TestCase):
    def test_zero_propensity_implies_zero_migration(self):
        p = Prospect("never", 1000, 0, 0, 0, 0)
        self.assertEqual(simulate([p], draws=20), [0.0] * 20)

    def test_draws_are_bounded_and_seeded(self):
        p = Prospect("certain", 1000, 0, 0, 0, 1)
        a = simulate([p], draws=100, seed=3)
        self.assertEqual(a, simulate([p], draws=100, seed=3))
        self.assertTrue(all(0 <= x <= 1000 for x in a))

    def test_quantile_interpolates_and_checks_bounds(self):
        self.assertEqual(quantile([0, 10], .5), 5)
        self.assertEqual(quantile([0, 10], 1), 10)
        with self.assertRaises(ValueError):
            quantile([], .5)


class CampaignEconomicsTests(unittest.TestCase):
    def test_positive_subscription_does_not_guarantee_positive_net_income(self):
        result = campaign_economics(100_000, 10, 50, .01, .004, .02, 0)
        self.assertEqual(result["subscription"], 1000)
        self.assertEqual(result["first_year_difference"], -1100)
        self.assertEqual(result["recurring_difference_before_future_contact_costs"], -1600)

    def test_recurring_break_even_identity(self):
        margin, fee = .025, .005
        q = 1 - fee / margin
        result = campaign_economics(100_000, 0, 0, 0, fee, margin, q)
        self.assertAlmostEqual(result["recurring_difference_before_future_contact_costs"], 0)

    def test_full_departure_removes_counterfactual_deposit_margin(self):
        result = campaign_economics(100_000, 0, 0, 0, .004, .02, 1)
        self.assertEqual(result["margin_without_campaign"], 0)
        self.assertEqual(result["recurring_difference_before_future_contact_costs"], 400)


if __name__ == "__main__":
    unittest.main()
