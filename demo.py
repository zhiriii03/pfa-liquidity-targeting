"""Synthetic portfolio demo, newly written for the public PFA case study.

No bank data or fitted classifier is used. Scores, clients, balances and scenario
parameters are artificial. Outputs are NOT original internship results.
Python 3.10+, standard library only. No files are written and no network is used.
"""

from dataclasses import dataclass
from math import isfinite
from random import Random
from statistics import mean


def nonnegative(*values: float) -> None:
    if any(not isfinite(x) or x < 0 for x in values):
        raise ValueError("Amounts and rates must be finite and nonnegative.")


@dataclass(frozen=True)
class Prospect:
    label: str
    savings: float
    demand: float
    other: float
    monthly_expense: float
    propensity: float

    def capacity(self, buffer_months: float = 3) -> float:
        nonnegative(self.savings, self.demand, self.other,
                    self.monthly_expense, buffer_months)
        if not isfinite(self.propensity) or not 0 <= self.propensity <= 1:
            raise ValueError("Propensity must be between zero and one.")
        return (self.savings + self.other
                + max(0.0, self.demand - buffer_months * self.monthly_expense))


def percentile_ranks(values: list[float]) -> list[float]:
    """Average one-based rank / n; ties receive the same percentile."""
    if not values:
        return []
    if any(not isfinite(x) for x in values):
        raise ValueError("Ranking values must be finite.")
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        percentile = ((start + 1 + end) / 2) / len(values)
        for position in range(start, end):
            ranks[order[position]] = percentile
        start = end
    return ranks


def rank_prospects(prospects: list[Prospect]) -> list[tuple[Prospect, float]]:
    capacity_ranks = percentile_ranks([p.capacity() for p in prospects])
    propensity_ranks = percentile_ranks([p.propensity for p in prospects])
    scored = [(p, a * b) for p, a, b in
              zip(prospects, capacity_ranks, propensity_ranks)]
    return sorted(scored, key=lambda item: (-item[1], item[0].label))


def simulate(prospects: list[Prospect], draws: int = 3000,
             seed: int = 42) -> list[float]:
    if draws <= 0:
        raise ValueError("At least one simulation draw is required.")
    capacities = [p.capacity() for p in prospects]
    rng = Random(seed)
    totals = []
    for _ in range(draws):
        total = 0.0
        for p, capacity in zip(prospects, capacities):
            if rng.random() < p.propensity:
                total += capacity * rng.betavariate(2, 3)
        totals.append(total)
    return totals


def quantile(values: list[float], fraction: float) -> float:
    if not values or not 0 <= fraction <= 1:
        raise ValueError("A nonempty sample and quantile in [0, 1] are required.")
    ordered = sorted(values)
    location = (len(ordered) - 1) * fraction
    low = int(location)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (location - low)


def campaign_economics(amount: float, contacts: int, contact_cost: float,
                       subscription_rate: float, annual_fee_rate: float,
                       deposit_margin: float, departure_probability: float) -> dict[str, float]:
    nonnegative(amount, contacts, contact_cost, subscription_rate,
                annual_fee_rate, deposit_margin)
    if not isfinite(departure_probability) or not 0 <= departure_probability <= 1:
        raise ValueError("Departure probability must be between zero and one.")
    subscription = amount * subscription_rate
    annual_fee = amount * annual_fee_rate
    forgone_margin = amount * (1 - departure_probability) * deposit_margin
    costs = contacts * contact_cost
    return {
        "subscription": subscription,
        "annual_fee": annual_fee,
        "margin_without_campaign": forgone_margin,
        "contact_cost": costs,
        "first_year_difference": subscription + annual_fee - forgone_margin - costs,
        "recurring_difference_before_future_contact_costs": annual_fee - forgone_margin,
    }


def synthetic_prospects(n: int = 200, seed: int = 7) -> list[Prospect]:
    rng = Random(seed)
    return [Prospect(
        label=f"DEMO-{i + 1:04d}",
        savings=rng.uniform(0, 100_000),
        demand=rng.uniform(0, 60_000),
        other=rng.uniform(0, 5_000),
        monthly_expense=rng.uniform(2_000, 12_000),
        propensity=rng.uniform(0.05, 0.95),
    ) for i in range(n)]


def main() -> None:
    prospects = synthetic_prospects()
    ranked = rank_prospects(prospects)
    selected = [p for p, _ in ranked[:40]]
    print("SYNTHETIC EDUCATIONAL DEMO -- not original PFA results")
    print("Input propensities are generated, not fitted classifier predictions.\n")
    print("Top five synthetic prospects:")
    for p, score in ranked[:5]:
        print(f"{p.label}: capacity={p.capacity():,.0f}; "
              f"input p={p.propensity:.3f}; percentile-product={score:.3f}")
    totals = simulate(selected)
    expected = 0.4 * sum(p.capacity() * p.propensity for p in selected)
    print(f"\nSelected fictional clients: {len(selected)}")
    print(f"Conditional analytical expectation: {expected:,.0f}")
    print(f"Simulated mean: {mean(totals):,.0f}")
    print(f"Central 90% scenario interval: {quantile(totals, .05):,.0f} "
          f"to {quantile(totals, .95):,.0f}")
    print("\nIllustrative financial scenario, using the analytical expectation:")
    print("Rates: subscription 1%; annual distributor fee 0.4%; deposit margin 2%.")
    print("Contact cost: 100 monetary units; assumed departure probability: 50%.")
    result = campaign_economics(expected, len(selected), 100, .01, .004, .02, .5)
    for label, value in result.items():
        print(f"{label}: {value:,.2f}")


if __name__ == "__main__":
    main()
