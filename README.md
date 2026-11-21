# Brawl Stars — Reward Probability & Economy Balancing

**Independent Game Economist case study | official Starr Drop rarity odds + hypothetical counterfactual**

> **One sentence:** **Same expected reward budget. Different player experience risk.**

## The design question (15 seconds)

**Would you double Legendary drop odds if it also makes strings of low-tier drops much more common?**

Supercell's published rarity probabilities for **regular Starr Drops** are the factual anchor. I designed a **fictional alternative distribution** that doubles Legendary rarity odds **while keeping expected reward value identical**, under an explicitly *invented* common value scale.

This is about one Game Economist decision: **which probability mix creates the intended reward rhythm without silently increasing the modeled reward budget?**

## Understand the project in one table

| Rarity | A: Supercell-published rarity odds | B: **invented** jackpot-heavy odds | **invented** value per tier (teaching units) |
|---|---:|---:|---:|
| Rare | 50% | 75% | 50 |
| Super Rare | 28% | 8% | 100 |
| Epic | 15% | 10% | 150 |
| Mythic | 5% | 3% | 250 |
| Legendary | 2% | 4% | 1,000 |

**Math:** Expected value per opening = Σ(probability × invented value).

- **A = (0.50×50) + (0.28×100) + (0.15×150) + (0.05×250) + (0.02×1000) = 108 units**.
- **B = (0.75×50) + (0.08×100) + (0.10×150) + (0.03×250) + (0.04×1000) = 108 units**.

Units are **not Coins, USD, Gems, actual prize values, or actual studio costs**. B is **not an update or proposed real live setting**. The example assumes independent openings and fixed tier values; the real loot system has varied item classes, account eligibility and fallback rewards.

## Results: EXACT probabilities, not measured player behavior

| Metric | A: published odds + toy values | B: invented counterfactual | Interpretation |
|---|---:|---:|---|
| **Expected value / opening** | **108** | **108** | Same illustrative reward budget |
| **At least one Legendary in 10 openings** | **18.3%** | **33.5%** | More jackpot exposure |
| **First five openings all Rare** | **3.1%** | **23.7%** | Much more frequent low-tier opening sequence |
| **Median total value across 10 openings** | **950** | **800** | Typical session has lower modeled reward total |

**Design insight:** **Doubling rare jackpot odds is not automatically a better experience.** It creates upside for some players, but also longer runs of low rewards. The model establishes *probabilities*, not real satisfaction, motivation, frustration or retention.

## What I would do in a real studio

1. **Design intent:** Choose whether the game should feel consistently rewarding or occasionally spectacular. Specify whose experience matters (e.g., new vs veteran players).
2. **Player check:** Prototype ten non-monetized openings per variant; ask players how rewarding the sequence felt (1–5) and whether they'd like another opening (1–5). Treat results as preliminary and avoid harmful pressure to spend.
3. **A/B plan:** Randomize eligible **players** once, not individual drops. Compare pre-registered player-level satisfaction (from a sampled survey), continued voluntary engagement, and economic guardrails such as actual item grants, inventory and net virtual-currency flows. Predefine time window and minimum meaningful effect; monitor segment heterogeneity.
4. **Only then adjust:** Estimate actual item/rarity value using game telemetry and player inventory; do not use our invented unit values for production.

## Open the project / reproduce it

- **[`reports/interactive_case.html`](reports/interactive_case.html)** — one-page visual case, self-contained, includes a 10-drop *illustration* you can click. No external assets or server.
- **[`reports/INTERVIEW_ONE_PAGER.pdf`](reports/INTERVIEW_ONE_PAGER.pdf)** — 1-page interview handout.
- **[`START_HERE_HE.md`](START_HERE_HE.md)** — shortest Hebrew walkthrough: understand in 90 seconds.
- **[`INTERVIEW_CHEAT_SHEET_HE.md`](INTERVIEW_CHEAT_SHEET_HE.md)** — short Hebrew study notes + 45-second English pitch.
- **[`RED_TEAM.md`](RED_TEAM.md)** — limitations and hard interview questions.
- **[`data/reward_design.csv`](data/reward_design.csv)** — one editable input table, official vs invented.
- **[`src/reward_model.py`](src/reward_model.py)** — dependency-free exact probability model; writes `reports/summary.json` and `reports/ten_drop_total_distribution.csv`.

Run (Python 3.10+; zero pip installs):

```bash
python -m src.reward_model
python -m src.build_dashboard
python -m unittest discover -s tests -v
```

The optional one-pager regeneration command is `python -m src.build_one_pager` (requires `pip install reportlab`). The prebuilt PDF is included.

The dashboard is a designed visualization of a deterministic model. **Its clickable openings are examples, not a human playtest or empirical result.**

## Sources and independence

- **Supercell official rarity odds:** [Starr Drop Chances — Supercell Support](https://sc-brawlstars.zendesk.com/hc/en-us/articles/49526642756507-Starr-Drop-Chances), checked 21 November 2026. Regular Starr Drops: Rare 50%, Super Rare 28%, Epic 15%, Mythic 5%, Legendary 2%.
- **How drops operate:** [Supercell Support — Drop Chances](https://sc-brawlstars.zendesk.com/hc/en-us/articles/49526625944987-Drop-Chances). Actual rewards depend on category, eligibility, and fallback rules.

**Not affiliated with, endorsed or commissioned by Supercell.** No game art, logos, game data, internal metrics or copyrighted assets reproduced. The game and mechanic are referenced descriptively. All values and alternative odds invented, and all numerical outputs conditional on those assumptions.
