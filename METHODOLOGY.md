# Analytical methodology

This document summarizes the PFA's reasoning. Published numerical examples belong
to the synthetic demo and do not disclose the original bank extraction or results.

## 1. Observation unit and data quality

Consolidate the extraction at client level before splitting it into learning and
validation populations. Repeated identifiers must not appear on both sides of a
split. Examine missing values, implausible demographics, conflicting investor
statuses and overlap between deposit components before calculating totals.

Distinguish an absent operation from an absent extraction. A large difference in
investor rates between missing and observed groups is a warning about data coverage
or leakage, not a complete explanation of its cause. Avoid reconstructing highly
incomplete variables without checking their predictive accuracy.

## 2. Behavioural segmentation

The original study distinguishes primary-bank accounts, presumed transit accounts
and inactive accounts. Flow-to-balance relationships help formulate these segments.
They do not prove external wealth or directly estimate the probability that funds
will leave the bank. Annualized flows are not a lower bound on external wealth:
the same money may circulate repeatedly.

The public demo represents only one synthetic prospect population. It does not
claim to reproduce the original segment assignment rules or population sizes.

## 3. Propensity classification and validation

The supervised target is observed investor status. Models discussed in the study are:

- Logistic regression, as an interpretable baseline.
- Random forest, for nonlinear effects and interactions.
- Histogram gradient boosting, for successive loss reduction.

The documented protocol uses stratified five-fold cross-validation with shuffling.
Each iteration fits on approximately 80% of the segment and validates on the remaining
20%. These are rotating validation folds, not an additional untouched 20% test set.
Out-of-fold probabilities support ranking and probability diagnostics.

Preprocessing learned from data must be fitted on the training fold. A pipeline
protects the operations actually included in it; upstream imputation or supervised
feature construction still requires its own audit. Evaluating model choices on
the same cross-validation predictions is not an independent final test.

AUC describes discrimination of the observed status. Brier score and calibration
curves provide complementary probability diagnostics. The original project's use
of that score as commercial propensity requires validation on future conversions.
No original AUC or calibration result is published in this edition.

**The public demo does not train these classifiers.** Its input scores are synthetic.

## 4. Investable-capacity scenario

The conceptual capacity for a primary-bank relationship is:

$$
S_i=C_i+\max(0,V_i-kD_i)+A_i,
$$

where $C_i$ is savings-account balance, $V_i$ demand-deposit balance, $A_i$ other
eligible deposits, $D_i$ a monthly-expense estimate and $k$ the safety-buffer length.
Term deposits are excluded from this surplus definition.

The demo supplies a fictitious monthly expense directly. It does not infer the
original project's undocumented expense proxy or its transit-flow annualization.
Stocks and flows retain distinct meanings and units.

## 5. Campaign ranking

Within each evaluated segment, the ranking score combines two percentile ranks:

$$
R_i=\operatorname{pctRank}(S_i)\operatorname{pctRank}(p_i).
$$

The implementation gives tied values their average rank, divided by population size.
This ranking score is dimensionless. It is not a predicted cash amount, nor is it
identical to ranking directly by $S_i p_i$.

## 6. Conditional migration simulation

A simulated portfolio amount is:

$$
M=\sum_i S_i\mathbf{1}\{U_i<p_i\}f_i,
\quad U_i\sim\mathcal U(0,1),\quad f_i\sim\operatorname{Beta}(2,3).
$$

Under independent draws and fixed $S_i,p_i$, the expected amount is
$\mathbb E[M\mid S,p]=0.4\sum_i S_i p_i$.

The 5th and 95th simulated percentiles form a central 90% scenario interval.
They do not automatically include parameter-estimation errors, uncertain capacity,
common market shocks or the gap between status and future conversion.

## 7. Economic counterfactual

Let $M$ be migrated assets, $s$ the initial subscription commission, $r$ the annual
distributor commission, $m$ the annual deposit margin, $N$ contacts and $c$ cost per contact.
Let $q$ be the probability funds would leave without the campaign.

The simplified first-year difference is:

$$
\Delta I_1=M[s+r-(1-q)m]-Nc.
$$

Ignoring initial revenue and assuming no subsequent contact cost, the recurring difference is:

$$
\Delta I_{\mathrm{recurring}}=M[r-(1-q)m].
$$

The recurring break-even departure probability is $q^*=1-r/m$ for $m>0$.
When this expression is negative, there is no positive departure-risk threshold
under this simplified comparison. The subscription-only ROI
$(Ms-Nc)/(Nc)$ excludes the deposit-margin effect.

These are illustrative scenario identities. They do not constitute a funding-transfer-pricing
model, a discounted valuation or a bank's verified internal profitability calculation.

## 8. Prospective validation

A campaign pilot should freeze eligible non-investors, scores and capacity at a
reference date; define an observation horizon; and use an appropriate control group.
Track conversions, actual amounts invested, origin of funds, contact costs and net
income separately. This distinguishes observed conversion from the incremental
effect of the campaign. Such a pilot is proposed, not claimed as completed here.

## Technical references

- [scikit-learn: out-of-fold predictions](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_predict.html)
- [scikit-learn: leakage and pipelines](https://scikit-learn.org/stable/common_pitfalls.html)
- [scikit-learn: probability calibration](https://scikit-learn.org/stable/modules/calibration.html)
