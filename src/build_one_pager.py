"""Optional: render a printable one-pager (requires reportlab); output is bundled."""
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen.canvas import Canvas
from src.reward_model import ROOT, REPORTS, build_summary

BG = HexColor('#0C1428')
PANEL = HexColor('#172440')
PANEL2 = HexColor('#203150')
WHITE = HexColor('#FFFFFF')
MUTED = HexColor('#B4C3DE')
BLUE = HexColor('#5ABAFE')
ORANGE = HexColor('#FFB35A')
GREEN = HexColor('#8DEDD5')


def rect(c, x, y, w, h, color, radius=12):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, radius, stroke=0, fill=1)


def txt(c, x, y, text, size=12, color=WHITE, font='Helvetica', align='left'):
    c.setFillColor(color)
    c.setFont(font, size)
    if align == 'center':
        c.drawCentredString(x, y, text)
    elif align == 'right':
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)


def make_pdf():
    d = build_summary()
    a = d['A_official_rarity_mix_with_toy_values']
    b = d['B_hypothetical_jackpot_mix_with_toy_values']
    w, h = landscape(A4)
    c = Canvas(str(REPORTS / 'INTERVIEW_ONE_PAGER.pdf'), pagesize=(w,h))
    c.setTitle('Brawl Stars - Reward Probability & Economy Balancing | Independent Case Study')
    c.setFillColor(BG); c.rect(0, 0, w, h, stroke=0, fill=1)
    margin = 36
    txt(c, margin, h-33, 'GAME ECONOMY  /  INDEPENDENT CASE STUDY', 10, GREEN, 'Helvetica-Bold')
    txt(c, w-margin, h-33, 'BRAWL STARS  |  STARR DROPS', 10, MUTED, 'Helvetica-Bold','right')
    txt(c, margin, h-83, 'Same expected value. Different player journeys.', 26, WHITE, 'Helvetica-Bold')
    txt(c, margin, h-108, 'Question: double Legendary odds without raising the modeled reward budget?', 13, MUTED)

    rect(c, margin, h-175, w-2*margin, 49, PANEL2)
    txt(c, margin+20, h-156, 'EXPECTED VALUE PER DROP', 10, GREEN, 'Helvetica-Bold')
    txt(c, margin+258, h-159, '108  =  108', 23, WHITE, 'Helvetica-Bold')
    txt(c, w-margin-17, h-155, 'ILLUSTRATIVE UNITS ONLY', 9, MUTED, 'Helvetica-Bold', 'right')

    gap=14; tw=(w-2*margin-gap)/2; y=h-313; hh=120
    rect(c, margin, y, tw, hh, PANEL)
    rect(c, margin+tw+gap, y, tw, hh, PANEL)
    txt(c, margin+19, y+91, 'A / SUPERCELL-PUBLISHED RARITY ODDS', 10, BLUE, 'Helvetica-Bold')
    txt(c, margin+19, y+34, '2%', 43, WHITE, 'Helvetica-Bold')
    txt(c, margin+116, y+43, 'Legendary per opening', 13, MUTED)
    txt(c, margin+19, y+17, 'Rare: 50%', 11, MUTED)
    x2=margin+tw+gap
    txt(c, x2+19, y+91, 'B / HYPOTHETICAL DESIGN', 10, ORANGE, 'Helvetica-Bold')
    txt(c, x2+19, y+34, '4%', 43, WHITE, 'Helvetica-Bold')
    txt(c, x2+116, y+43, 'Legendary per opening', 13, MUTED)
    txt(c, x2+19, y+17, 'Rare: 75%', 11, MUTED)

    # Three intuition-building KPIs; no emotional inference.
    yy=h-424; k_h=92; k_gap=12; kw=(w-2*margin-2*k_gap)/3
    ks=[
        ('LEGENDARY IN 10',f'{a["chance_legendary_in_ten_pct"]:.1f}%  vs  {b["chance_legendary_in_ten_pct"]:.1f}%', 'Chance of at least one'),
        ('FIRST 5 ALL RARE',f'{a["chance_first_five_all_rare_pct"]:.1f}%  vs  {b["chance_first_five_all_rare_pct"]:.1f}%', 'A low-tier opening run'),
        ('MEDIAN OF 10',f'{a["median_units_in_ten"]:,}  vs  {b["median_units_in_ten"]:,}', 'Total illustrative units'),
    ]
    for i,(name,metric,detail) in enumerate(ks):
        x=margin+i*(kw+k_gap);rect(c,x,yy,kw,k_h,PANEL)
        txt(c,x+13,yy+69,name,10,MUTED,'Helvetica-Bold')
        txt(c,x+13,yy+39,metric,20,WHITE,'Helvetica-Bold')
        txt(c,x+13,yy+18,detail,10,MUTED)

    y_dec=72;rect(c,margin,y_dec,w-2*margin,90,PANEL2)
    txt(c,margin+15,y_dec+66,'GAME ECONOMIST TAKEAWAY',11,GREEN,'Helvetica-Bold')
    txt(c,margin+15,y_dec+45,'More jackpots can coexist with more low-tier streaks.',15,WHITE,'Helvetica-Bold')
    txt(c,margin+15,y_dec+24,'Would test player experience and long-term economy impact before proposing a rollout.',11,MUTED)
    txt(c,margin+15,y_dec+8,'The model predicts reward patterns - not emotions, retention, revenue or actual production cost.',9,MUTED)

    txt(c, margin, 43, 'MODEL: official rarity odds for A; B odds and ALL reward values invented. Independent / not endorsed by Supercell.', 8, MUTED)
    txt(c, margin, 27, 'SOURCE: Supercell Support, "Starr Drop Chances"  |  sc-brawlstars.zendesk.com  |  checked 21 Nov 2026', 8, MUTED)
    txt(c, w-margin, 27, 'NO LIVE DATA', 8, ORANGE,'Helvetica-Bold','right')
    c.linkURL('https://sc-brawlstars.zendesk.com/hc/en-us/articles/49526642756507-Starr-Drop-Chances',
              (margin,22,w-2*margin,38),relative=0)
    c.showPage();c.save()
    print(f'Built {REPORTS / "INTERVIEW_ONE_PAGER.pdf"}')

if __name__ == '__main__':
    make_pdf()
