#!/usr/bin/env python3
"""Deploy both Netlify sites via the digest-deploy API (stdlib only).

Usage:  NETLIFY_AUTH_TOKEN=... python3 scripts/deploy.py [mobile|laptop ...]
With no argument, deploys every site. A site whose files already match the
live deploy is skipped. Files served live but not listed below are carried
over unchanged (by sha1), so a deploy never silently drops a live file.
"""
import hashlib, json, os, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = 'https://api.netlify.com/api/v1'

SITES = {
    # wine-app-yd.netlify.app — Cave YD (mobile)
    'mobile': {
        'id': 'bdc28751-6d21-4eda-9493-d61fb9fba445',
        'files': {
            '/index.html': 'App/Cave-YD-mobile.html',
            '/apple-touch-icon.png': 'App/apple-touch-icon.png',
            '/favicon-32.png': 'App/favicon-32.png',
            '/manifest.json': 'App/manifest.json',
        },
    },
    # my-cellar-yd.netlify.app — index.html (laptop)
    'laptop': {
        'id': 'af0c6c49-008c-4578-a41e-c135b25a7c5b',
        'files': {
            '/index.html': 'index.html',
            '/manifest.json': 'manifest.json',
            '/icon.svg': 'icon.svg',
            '/icon-192.png': 'icon-192.png',
            '/icon-512.png': 'icon-512.png',
            '/map-bordeaux.svg': 'map-bordeaux.svg',
            '/map-france.svg': 'map-france.svg',
        },
    },
}


def call(method, path, token, body=None, raw=None):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header('Authorization', 'Bearer ' + token)
    req.add_header('Content-Type', 'application/octet-stream' if raw is not None else 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            txt = r.read()
            return json.loads(txt) if txt else None
    except urllib.error.HTTPError as e:
        sys.exit(f'{method} {path} -> {e.code}: {e.read()[:300].decode(errors="replace")}')


def deploy(name, token):
    site = SITES[name]
    local = {}
    for path, src in site['files'].items():
        with open(os.path.join(ROOT, src), 'rb') as f:
            content = f.read()
        local[path] = (hashlib.sha1(content).hexdigest(), content)

    info = call('GET', f"/sites/{site['id']}", token)
    live = {}
    if info.get('published_deploy'):
        for f in call('GET', f"/deploys/{info['published_deploy']['id']}/files", token):
            live[f['id']] = f['sha']

    digest = {**live, **{p: sha for p, (sha, _) in local.items()}}
    if digest == live:
        print(f'[{name}] up to date, skipping')
        return

    dep = call('POST', f"/sites/{site['id']}/deploys", token, {'files': digest})
    by_sha = {sha: content for sha, content in local.values()}
    for sha in dep.get('required', []):
        path = next(p for p, (s, _) in local.items() if s == sha)
        call('PUT', f"/deploys/{dep['id']}/files{path}", token, raw=by_sha[sha])
        print(f'[{name}] uploaded {path}')

    for _ in range(60):
        state = call('GET', f"/deploys/{dep['id']}", token)['state']
        if state == 'ready':
            break
        if state == 'error':
            sys.exit(f'[{name}] deploy {dep["id"]} failed')
        time.sleep(2)
    else:
        sys.exit(f'[{name}] deploy {dep["id"]} not ready after 2 min')

    call('POST', f"/sites/{site['id']}/deploys/{dep['id']}/restore", token)
    print(f'[{name}] published {dep["id"]} -> {info.get("ssl_url") or info.get("url")}')


if __name__ == '__main__':
    token = os.environ.get('NETLIFY_AUTH_TOKEN')
    if not token:
        sys.exit('NETLIFY_AUTH_TOKEN is not set')
    names = sys.argv[1:] or list(SITES)
    for n in names:
        if n not in SITES:
            sys.exit(f'unknown site {n!r} (choose from {", ".join(SITES)})')
        deploy(n, token)
