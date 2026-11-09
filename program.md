# TopstepX 50K multi-asset research v1.6

## Mission
Find causal intraday-only 1-minute CME futures strategies for one simulated TopstepX 50K combine account. Development evidence is not proof. Optimize economic edge first; combine pass rate ranks only eligible finalists.

## What changed from v3.2, and why
v3.2 produced 42 experiments, 12 submitted runs, every one scored `0.0000`, and zero sealed-validation submissions. The gates were not too strict — the strictness was applied to the *feedback channel*. The mandated dev screen ran `--null-seeds 0`, which left `null_p = None`, which forced `score = 0` on every screen unconditionally. The leaderboard could not show progress, so nobody could rank, adopt, or build on anything.

v1.4 separates three jobs that v3.2 collapsed into one gate:

| job | v1.4 treatment |
|---|---|
| exploration signal | graded, cheap, **never zero** |
| overfit defense | **structural** — era folds + per-parameter penalty |
| final eligibility | hard, sealed, unchanged in spirit |

You now get a real number from experiment one. Use it.

## What changed in v1.5, and why
v14 ran four identical agents. All four stopped on stagnation. The best candidate
(`SHA af6eba39`, MNQ afternoon momentum plus an overnight drift-long sleeve) passed the
strongest test the development channel had: a **200-seed side null at p = 0.010**, the first
directional-evidence pass in this project's whole history. It then lost **-22,960 in 2019**
and, after one sealed slot, lost **-7,608 in 2024 and -3,620 in 2025** with sealed null
**p = 0.537**. The edge lived in 2020-2023 and nowhere else.

## What changed in v1.6

v1.5 ran ten role-specialized agents. All ten converged within hours onto the SAME
falsified v14 MNQ intraday momentum family (best dev_score 0.299, 20-seed null
p=0.4286, three independent analyst reproductions all p=0.4286). The cross-era gate
and analyst layer correctly REFUSED to ship it — zero sealed slots burned — but the
swarm wasted its budget re-deriving a dead family instead of exploring the 49-symbol
universe. v1.6 attacks the convergence failure directly:

1. **Diversity by construction, not by hope.** Each explorer gets a starting seed area
   (energy, metals, FX, rates, ags/livestock/crypto, equity-index/cross-asset). A feed
   quarantine forbids copying peers for your first 8 experiments. The leaderboard is
   collapsed to the best row per mechanism FAMILY, and the evaluator pays a small
   novelty bonus for a FAMILY tag nobody has tested yet. An idea bank of ~40 named
   mechanisms across all asset classes is provided below.
2. **Machine learning is now first-class.** xgboost, lightgbm, scikit-learn,
   statsmodels, scipy, and TA-Lib are installed alongside pandas/numpy/numba/vectorbt.
   Use them for causal feature ranking, regime filters, and cross-asset signals. The
   knob penalty and six-gate cap still apply: an ML model is a mechanism, not a way to
   smuggle in 500 free parameters. Declare your real degrees of freedom.
3. **Pivot, never stop.** The stagnation rule no longer exits the run. On stagnation
   you MUST pivot to a different family or asset class and keep going. The run ends on
   the wall clock or on a sealed PASS, not on running out of ideas.
4. **One shared sealed pool, one gatekeeper.** Six sealed slots total for the whole
   swarm. Only the gatekeeper holds a submission token; explorers and analysts
   nominate frozen SHAs via the feed. The validator runs a slot-free pre-check on dev
   (eligibility + cross-era + vectorbt PnL parity) and rejects weak candidates WITHOUT
   consuming a slot, then returns only a PASS/FAIL bit so the swarm can pivot.

Two lessons drive v1.5:

1. **Folds were not a gate.** Era-fold pass rates were reported, but nothing refused a
   one-era candidate. v1.5 adds a hard **cross-era gate**: the dev partition is split into
   three equal-count chronological sub-era blocks and **every block must be profitable under
   stressed costs**. `af6eba39` would have been blocked before burning a sealed slot.
2. **Identical agents waste identical work.** v1.5 runs **ten agents in three roles** with
   different duties, budgets, model tiers, and submission rights.

## Roles
Your role is fixed for this run. It appears in your prompt and in `.hive/role`.

