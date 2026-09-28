"""Build the optional Sea Glow theme from the owner's selected illustration."""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/sea-glow'


def build():
    OUT.mkdir(exist_ok=True)
    art = 'data:image/jpeg;base64,' + base64.b64encode((ROOT/'assets/art/sea-glow.jpg').read_bytes()).decode()
    for theme in ('dark', 'light'):
        bg, ink, accent, line = ('#142235','#F0F2F3','#D4BF97','#36495C') if theme == 'dark' else ('#F4F6F7','#22394B','#836C42','#D4DDE2')
        def svg(h, body, title):
            return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>'
        hero = f'''<image width="1200" height="400" href="{art}"/>
<g font-family="Georgia,serif" fill="#F0F2F3">
<text x="54" y="116" font-family="Arial,sans-serif" font-size="12" letter-spacing="4" fill="#D4BF97">NOTES FROM THE QUIET HOURS</text>
<text x="50" y="198" font-size="58" letter-spacing="-1.7">Theater-ahyeon</text>
<text x="54" y="240" font-size="20" letter-spacing="1">code, notes, and side projects.</text>
<path d="M54 275H178" stroke="#D4BF97" stroke-width="1"/>
<text x="54" y="310" font-size="13" fill="#BCCBD5" letter-spacing="2">PHOEBE / SEA GLOW</text></g>
<rect y="400" width="1200" height="4" fill="{accent}"/>'''
        (OUT/f'hero-{theme}.svg').write_text(svg(404,hero,'Theater-ahyeon — Sea Glow'),encoding='utf-8')
        divider = f'<path d="M0 24H550 M650 24H1200" stroke="{line}"/><path d="M568 24q16-12 32 0t32 0" fill="none" stroke="{accent}" stroke-width="2"/>'
        (OUT/f'divider-{theme}.svg').write_text(svg(48,divider,'Sea Glow divider'),encoding='utf-8')
        footer = f'''<rect width="1200" height="150" rx="8" fill="{bg}"/>
<path d="M0 105Q150 80 300 105T600 105T900 105T1200 105 M0 119Q150 94 300 119T600 119T900 119T1200 119" fill="none" stroke="{line}"/>
<text x="600" y="64" text-anchor="middle" font-family="Georgia,serif" font-size="25" letter-spacing="2" fill="{ink}">thanks for stopping by.</text>
<text x="600" y="92" text-anchor="middle" font-family="Arial,sans-serif" font-size="12" letter-spacing="3" fill="{accent}">UNTIL THE NEXT TIDE</text>'''
        (OUT/f'footer-{theme}.svg').write_text(svg(150,footer,'Thanks for stopping by. Until the next tide.'),encoding='utf-8')


if __name__ == '__main__':
    build()
