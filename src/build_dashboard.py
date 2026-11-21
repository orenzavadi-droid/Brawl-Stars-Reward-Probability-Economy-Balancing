"""Build a self-contained HTML exhibit from the model's exact results (stdlib only)."""
import json
from pathlib import Path
from src.reward_model import ROOT, REPORTS, write_outputs


def build():
    d = write_outputs()
    a = d["A_official_rarity_mix_with_toy_values"]
    b = d["B_hypothetical_jackpot_mix_with_toy_values"]
    vals = d["teaching_value_by_rarity"]
    rarities = list(vals)
    rows = "\n".join(
        f'''<div class="bar-row"><span class="tier-name">{r}</span>
        <div class="bar-area"><div class="bar-label"><span>A <b>{a['probabilities_pct'][r]:g}%</b></span><span>B <b>{b['probabilities_pct'][r]:g}%</b></span></div>
        <div class="bars"><div class="track"><div class="fill a" style="width:{a['probabilities_pct'][r]}%"></div></div><div class="track"><div class="fill b" style="width:{b['probabilities_pct'][r]}%"></div></div></div></div>
        <span class="units">{vals[r]:,}<small>units</small></span></div>'''
        for r in rarities)
    payload = json.dumps({"A": [a["probabilities_pct"][r] / 100 for r in rarities],
                          "B": [b["probabilities_pct"][r] / 100 for r in rarities],
                          "rarities": rarities, "values": [vals[r] for r in rarities]})
    html = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brawl Stars — Reward Probability &amp; Economy Balancing</title>