| role | agents | model tier | duty | experiments | sealed slots |
|---|---|---|---|---|---|
| **explorer** | 6 | mid (`TIER-2`) | hypothesis volume and fast screens. Generate mechanisms, run `--null-seeds 0` screens, post mechanisms and screen numbers to the feed. | 30 | 0 |
| **analyst** | 3 | cheap (`TIER-3`) | verification. Reproduce peers' claimed `dev_score` by re-running their committed SHA, run `--null-seeds 20` provisional nulls on peer candidates, audit era blocks and yearly PnL, post verification results (confirmed / not reproduced / era-fragile) to the feed. | 20 | 0 |
| **gatekeeper** | 1 | frontier (`TIER-1`) | design, integration, finalists, sole submitter. Refine mechanisms, combine verified pieces, freeze finalists, run the shared sealed pool of 6 slots, post work orders to the feed. | 30 | shared pool 6 |

Rules by role:
- Only the **gatekeeper** submits sealed validation. An explorer or analyst submission is rejected and consumes no slot.
- **Analysts do not originate mechanisms.** Their value is independent reproduction. An analyst who finds a stronger mechanism hands it to the gatekeeper with evidence.
- **Explorers do not run 200-seed nulls.** That cost is reserved for the gatekeeper on frozen finalists.
- Everyone may post dev numbers, mechanisms, and era-block numbers to the feed.

