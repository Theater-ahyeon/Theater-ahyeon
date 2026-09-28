"""Build self-contained README SVGs from generated illustrations."""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'


def image(name):
    return 'data:image/jpeg;base64,' + base64.b64encode((ASSETS / 'art' / name).read_bytes()).decode()


def star(x, y, size=8, color='#D9C089'):
    return f'<path d="M{x},{y-size} Q{x+1},{y-1} {x+size},{y} Q{x+1},{y+1} {x},{y+size} Q{x-1},{y+1} {x-size},{y} Q{x-1},{y-1} {x},{y-size}Z" fill="{color}"/>'


def frame(w, h, color):
    return f'<g fill="none" stroke="{color}" stroke-width="1" opacity=".8"><rect x="12" y="12" width="{w-24}" height="{h-24}" rx="4"/><path d="M30,36V24H52 M{w-52},24H{w-30}V36 M30,{h-36}V{h-24}H52 M{w-52},{h-24}H{w-30}V{h-36}"/></g>'


def build():
    for theme in ('dark', 'light'):
        dark = theme == 'dark'
        gold = '#D9C089' if dark else '#9B7840'
        ink = '#F7F5EE' if dark else '#172D50'
        base = '#101A3A' if dark else '#F7F5EE'
        hero = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="480" viewBox="0 0 1200 480" role="img" aria-label="Theater-ahyeon — code, notes, and side projects. Phoebe in a luminous cathedral.">
<title>Theater-ahyeon — code, notes, and side projects.</title>
<defs><linearGradient id="shade"><stop stop-color="{base}" stop-opacity=".8"/><stop offset=".43" stop-color="{base}" stop-opacity=".6"/><stop offset=".65" stop-color="{base}" stop-opacity="0"/></linearGradient></defs>
<image width="1200" height="480" href="{image(f'hero-{theme}.jpg')}" preserveAspectRatio="xMidYMid slice"/>
<path fill="url(#shade)" d="M0 0H1200V480H0Z"/>{frame(1200,480,gold)}
<g font-family="Georgia, 'Times New Roman', serif">
<text x="62" y="160" fill="{gold}" font-size="13" letter-spacing="5">A LITTLE LIGHT, A LITTLE CODE</text>
<text x="58" y="241" fill="{ink}" font-size="60" letter-spacing="-1.8">Theater-ahyeon</text>
<text x="62" y="281" fill="{ink}" font-size="20" letter-spacing="2">code, notes, and side projects.</text>
<path d="M62 319H174 M202 319H314" stroke="{gold}" opacity=".8"/>{star(188,319,8,gold)}
<text x="62" y="369" fill="{gold}" font-size="12" letter-spacing="4">PHOEBE · WUTHERING WAVES</text></g></svg>'''
        (ASSETS / f'hero-{theme}.svg').write_text(hero, encoding='utf-8')
        divider = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="44" viewBox="0 0 1200 44"><defs><linearGradient id="line" gradientUnits="userSpaceOnUse" x1="0" y1="22" x2="1200" y2="22"><stop stop-color="{gold}" stop-opacity="0"/><stop offset=".5" stop-color="{gold}"/><stop offset="1" stop-color="{gold}" stop-opacity="0"/></linearGradient></defs><path d="M0 22H572 M628 22H1200" stroke="url(#line)"/><circle cx="600" cy="22" r="14" fill="none" stroke="{gold}" opacity=".65"/>{star(600,22,20,gold)}{star(568,22,4,gold)}{star(632,22,4,gold)}</svg>'''
        (ASSETS / f'divider-{theme}.svg').write_text(divider, encoding='utf-8')
        footer = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="250" viewBox="0 0 1200 250" role="img" aria-label="Thanks for stopping by. A cathedral opens onto a sunlit sea."><title>thanks for stopping by.</title>
<defs><linearGradient id="veil" x2="0" y2="1"><stop stop-color="{base}" stop-opacity=".1"/><stop offset=".55" stop-color="{base}" stop-opacity=".15"/><stop offset="1" stop-color="{base}" stop-opacity=".95"/></linearGradient></defs>
<image width="1200" height="250" href="{image('footer.jpg')}" preserveAspectRatio="xMidYMid slice"/>
<path d="M0 0H1200V250H0Z" fill="url(#veil)"/>{frame(1200,250,gold)}
<text x="600" y="212" text-anchor="middle" font-family="Georgia,serif" font-size="21" letter-spacing="3" fill="{ink}">thanks for stopping by.</text></svg>'''
        (ASSETS / f'footer-{theme}.svg').write_text(footer, encoding='utf-8')


if __name__ == '__main__':
    build()