<style>
:root{--bg:#0b1024;--p:#151d39;--p2:#202b4b;--white:#f6f8ff;--muted:#acb9d5;--a:#5abaff;--b:#ffa948;--line:#384567;--green:#8dedd5}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(ellipse at 50% 0%,#223660 0,#10192f 40%,#0b1024 74%);color:var(--white);font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.5}
.wrap{max-width:1080px;margin:auto;padding:26px 32px 70px}.top{display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:12px;color:var(--muted);letter-spacing:.12em;font-weight:800}.top strong{color:#fff}.tag{padding:6px 12px;border:1px solid #44577e;border-radius:30px;font-size:11px;letter-spacing:.07em}
.hero{padding:65px 0 32px;max-width:970px}.eyebrow{font-size:12px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--green)}h1{font-size:clamp(36px,6vw,66px);line-height:1.05;letter-spacing:-.045em;margin:17px 0 16px}.sub{font-size:clamp(17px,2.2vw,22px);color:var(--muted);max-width:740px}.sub strong{color:#fff}.star{color:#ffd16b}h2{font-size:25px;letter-spacing:-.025em;margin:0 0 8px}p{margin:0 0 12px}small,.note{color:var(--muted);font-size:12px}
.thesis{display:flex;align-items:center;gap:18px;border:1px solid #607c93;padding:20px 24px;border-radius:16px;margin:20px 0 32px;background:#162848}.thesis .mark{font-size:32px}.thesis p{margin:0;font-size:18px;font-weight:700}.thesis span{color:var(--green)}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:15px}.card{background:linear-gradient(160deg,#1c2846,#121a33);border:1px solid var(--line);border-radius:18px;padding:24px}.card.a{border-top:4px solid var(--a)}.card.b{border-top:4px solid var(--b)}.card h3{font-size:22px;letter-spacing:-.02em;margin:7px 0 4px}.policy{font-size:12px;letter-spacing:.1em;text-transform:uppercase;font-weight:900}.policy.a{color:var(--a)}.policy.b{color:var(--b)}.big{font-size:54px;font-weight:850;line-height:1.1;letter-spacing:-.05em}.small{font-size:13px;color:var(--muted)}.divider{height:1px;background:var(--line);margin:18px 0}.cost{text-align:center;border:1px solid var(--line);border-radius:16px;margin:18px 0 30px;padding:20px;background:#131e36}.cost strong{font-size:32px}.cost .hint{font-size:14px;color:var(--muted)}
.section{margin-top:42px}.section-head{margin-bottom:15px}.panel{border:1px solid var(--line);border-radius:16px;padding:24px;background:var(--p)}.bar-row{display:grid;grid-template-columns:110px 1fr 65px;gap:18px;align-items:center;padding:12px 0;border-bottom:1px solid #2f3a55}.bar-row:last-child{border:none}.tier-name{font-weight:750;font-size:14px}.bar-label{display:flex;justify-content:space-between;color:var(--muted);font-size:12px}.bar-label b{color:white}.bars{display:grid;gap:5px;margin-top:6px}.track{height:9px;background:#333f5f;border-radius:10px;overflow:hidden}.fill{height:100%;border-radius:10px}.fill.a{background:var(--a)}.fill.b{background:var(--b)}.units{text-align:right;font-weight:800}.units small{display:block;font-weight:500}
.metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}.metric{background:#182440;border-radius:16px;padding:21px;border:1px solid var(--line)}.metric .label{color:var(--muted);font-size:12px;font-weight:700;min-height:34px}.metric .nums{display:flex;align-items:center;justify-content:space-between;gap:5px;margin:10px 0 8px}.metric .nums strong{font-size:23px}.metric .nums span{color:#8492ae}.metric .explain{font-size:12px;color:var(--muted)}
.bullet{display:flex;gap:12px;margin:14px 0}.num{display:grid;place-items:center;flex-shrink:0;height:24px;width:24px;border-radius:50%;background:#334668;color:#eaf1ff;font-size:12px;font-weight:800}.path{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.path .card{padding:20px}.path b{font-size:15px}.path p{color:var(--muted);font-size:13px;margin-top:9px}
button{border:0;border-radius:12px;padding:12px 17px;font-weight:800;background:var(--green);color:#0a1630;cursor:pointer;font-size:14px}button:hover{filter:brightness(1.07)}.simhead{display:flex;align-items:center;justify-content:space-between;gap:12px}.trial-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}.trial{padding:16px;border:1px solid var(--line);border-radius:14px;background:#101a34}.drops{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;margin:12px 0}.drop{border:1px solid #43526e;border-radius:8px;text-align:center;padding:9px 2px;font-size:10px;font-weight:750;background:#293553}.drop.Legendary{background:#705021;border-color:#e1ad58;color:#fff0bb}.drop.Mythic{background:#5f315c;border-color:#a15fa7}.drop.Epic{background:#4f3b75;border-color:#8764c9}.drop.Super-Rare{background:#245a79;border-color:#4288bc}.total{font-size:15px;font-weight:800}.trial .hint{color:var(--muted);font-size:11px}.foot{margin-top:38px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:18px}.foot a{color:var(--a)}
@media(max-width:700px){.wrap{padding:20px 15px 35px}.hero{padding:39px 0 20px}.cards,.metric-grid,.path,.trial-grid{grid-template-columns:1fr}.metric .label{min-height:0}.bar-row{grid-template-columns:82px 1fr 45px;gap:9px}.panel{padding:16px}.tier-name{font-size:12px}.units{font-size:12px}.thesis p{font-size:16px}.top{letter-spacing:.03em}.tag{font-size:10px}.simhead{align-items:start;flex-direction:column}}
@media print{body{background:#fff;color:#111}.wrap{max-width:none}.card,.panel,.metric,.thesis,.cost{background:#f3f5fb;color:#111;border-color:#ccc}.sub,.small,.note,.metric .label,.metric .explain,.path p{color:#555}button,.trial-grid{display:none}}
</style></head>
<body><main class="wrap">
<div class="top"><div><strong>GAME ECONOMY</strong> / INDEPENDENT CASE STUDY</div><span class="tag">BRAWL STARS · STARR DROPS</span></div>
<header class="hero"><div class="eyebrow">Reward probability &amp; economy balancing</div>
<h1>Same expected value.<br><span class="star">Different player journeys.</span></h1>
<p class="sub">What if we <strong>double Legendary odds</strong> without increasing modeled reward cost? The answer is a design trade-off, not a free win.</p></header>
<div class="thesis"><div class="mark">✦</div><p>Core takeaway: <span>More jackpots can also mean more low-tier streaks.</span></p></div>
<div class="cards"><div class="card a"><div class="policy a">A · published rarity odds</div><h3>Balanced distribution</h3><p class="small">Supercell's disclosed regular Starr Drop rarity chances; simplified teaching payout values.</p><div class="divider"></div><div class="big">2%</div><div class="small">Legendary per opening</div></div>
<div class="card b"><div class="policy b">B · hypothetical concept</div><h3>Jackpot-heavy distribution</h3><p class="small">Invented alternative: twice the Legendary chance, balanced by more Rare drops.</p><div class="divider"></div><div class="big">4%</div><div class="small">Legendary per opening</div></div></div>
<div class="cost"><div class="hint">EXPECTED VALUE PER OPENING · SAME IN BOTH MODELS</div><strong>108 = 108</strong><div class="hint">Illustrative value units only · not actual Brawl Stars currency, item value, or studio cost</div></div>
<section class="section"><div class="section-head"><h2>01 / The economy rule</h2><p class="note">One input table. Published rarity odds for A; invented B odds and invented per-tier values.</p></div><div class="panel">__ROWS__</div></section>
<section class="section"><div class="section-head"><h2>02 / The player-journey trade-off</h2><p class="note">Exact model probabilities assuming independent openings. These are <strong>not</strong> empirical measures of emotion.</p></div><div class="metric-grid">
<div class="metric"><div class="label">Chance of ≥1 Legendary in 10 openings</div><div class="nums"><strong style="color:var(--a)">__A_JACK__%</strong><span>→</span><strong style="color:var(--b)">__B_JACK__%</strong></div><div class="explain">B creates more opportunities for a standout moment.</div></div>
<div class="metric"><div class="label">Chance the first 5 openings are all Rare</div><div class="nums"><strong style="color:var(--a)">__A_RARE__%</strong><span>→</span><strong style="color:var(--b)">__B_RARE__%</strong></div><div class="explain">B also makes a low-tier run much more common.</div></div>
<div class="metric"><div class="label">Median total teaching units over 10 openings</div><div class="nums"><strong style="color:var(--a)">__A_MED__</strong><span>→</span><strong style="color:var(--b)">__B_MED__</strong></div><div class="explain">A more 'typical' ten-drop total is lower in B.</div></div>
</div></section>
<section class="section"><div class="panel"><div class="simhead"><div><h2 style="margin:0">03 / Try the reward rhythm</h2><p class="note">A playful illustration with the published vs hypothetical rarity mix. No money, no player data.</p></div><button id="go" type="button">Show 10 openings</button></div>
<div class="trial-grid"><div class="trial"><div class="policy a">A / published odds</div><div id="dropsA" class="drops"><span class="hint">Click to see one possible path</span></div><div id="totalA" class="total">—</div></div>
<div class="trial"><div class="policy b">B / invented odds</div><div id="dropsB" class="drops"><span class="hint">Click to see one possible path</span></div><div id="totalB" class="total">—</div></div></div>
<p class="note" style="margin-top:12px">One draw is an anecdote; the calculated percentages above are the model's exact probabilities. An interaction is not a psychological experiment.</p></div></section>
<section class="section"><div class="section-head"><h2>04 / The Game Economist decision</h2><p class="note">What would I actually recommend before changing production odds?</p></div><div class="path"><div class="card"><div class="num">1</div><b>State the feeling</b><p>Is the intent steady progress or rare moments of excitement? Which player segment?</p></div><div class="card"><div class="num">2</div><b>Audit the economy</b><p>Use real item/fallback values and inventory. Equal fictional EV is not equal real cost.</p></div><div class="card"><div class="num">3</div><b>Playtest → A/B</b><p>Ask how rewarded players felt; then measure voluntary play and economy guardrails.</p></div></div></section>
<div class="thesis" style="margin-top:38px"><div class="mark">↗</div><p><span>Interview line:</span> "I model the experience I intend to create, then test whether players actually experience it."</p></div>
<footer class="foot">Independent portfolio exercise, not affiliated with Supercell. Only the A rarity odds are sourced from <a href="https://sc-brawlstars.zendesk.com/hc/en-us/articles/49526642756507-Starr-Drop-Chances" target="_blank" rel="noopener">Supercell's Starr Drop Chances</a> (checked 21 Nov 2026). B odds and both value schedules are fictional. No real economy cost, retention, preference, satisfaction or causality is established. <span style="color:#fff">Design first. Validate second.</span></footer>
</main>
<script>
const model = __MODEL__;
function dropFor(u,ps){ let sum=0;for(let i=0;i<ps.length;i++){sum+=ps[i];if(u<sum || i===ps.length-1)return i;}return ps.length-1;}
function draw(){const common=Array.from({length:10},()=>Math.random()); for(const p of ['A','B']){const indices=common.map(u=>dropFor(u,model[p]));document.getElementById('drops'+p).innerHTML=indices.map(i=>'<span class="drop '+model.rarities[i].replaceAll(' ','-')+'">'+model.rarities[i]+'</span>').join('');const total=indices.reduce((s,i)=>s+model.values[i],0);document.getElementById('total'+p).textContent=total.toLocaleString()+' illustrative units';}}
document.getElementById('go').addEventListener('click',draw);
</script></body></html>'''
    replacements = {
        "__ROWS__": rows, "__MODEL__": payload,
        "__A_JACK__": f'{a["chance_legendary_in_ten_pct"]:.1f}',
        "__B_JACK__": f'{b["chance_legendary_in_ten_pct"]:.1f}',
        "__A_RARE__": f'{a["chance_first_five_all_rare_pct"]:.1f}',
        "__B_RARE__": f'{b["chance_first_five_all_rare_pct"]:.1f}',
        "__A_MED__": f'{a["median_units_in_ten"]:,}',
        "__B_MED__": f'{b["median_units_in_ten"]:,}',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    output = REPORTS / "interactive_case.html"
    output.write_text(html, encoding="utf-8")
    print(f"Built {output}")

if __name__ == '__main__':
    build()
