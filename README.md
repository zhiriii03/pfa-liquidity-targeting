# Idle Liquidity & Investment Targeting

**PFA · Banking analytics · Python · Customer targeting · Financial decision support**

**Author:** [Hamza Zhiri](https://github.com/zhiriii03) · INSEA

[Lire en français](README.fr.md) · [Methodology](METHODOLOGY.md) · [Publication scope](PUBLICATION_SCOPE.md)

## The business question

Which customers combine potentially investable liquidity with a profile suggesting
interest in investment products? And under which assumptions would moving deposits
into investments create value for the distributing bank?

My end-of-year project connects data quality, customer segmentation, propensity
modelling, campaign prioritization and financial scenario analysis. Its purpose is
to support a decision, rather than optimize a classification metric in isolation.

## What I worked on

| Stage | Contribution |
|---|---|
| Data quality | Client-level deduplication, missingness diagnostics, logical consistency checks and deposit-component overlap checks. |
| Segmentation | Separate primary-bank relationships, presumed transit accounts and inactive accounts, while keeping the limits of that interpretation explicit. |
| Modelling | Compare logistic regression, random forests and histogram gradient boosting using stratified five-fold validation. |
| Targeting | Combine within-segment capacity and propensity percentile ranks. |
| Simulation | Translate capacity and propensity into conditional migration scenarios. |
| Financial analysis | Distinguish subscription-commission ROI from the loss of deposit margin and the risk of funds leaving without a campaign. |
| Communication | Document assumptions, limits and an operational reporting structure using a client-level fact table and DAX measures. |

The original study uses observed investor status for classification and interprets
the score as commercial propensity. This transfer is an assumption: validation of
conversion after contact requires a subsequent campaign, ideally with a control group.

## Public release

This is an **anonymized portfolio edition**, not the internal internship deliverable.
It contains a methodological case study and a standalone educational Python demo.
No bank dataset, client records, internal financial results, fitted model or full
internship report is included.

**The demo is a new, simplified reconstruction for publication.** Every client,
balance, score and financial parameter in it is synthetic. Its scores are generated
inputs, not predictions from a trained classifier. Its outputs are not results
from the original PFA.

## Run the demonstration

Requires **Python 3.10+** and only the standard library.

```bash
python demo.py
python -m unittest -v
```

The demo prints a synthetic prospect ranking, conditional Monte Carlo quantiles
and a simplified financial comparison. It creates no files and makes no network calls.
See [demo.py](demo.py) and the [financial and ranking checks](test_demo.py).

## What to look for

- Capacity and propensity answer different questions: **how much** and **how likely**.
- A high observed-status AUC does not validate a future campaign conversion rate.
- A simulation interval is conditional on its probability, capacity and dependence assumptions.
- Fees can cover contact costs while migration still reduces the bank's overall income.
- A low account balance does not establish a customer's total wealth or another-bank balance.

## Technology

The original analysis is documented using Python, pandas, NumPy and scikit-learn,
with DAX for operational measures and LaTeX for the report. The public demo uses
only Python's standard library; it does not reproduce the original training pipeline.

## Repository guide

| File | Contents |
|---|---|
| [METHODOLOGY.md](METHODOLOGY.md) | Analytical workflow, validation protocol and financial equations. |
| [demo.py](demo.py) | Synthetic capacity, ranking, simulation and campaign-economics example. |
| [test_demo.py](test_demo.py) | Boundary cases, tied ranks, simulation and financial identities. |
| [PUBLICATION_SCOPE.md](PUBLICATION_SCOPE.md) | What this edition publishes and what it does not substantiate. |

This repository presents personal academic work and does not represent a bank's
endorsement or a production investment recommendation.
