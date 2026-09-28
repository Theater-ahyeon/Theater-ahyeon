"""Render public GitHub stats and verified merged upstream PRs using authenticated gh."""
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


def merged_prs():
    query = """query($login:String!, $cursor:String) {
      user(login:$login) { pullRequests(first:100, after:$cursor, states:MERGED,
        orderBy:{field:UPDATED_AT,direction:DESC}) {
        pageInfo { hasNextPage endCursor }
        nodes { number title url mergedAt repository {
          nameWithOwner isPrivate isFork owner { login }
        } }
      } }
    }"""
    prs, cursor = [], None
    while True:
        args = ['graphql', '-f', f'query={query}', '-f', f'login={LOGIN}']
        if cursor:
            args += ['-f', f'cursor={cursor}']
        result = api(*args)
        if result.get('errors') or not result.get('data', {}).get('user'):
            raise RuntimeError('GitHub did not return merged pull requests')
        page = result['data']['user']['pullRequests']
        for pr in page['nodes']:
            repo = pr['repository']
            if pr['mergedAt'] and not repo['isPrivate'] and not repo['isFork'] and repo['owner']['login'].lower() != LOGIN.lower():
                prs.append(pr)
        if not page['pageInfo']['hasNextPage']:
            return sorted(prs, key=lambda pr: pr['mergedAt'], reverse=True)
        next_cursor = page['pageInfo']['endCursor']
        if not next_cursor or next_cursor == cursor:
            raise RuntimeError('Invalid GitHub pagination cursor')
        cursor = next_cursor


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
    prs = merged_prs()
    projects = {}
    for pr in prs:
        name = pr['repository']['nameWithOwner']
        projects[name] = projects.get(name, 0) + 1
    return dict(login=LOGIN, generated_at=datetime.now(timezone.utc).isoformat(),
                repositories=len(repos), stars=sum(repo['stargazers_count'] for repo in repos),
                contributions=calendar['totalContributions'], merged_prs=prs, projects=projects)


def shell(theme, title, subtitle, body):
    dark = theme.endswith('dark')
    bg, fg, accent, muted, edge = ('#242636', '#F7F0DC', '#C6B4EF', '#BCC7DF', '#44485E') if dark else ('#FFF9EC', '#353347', '#7960A0', '#59657B', '#E3DFD4')
    if theme.startswith('sea-glow'):
        bg, fg, accent, muted, edge = ('#142235','#F0F2F3','#D4BF97','#A9BCCB','#36495C') if dark else ('#F4F6F7','#22394B','#836C42','#607381','#D4DDE2')
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="580" height="250" viewBox="0 0 580 250" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><rect x="1" y="1" width="578" height="248" rx="8" fill="{bg}" stroke="{edge}"/><path d="M28 82H552" stroke="{edge}"/><style>text{{font-family:Georgia,serif;fill:{fg}}}.muted{{fill:{muted};font-family:Arial,sans-serif}}.value{{fill:{accent};font-family:Arial,sans-serif;font-weight:600}}</style><text x="28" y="42" font-size="23">{escape(title)}</text><text x="28" y="66" class="muted" font-size="12">{escape(subtitle)}</text>{body}</svg>'''
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
    for theme in ('dark', 'light', 'sea-glow-dark', 'sea-glow-light'):
        rows = [('Public original repos', data['repositories']), ('Stars on these repos', data['stars']), ('Contributions · past year', data['contributions'])]
        body = ''.join(f'<text x="30" y="{112+i*40}" class="muted" font-size="16">{label}</text><text x="546" y="{114+i*40}" text-anchor="end" class="value" font-size="24">{value:,}</text>' for i, (label, value) in enumerate(rows))
        body += f'<text x="30" y="232" class="muted" font-size="10">Updated {data["generated_at"][:10]} · GitHub public data</text>'
        (OUT / f'stats-{theme}.svg').write_text(shell(theme, 'GitHub Stats', LOGIN, body), encoding='utf-8')
        prs, projects = data['merged_prs'], data['projects']
        body = ''
        for x, label, value in [(154,'Merged PRs',len(prs)),(426,'Projects',len(projects))]:
            body += f'<text x="{x}" y="145" text-anchor="middle" class="value" font-size="42">{value:,}</text><text x="{x}" y="179" text-anchor="middle" class="muted" font-size="16">{label}</text>'
        body += '<text x="290" y="220" text-anchor="middle" class="muted" font-size="12">Public upstream repositories · all time</text>'
        (OUT / f'collaboration-{theme}.svg').write_text(shell(theme, 'Open-source collaboration', 'Small patches. Shared progress.', body), encoding='utf-8')
        render_projects(data, theme)
    (OUT / 'data.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def render_projects(data, theme):
    projects = sorted(data['projects'].items(), key=lambda item: (item[0] != 'bytedance/deer-flow', -item[1], item[0]))
    dark = theme.endswith('dark')
    bg, fg, accent, muted, edge = ('#242636', '#F7F0DC', '#C6B4EF', '#BCC7DF', '#44485E') if dark else ('#FFF9EC', '#353347', '#7960A0', '#59657B', '#E3DFD4')
    if theme.startswith('sea-glow'):
        bg, fg, accent, muted, edge = ('#142235','#F0F2F3','#D4BF97','#A9BCCB','#36495C') if dark else ('#F4F6F7','#22394B','#836C42','#607381','#D4DDE2')
    h = 136 + 48 * max(1,len(projects))
    body = f'<rect x="2" y="2" width="1156" height="{h-4}" rx="24" fill="{bg}" stroke="{edge}" stroke-width="2"/><g font-family="Arial,sans-serif"><text x="32" y="44" font-size="25" font-weight="700" fill="{fg}">Merged contributions</text><text x="32" y="74" font-size="15" fill="{muted}">PRs authored by {escape(LOGIN)} · own repositories and forks excluded</text>'
    for i,(name,count) in enumerate(projects):
        y=113+i*48
        latest=next(pr for pr in data['merged_prs'] if pr['repository']['nameWithOwner']==name)
        body += f'<path d="M32 {y+20}H1128" stroke="{edge}" stroke-dasharray="4 7"/><circle cx="40" cy="{y-5}" r="5" fill="{accent}"/><text x="58" y="{y}" font-size="20" fill="{fg}">{escape(name)}</text><text x="820" y="{y}" text-anchor="end" font-size="16" fill="{muted}">latest: #{latest["number"]} · {latest["mergedAt"][:10]}</text><text x="1126" y="{y}" text-anchor="end" font-size="21" font-weight="700" fill="{accent}">{count} merged</text>'
    if not projects:
        body += f'<text x="32" y="118" font-size="20" fill="{muted}">No merged upstream pull requests yet.</text>'
    body += f'<text x="32" y="{h-22}" font-size="13" fill="{muted}">Updated {data["generated_at"][:10]} · verified mergedAt · click to explore PRs</text></g>'
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1160" height="{h}" viewBox="0 0 1160 {h}" role="img" aria-label="Merged contributions by project"><title>Merged contributions by project</title>{body}</svg>'
    (OUT/f'projects-{theme}.svg').write_text(svg,encoding='utf-8')


if __name__ == '__main__':
    render(fetch())
