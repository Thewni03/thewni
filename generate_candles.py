import urllib.request
import json
import math
from datetime import datetime, timedelta

USERNAME = "Thewni03"

def fetch_contributions():
    url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}?y=last"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
            return data.get("contributions", [])
    except:
        return []

def generate_svg(weeks_data):
    W, H, pad, bw = 640, 220, 30, 18
    last20 = weeks_data[-20:]
    max_val = max((w for w in last20), default=1) or 1
    step = (W - pad * 2) / len(last20)

    inner = ""
    for i, w in enumerate(last20):
        x = pad + i * step + step / 2
        bar_h = max(4, (w / max_val) * (H - pad * 2 - 30))
        y = H - pad - bar_h
        intensity = w / max_val
        if intensity < 0.25:
            c = "#ffd6e7"
        elif intensity < 0.5:
            c = "#ffb6c1"
        elif intensity < 0.75:
            c = "#FF6B9D"
        else:
            c = "#d63d78"

        inner += f'<rect x="{x-bw/2:.1f}" y="{y:.1f}" width="{bw}" height="{bar_h:.1f}" rx="3" fill="{c}"/>'
        inner += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y-10:.1f}" stroke="#ffb6c1" stroke-width="1.2"/>'
        inner += f'<circle cx="{x:.1f}" cy="{y-13:.1f}" r="3" fill="#FFD700" opacity="0.9"/>'
        if w > 0:
            inner += f'<text x="{x:.1f}" y="{H-pad+14:.1f}" text-anchor="middle" fill="#ffb6c1" font-size="9" font-family="sans-serif">{w}</text>'

    updated = datetime.utcnow().strftime("%b %d, %Y")
    inner += f'<text x="320" y="{H-2}" text-anchor="middle" fill="#ffb6c1" font-size="10" font-family="sans-serif">last 20 weeks · updated {updated}</text>'

    return f'''<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" role="img">
<title>Thewni's weekly commit candle chart</title>
<desc>Candle chart showing weekly GitHub commits, auto-updated daily</desc>
{inner}
</svg>'''

def main():
    contributions = fetch_contributions()
    weeks = []
    for i in range(0, len(contributions), 7):
        week = contributions[i:i+7]
        weeks.append(sum(d.get("count", 0) for d in week))

    svg = generate_svg(weeks)
    with open("candles.svg", "w") as f:
        f.write(svg)
    print("candles.svg generated successfully!")

if __name__ == "__main__":
    main()