## New hypothesis family: cross-sectional intraday
Every generation so far searched single-symbol directional timing and mostly searched the
same families. The evaluator loads several symbols at once: `signals(panel)` and
`entry_risk(panel)` receive one frame per symbol and may return targets for several.
**Pairs, spreads, ratios, and lead-lag between two instruments are allowed** provided every
input is causal (completed bars only, no future shifts) and no cross-market leakage is used.
Ideas in this family that respect the account model:
- equity-index relative value (MES vs MNQ, ES vs NQ) with market-neutral or hedged exposure;
- an instrument traded against another instrument's lagged move, sized inside the $300 entry-risk cap;
- session-relative behavior (one instrument's afternoon move versus its own overnight drift).

Aggregate exposure stays at most 5 standard equivalents, and every entry still needs a
causal protective-stop risk declaration.

## Account model
One shared $50,000 account. Target $3,000. Daily loss limit $1,000: evaluator flattens. EOD trailing maximum loss $2,000, locked at $50,000. At least two trading days. Best day under 50% total profit. Flat by 15:09 CT; no overnight positions. Integer positions only. Aggregate exposure at most 5 standard equivalents.

Each newly opened position needs a causal protective-stop risk declaration. `entry_risk(panel)` returns `{symbol: dollar-risk-per-contract array}` aligned with bars. Risk at entry is opened contracts times prior-bar declaration. Every entry must be at most $300. Missing declaration fails eligibility. Stop distance must exist before entry; no retrospective close-based stop.

## Universe and data
Use only cache-present CME roots: ES MES NQ MNQ YM MYM RTY M2K NKD; CL MCL QM NG MNG QG RB HO; GC MGC SI SIL HG MHG PL; 6E M6E 6B M6B 6A M6A 6C 6J 6S 6N 6M; MBT MET; ZB UB ZT ZF ZN TN; ZC ZS ZW ZL HE LE. History begins at actual product availability. Different sizes of same underlying are not independent evidence.

Execution is on Databento 1-minute OHLCV (fill next minute open), but you may build any higher timeframe (5m/15m/60m/daily) for SIGNALS by causal resampling of the completed 1-minute bars — lag them so a higher-timeframe feature is only available once its last constituent 1-minute bar has closed. UTC bar-start timestamps. Completed-bar feature available only after close; signal fills next minute open. Development only: `/data/dev/<SYMBOL>.parquet`, 2010-06 through 2023-12. Sealed validation: 2024-01 through 2025-08, never mounted for agents. Historical audit: 2025-09 through 2026-08, owner-only reused data, not fresh OOS. No raw hidden data, old task history, host memory, hidden-period probing, external services, or live trading access.

## Strategy contract
`signals(panel)` receives `{symbol: pandas.DataFrame}` and returns aligned integer target arrays. Omitted symbols flat. `entry_risk(panel)` same keys, nonnegative finite dollar risk per contract. No future shifts, centered windows, full-sample normalization, cross-market leakage, fractional sleeves, calendar/date selection, or Kelly sizing selected from backtest wins. Lag trailing windows. Maximum six independent entry gates. The knob penalty is the machine-enforced complexity brake; the six-gate cap is reviewed by the owner against your committed source and mechanism notes.

### Declare your parameters
Put every free numeric choice in one module-level mapping:

```python
PARAMS = {"lookback": 20, "atr_mult": 2.5, "vol_floor": 500}
```

The evaluator counts knobs from `PARAMS` when present. If you omit it, the evaluator falls back to counting **every distinct numeric literal** in your file, which is far more expensive. Declaring `PARAMS` is strictly cheaper and makes your degrees of freedom legible to other researchers.

## Scoring: two tiers

### `dev_score` — the leaderboard number, always available
```
dev_score = max(0, 0.7 * fold_score * positive_year_fraction + 0.3 * econ_grade - 0.001 * knobs)

econ_grade  = clip(0.5 * positive_year_fraction + 0.5 * tanh(pnl_per_year / 1000), 0, 1)
fold_score  = mean of the worst 2 of 4 contiguous era-fold pass rates
```
- `fold_score` — folds are equal-count session blocks in chronological order across 2010-2023. You cannot win by fitting one era.
- `positive_year_fraction` = share of calendar years with positive stressed PnL. Continuous, not a cliff.
- `econ_grade` is the **economic gradient**. Combine pass rate stays exactly 0 until you clear the $3,000 target, so a pass-only score would repeat the v3.2 failure in softer form — every improving candidate reads 0. `econ_grade` is bounded [0,1] and monotone in both year consistency and dollars-per-year, so progress is visible from the first experiment that stops losing money. `tanh` bounds it: +$1,000/year maps to ~0.38 of the econ half, and it saturates rather than letting one lucky year dominate.
- `knobs` = your free-parameter count. **This is the overfit brake.** Each extra knob costs 0.001. A 6-knob strategy pays 0.006 — meaningful against a 0.3-weighted econ term. Adding a parameter must earn more than it costs.

`dev_score` is never forced to zero by an eligibility gate. It floors at 0 only when the strategy is uniformly unprofitable. It is the number you submit to the Hive leaderboard during development, and the number you use to rank and adopt mechanisms.

### `score` — eligibility-gated, for finalists only
Mean of the worst three eligible yearly pass rates, zeroed unless every gate passes. This is what sealed validation uses. Do not chase it during exploration; chase `dev_score`.

## Screening ladder
Measured on dev data 2010-2023: a 20-seed null costs roughly **3 minutes per symbol** (MES alone: 2m54s). A 200-seed finalist run is therefore ~30 minutes per symbol — about 5 hours on a 10-symbol universe. Budget accordingly; do not burn experiments on 200-seed runs early.

1. **Screen** — `--null-seeds 0 --mode dev`. One pass, no permutations. Read `dev_score`, `folds`, `positive_year_fraction`, `econ_grade`, `knobs`, PnL, fills, costs, entry risk, yearly PnL, turnover, mechanism. Iterate freely here.
2. **Provisional null** — `--null-seeds 20 --mode dev`. ~3 min/symbol. Gives a directional-evidence p-value with a wide CI (resolution 1/21 ≈ 0.048, so `p <= 0.05` needs zero nulls beating you). Run this once a hypothesis looks plausible on screen, **not** on every variant. Marked `provisional: true`. Good enough to rank and to decide whether a mechanism is worth a finalist slot.
3. **Frozen finalist** — `--null-seeds 200 --mode final`. ~30 min/symbol. Freeze source SHA first. No parameter changes after seeing the null result.

Keep your finalist symbol set small. Symbol count multiplies null cost linearly and buys no additional directional evidence.

The null test flips entire session direction randomly while preserving exact entries, exits, sizes, timing, costs, and flat behavior. It tests whether your direction predicts price direction. If random signs match or beat you more than 5% of runs, your positive PnL is market drift or timing exposure, not directional edge.

**v3.2 bug fixed here:** the null now compares `worst_three_mean` (the ungated pass rate), not the eligibility-zeroed `score`. Previously a candidate failing the recent-year gate scored 0 against nulls that also scored 0 and got `p = 1.0` by construction — an unpassable test that measured nothing.

## Eligibility

Stressed costs throughout: 2 ticks slippage plus 1.5x estimated commission. New entries from 08:30–09:30 CT must not exceed 40%. Do not add correlated or losing sleeves to raise account variance.

### `--mode dev` (graded, for exploration and ranking)
1. Positive total stressed PnL.
2. `positive_year_fraction >= 0.70`.
3. **Cross-era gate (v1.5): every one of the three chronological sub-era blocks has positive stressed PnL.** The screen prints `era blocks` with per-block stressed PnL; `worst` must be positive. A candidate that only works in one era fails here before it can ever reach a sealed slot.
3. Entry-time diversity passes.
4. Every entry risk at most $300.
5. Side-null `p <= 0.05` **if a null was run**. Unrun null does not fail dev.

### `--mode final` (strict, sealed validation only)
1. Positive total stressed PnL.
2. Positive stressed PnL in **every** calendar year present in the partition. Validation has 2024 plus partial 2025, so both must be positive.
3. Entry-time diversity passes.
4. Every entry risk at most $300.
5. Side-null `p <= 0.05` from a **200-seed** run. A 20-seed provisional null does not satisfy this even at `p <= 0.05`.

Ineligible `score` is zero. Eligible candidates rank by `dev_score`, then by mean worst three yearly rolling-30-session pass rates. Report raw numbers plus every gate. Never claim edge from raw score alone.

## Experiment budget: stop on stagnation, not on a clock
Absolute ceiling is **30 recorded development experiments** per explorer and per gatekeeper, **20** per analyst. Across pivots, not per family. You are not required to use all 30 — v3.2 agents that quit early and agents that ground out 22 uninformative runs both wasted the run.

**Pivot rule (v1.6):** track your best `dev_score` within your CURRENT family. If it has not improved within your last **8** recorded experiments, you are stagnating in that family. Do NOT exit. PIVOT: pick a different mechanism family or asset class from the idea bank (or an un-claimed peer family) and continue. Record the pivot in `experiments.jsonl` and on the feed. The run ends on the wall clock or a sealed PASS, not on stagnation.

Conversely, while `dev_score` keeps improving within a family, keep going. Improvement is the only reason to keep spending budget on that family.

Every change, crash, screen, or variant counts as an experiment. No unrecorded grid/random sweeps. Append to `experiments.jsonl`: hypothesis, source SHA256, symbols, `dev_score`, `fold_score`, `positive_year_fraction`, `knobs`, all four fold rates, raw screen metrics, provisional or frozen null result if run, eligibility gates, economics, mechanism, and variants. Commit only `strategy.py`, `experiments.jsonl`, and mechanism notes. Push, then submit.

## Idea bank (seed areas and mechanism families)
Use only cache-present symbols. Tag every strategy with `FAMILY = "<slug>"` in source; the
evaluator pays a novelty bonus for a family not yet in the shared family ledger, and the
leaderboard shows one row per family so a crowded family cannot dominate. Do not all pile
onto one family.

Seed areas (one per explorer at start; leave after 8 experiments if it is dry):
- **energy**: CL MCL QM NG MNG QG RB HO
- **metals**: GC MGC SI SIL HG MHG PL
- **fx**: 6E M6E 6B M6B 6A M6A 6C 6J 6S 6N 6M
- **rates**: ZB UB ZT ZF ZN TN
- **ags-livestock-crypto**: ZC ZS ZW ZL HE LE MBT MET
- **equity-index-cross-asset**: ES MES NQ MNQ YM MYM RTY M2K NKD and cross-asset pairs

Mechanism families (claim with `hive feed claim`; one claim per agent at a time):
1. Inventory-report drift: CL around weekly EIA (Wed), NG around EIA (Thu).
2. Mean reversion to settlement / prior close after an overnight gap.
3. Opening-range breakout with volatility filter (first 5-30 min).
4. London/NY session-handoff momentum in FX (6E 6B 6J).
5. FX fixing flow around 16:00 London (11:00 CT).
6. Treasury auction-day drift in rates (ZN ZB ZF around 13:00 ET).
7. Rates curve relative value: ZF vs ZN vs ZB calendar/butterfly.
8. Grain seasonality and report-day (USDA WASDE) drift: ZC ZS ZW ZL.
9. Crack-spread and HO/RB/CL energy-complex relative value.
10. Gold/silver ratio (GC/SI) mean reversion and trend.
11. Copper-gold (HG/GC) macro risk-on/off cross-signal.
12. Equity-index cross-sectional relative value: MES vs MNQ vs MYM vs M2K, hedged.
13. Lead-lag: does ES lead RTY/M2K by 1-3 minutes in a causal window?
14. Volatility regime filter (any asset): trade only in a vol band via ATR/realized vol.
15. Overnight-vs-intraday return decomposition (any liquid symbol).
16. Time-of-day seasonality curves per symbol (causal, walk-forward).
17. Carry / roll-yield tilt in calendar-spread-adjacent single contracts.
18. Post-settlement drift in energies and metals after 14:30 CT settle.
19. Cross-asset risk barometer: trade an equity index only when a rates/FX confirm aligns.
20. Dollar-index proxy (basket of 6E 6B 6J) as a filter on metals and energies.
21. Bitcoin (MBT) weekend/session-gap behavior vs equity index.
22. Volatility-spike fade vs continuation, conditioned on symbol and time of day.
23. Multi-symbol ML regime filter: xgboost/lightgbm predicts next-bar direction sign from
    causal cross-asset features; gate entries by predicted class probability. Keep the
    feature set small and declare it; the knob penalty still applies.
24. Feature-ranked momentum: use feature_importances_ to pick 2-3 causal features, then a
    transparent linear/tree rule (not a black box with 500 knobs).
25. Cross-validated walk-forward logistic/linear signal on engineered causal features.
26. Volume-profile / high-volume-node reversion using causal rolling volume at price.
27. ATR-scaled breakout with time-stop and cost-aware position sizing.
28. Overnight drift long in energies vs fade in equities (sign asymmetry by asset class).
29. Month-end / turn-of-month effects in equity indexes and bonds.
30. Day-of-week seasonality per asset class (causal, walk-forward).
31. First-hour range as a predictor of rest-of-day range (vol targeting).
32. Cross-asset correlation breakdown: trade when a historically correlated pair decorrelates.
33. Micro-vs-standard basis: MES vs ES intraday microstructure divergence (same underlying,
    NOT independent evidence — use as execution/sizing, not a second signal).
34. Stop-run / sweep-and-revert around prior day high/low in liquid symbols.
35. Trend-following on resampled 5m/15m/60m bars (build higher timeframes causally from 1m).
36. Donchian/channel breakout with portfolio-level exposure cap.
37. Mean-reversion on z-score of resampled returns, per-symbol walk-forward band.
38. Cross-momentum: sort a small basket by trailing return, long winner / short loser, hedged.
39. Event-volatility compression/expansion around scheduled releases, any asset.
40. Genetic/programmatic search: evolve a small expression tree of causal indicators with a
    hard knob budget; freeze and declare the final rule exactly like any other mechanism.

A family that two generations have falsified with a 200-seed null is DEAD: MNQ/PM-session
single-symbol intraday momentum and overnight-drift-long are falsified. Do not re-derive
them. They appear here only so you recognize and avoid them.

## Collaboration
Development scores are **shareable and should be shared**. Post your mechanism, `dev_score`, fold breakdown, and provisional `p` to the feed. The v3.2 ban was on requesting *sealed validation* results — that ban stands. It was never a ban on dev numbers, and treating it as one is why v3.2 agents hoarded.

Adopting another researcher's mechanism is encouraged and cheap: you do **not** need to reproduce their 200-seed null. Re-test the mechanism on your own symbols and folds at `--null-seeds 0` or `20`, and record it as your own experiment with attribution. Verify a claimed `dev_score` by re-running their committed SHA before you build on it.

Claim work with `hive feed claim` to avoid duplicating a mechanism already in flight.

## Sealed validation
**Gatekeeper only, against a SHARED pool of 6 slots for the whole swarm.** Explorer and
analyst submissions are rejected and consume nothing; they nominate frozen SHAs to the
gatekeeper via the feed.

Before freezing anything, the gatekeeper must confirm on development data that all three
cross-era blocks are positive, `positive_year_fraction >= 0.70`, every entry risk <= $300,
and the 200-seed null passes at `p <= 0.05`. Freeze distinct SHA256 finalists. Submit:

```bash
python3 /usr/local/bin/v16-validate --strategy strategy.py --symbols MES,MGC
```

The validator runs a slot-free pre-check on dev: eligibility, cross-era gate, the 200-seed
null, and a vectorbt PnL-parity replay of the exact trade ledger. A pre-check failure
REJECTS the candidate WITHOUT consuming a slot, so weak candidates are cheap. Only a
candidate that clears the pre-check consumes one of the 6 shared slots and runs on sealed
data. The response is a PASS/FAIL bit plus the pool count — no sealed metrics, errors,
traces, or timing. A FAIL means pivot to a different family; do not resubmit a tweaked
variant of the same dead family. Read your bits any time with:

```bash
python3 /usr/local/bin/v16-validate --status
```

A PASS is the goal of the whole run: report it and stop. Do not change candidate or
identity to evade the pool. The validator reruns 200 null seeds at `--mode final` on sealed
data and records full eligibility for owner review only.
