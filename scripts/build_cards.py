"""Render public GitHub statistics using authenticated gh; streaks are past-year UTC."""
import json
import os
import subprocess
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
LOGIN = os.environ.get('GH_LOGIN', 'Theater-ahyeon')


def api(*args):
    result = subprocess.run(['gh', 'api', *args], capture_output=True, text=True, encoding='utf-8', check=True)
    return json.loads(result.stdout)


def streaks(days):
    """An unfinished inactive UTC day does not break yesterday's streak."""
    longest = running = 0
    for day in days:
        running = running + 1 if day['contributionCount'] else 0
        longest = max(longest, running)
    tail = list(days)
    today = datetime.now(timezone.utc).date().isoformat()
    if tail and tail[-1]['date'] == today and tail[-1]['contributionCount'] == 0:
        tail.pop()
    current = 0
    for day in reversed(tail):
        if not day['contributionCount']:
            break
        current += 1
    return current, longest


def fetch():
    repos = api(f'users/{LOGIN}/repos?per_page=100&type=owner', '--paginate', '--slurp')
    repos = [repo for page in repos for repo in page if not repo['private'] and not repo['fork']]
    query = '''query($login:String!) { user(login:$login) {
      contributionsCollection { contributionCalendar { totalContributions weeks {
        contributionDays { date contributionCount contributionLevel }
      } } }
    } }'''
    result = api('graphql', '-f', f'query={query}', '-f', f'login={LOGIN}')
    if result.get('errors') or not result.get('data', {}).get('user'):
        raise RuntimeError('GitHub did not return a contribution calendar')
    calendar = result['data']['user']['contributionsCollection']['contributionCalendar']
    days = [day for week in calendar['weeks'] for day in week['contributionDays']]
    current, longest = streaks(days)
    return dict(login=LOGIN, generated_at=datetime.now(timezone.utc).isoformat(),
                repositories=len(repos), stars=sum(repo['stargazers_count'] for repo in repos),
                contributions=calendar['totalContributions'], current=current, longest=longest,
                active_days=sum(day['contributionCount'] > 0 for day in days), weeks=calendar['weeks'])


def shell(theme, title, subtitle, body):
    dark = theme == 'dark'
    bg, fg, accent, muted, edge = ('#242636', '#F7F0DC', '#C6B4EF', '#BCC7DF', '#44485E') if dark else ('#FFF9EC', '#353347', '#7960A0', '#59657B', '#E3DFD4')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="580" height="250" viewBox="0 0 580 250" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>
<rect x="3" y="3" width="574" height="244" rx="22" fill="{bg}" stroke="{edge}" stroke-width="2"/>
<path d="M22 81H558" stroke="{edge}" stroke-width="2" stroke-dasharray="4 6"/>
<path d="M495 0h52v17h-52z" fill="{accent}" opacity=".45" transform="rotate(5 521 8)"/>
<circle cx="30" cy="35" r="6" fill="{accent}"/>
<style>text{{font-family:Arial,sans-serif;fill:{fg}}}.muted{{fill:{muted}}}.value{{fill:{accent};font-weight:700}}</style>
<text x="47" y="43" font-size="22" font-weight="700">{escape(title)}</text>
<text x="28" y="65" class="muted" font-size="12">{escape(subtitle)}</text>{body}</svg>'''


def render(data):
    OUT.mkdir(exist_ok=True)
    for theme in ('dark', 'light'):
        rows = [('Public original repos', data['repositories']), ('Stars on these repos', data['stars']), ('Contributions · past year', data['contributions'])]
        body = ''.join(f'<text x="30" y="{112+i*40}" class="muted" font-size="16">{label}</text><text x="546" y="{114+i*40}" text-anchor="end" class="value" font-size="24">{value:,}</text>' for i, (label, value) in enumerate(rows))
        body += f'<text x="30" y="232" class="muted" font-size="10">Updated {data["generated_at"][:10]} · GitHub public data</text>'
        (OUT / f'stats-{theme}.svg').write_text(shell(theme, 'GitHub Stats', LOGIN, body), encoding='utf-8')
        body = ''
        for x, label, key in [(104,'Current streak','current'),(290,'Longest streak','longest'),(476,'Active days','active_days')]:
            body += f'<text x="{x}" y="142" text-anchor="middle" class="value" font-size="38">{data[key]:,}</text><text x="{x}" y="174" text-anchor="middle" class="muted" font-size="14">{label}</text>'
        body += '<text x="290" y="219" text-anchor="middle" class="muted" font-size="11">Days · past-year calendar · UTC</text>'
        (OUT / f'streak-{theme}.svg').write_text(shell(theme, 'Contribution Streak', 'One little step at a time.', body), encoding='utf-8')
    (OUT / 'data.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    render(fetch())
