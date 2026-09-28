"""Build the Phoebe sticker-notebook profile; no external SVG resources."""
import base64
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'

def build():
    sticker = 'data:image/png;base64,' + base64.b64encode((ASSETS/'art/phoebe-sticker.png').read_bytes()).decode()
    for theme in ('dark','light'):
        dark = theme == 'dark'
        paper,ink,line,blue,purple = ('#242636','#F7F0DC','#44485E','#A6C8F5','#C6B4EF') if dark else ('#FFF9EC','#353347','#E3DFD4','#6797C9','#9173BD')
        note = '#35394F' if dark else '#E4EDF9'
        def svg(h,body,title):
            return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{h}" viewBox="0 0 1200 {h}" role="img" aria-label="{title}"><title>{title}</title><defs><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{line}" stroke-width=".7"/></pattern></defs>{body}</svg>'
        hero = f'''<rect x="2" y="2" width="1196" height="456" rx="28" fill="{paper}" stroke="{line}" stroke-width="3"/>
<rect x="3" y="3" width="1194" height="454" rx="27" fill="url(#grid)"/>
<path d="M48 0V460" stroke="{purple}" opacity=".3" stroke-width="2"/>
<g fill="{ink}" font-family="Arial, sans-serif">
<g transform="rotate(-3 185 92)"><rect x="78" y=" sixty" width="235" height="48" rx="8" fill="{note}"/><text x="96" y="92" font-size="16" font-weight="700" letter-spacing="2">HELLO, I'M THEATER</text></g>
<text x="76" y="208" font-size="68" font-weight="800" letter-spacing="-3">Theater-ahyeon</text>
<path d="M80 228 Q265 239 489 226" stroke="{purple}" stroke-width="7" stroke-linecap="round" fill="none" opacity=".7"/>
<text x="80" y="276" font-size="24" fill="{blue}">code, notes, and side projects.</text>
<rect x="80" y="320" width="92" height="35" rx="17" fill="{note}"/><text x="101" y="343" font-size="15">BUPT</text>
<rect x="184" y="320" width="118" height="35" rx="17" fill="{note}"/><text x="202" y="343" font-size="15">curiosity</text>
<rect x="314" y="320" width="110" height="35" rx="17" fill="{note}"/><text x="337" y="343" font-size="15">music ♫</text>
<text x="80" y="412" font-size="13" letter-spacing="2" opacity=".65">LITTLE NOTES. LITTLE STEPS.</text></g>
<ellipse cx="929" cy="405" rx="176" ry="19" fill="{purple}" opacity=".15"/>
<image x="715" y="26" width="435" height="410" href="{sticker}"/>
<path d="M655 115l8 13 15 2-11 11 2 15-14-7-14 7 2-15-11-11 15-2z" fill="{purple}" opacity=".6"/>
<path d="M1118 85q26-20 31 8q-5 18-29 29q-23-26-2-37" fill="{blue}" opacity=".65"/>'''.replace('y=" sixty"','y="60"')
        (ASSETS/f'hero-{theme}.svg').write_text(svg(460,hero,'Theater-ahyeon — a little notebook with Phoebe'),encoding='utf-8')
        divider=f'<path d="M32 25H545 M655 25H1168" fill="none" stroke="{line}" stroke-width="2" stroke-dasharray="5 9" stroke-linecap="round"/><g transform="rotate(-5 600 25)"><rect x="563" y="11" width="74" height="28" rx="5" fill="{note}"/><path d="M585 25h30 M600 18v14" stroke="{purple}" stroke-width="3" stroke-linecap="round"/></g>'
        (ASSETS/f'divider-{theme}.svg').write_text(svg(50,divider,'Notebook divider'),encoding='utf-8')
        footer=f'''<rect x="2" y="16" width="1196" height="164" rx="22" fill="{paper}" stroke="{line}" stroke-width="2"/>
<path d="M30 144H1170" stroke="{line}" stroke-dasharray="5 8" stroke-width="2"/>
<rect x="86" y="6" width="120" height="30" rx="3" fill="{blue}" opacity=".5" transform="rotate(-6 146 21)"/>
<rect x="994" y="6" width="120" height="30" rx="3" fill="{purple}" opacity=".5" transform="rotate(5 1054 21)"/>
<g font-family="Arial,sans-serif" text-anchor="middle" fill="{ink}"><text x="600" y="89" font-size="30" font-weight="700">thanks for stopping by!</text><text x="600" y="122" font-size="17" fill="{blue}">see you on the next page.</text></g>
<path d="M126 83q-25-23-38 0q-4 15 37 38q40-28 31-42q-10-17-30 4" fill="{purple}" opacity=".65"/>
<path d="M1050 70l8 19 21 2-16 14 5 21-18-11-19 11 5-21-16-14 21-2z" fill="{blue}" opacity=".7"/>'''
        (ASSETS/f'footer-{theme}.svg').write_text(svg(192,footer,'Thanks for stopping by! See you on the next page.'),encoding='utf-8')

if __name__ == '__main__':
    build()
