"""Validate generated SVGs before publishing."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def check():
    files = [ROOT/'assets'/f'{kind}-{theme}.svg' for kind in ('hero','divider','footer') for theme in ('dark','light')]
    files += [ROOT/'dist'/f'{kind}-{theme}.svg' for kind in ('stats','streak','snake') for theme in ('dark','light')]
    for file in files:
        assert file.exists() and file.stat().st_size > 100, f'Missing/empty: {file}'
        root = ET.parse(file).getroot()
        assert root.tag == '{http://www.w3.org/2000/svg}svg', f'Not SVG: {file}'
        for element in root.iter():
            assert not element.tag.endswith('script'), f'Script in {file}'
            for key, value in element.attrib.items():
                if key.endswith('href'):
                    assert value.startswith(('data:image/', '#')), f'External asset in {file}'
        print(f'OK {file.relative_to(ROOT)} ({file.stat().st_size:,} bytes)')


if __name__ == '__main__':
    check()
