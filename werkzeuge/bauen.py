# Baut aus der Arbeitsdatei die fertige index.html und den Kopf-Schnipsel für die Passwort-Seite.
# Aufruf: python3 bauen.py <arbeitsdatei.html> <ziel/index.html> [Basis-URL]
# Steht in der Datei "var ENTWURF = true;", bekommt die Seite den Hinweis "noindex" für Suchmaschinen.
import re, sys, os, urllib.parse
src = open(sys.argv[1], encoding='utf-8').read()
basis = sys.argv[3] if len(sys.argv) > 3 else 'https://website-dance.netlify.app'
here = os.path.dirname(os.path.abspath(sys.argv[2]))
i = src.index('<style>'); head_part, rest = src[:i], src[i:]
j = rest.index('</style>') + len('</style>'); style_block, body_part = rest[:j], rest[j:]
title = re.search(r'<title>(.*?)</title>', head_part).group(1)
entwurf = 'var ENTWURF = true;' in src
favicon = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'favicon.svg'), encoding='utf-8').read().strip()
favicon_uri = 'data:image/svg+xml,' + urllib.parse.quote(favicon, safe="/:=,' ")
beschreibung = 'Anouk: Tanz, Ausdruck, Kreativität und Freude an der Arbeit mit Menschen. Persönliche Visitenkarte mit Version in Leichter Sprache.'
kopf = f'''<meta name="description" content="{beschreibung}">
{'<meta name="robots" content="noindex, nofollow">' if entwurf else ''}
<meta name="theme-color" content="#140f1e">
<link rel="icon" href="{favicon_uri}">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{beschreibung}">
<meta property="og:url" content="{basis}/">
<meta property="og:image" content="{basis}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Anouk, Dance &amp; Creative Arts, auf einer Bühne mit rotem Vorhang">
<meta name="twitter:card" content="summary_large_image">'''
html = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
{kopf}
<style>
:root {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }}
body {{ margin: 0; }}
img {{ max-width: 100%; }}
[hidden] {{ display: none !important; }}
</style>
{style_block}
</head>
<body>
{body_part.strip()}
</body>
</html>
'''
open(sys.argv[2], 'w', encoding='utf-8').write(html)
open(os.path.join(here, 'kopf.html'), 'w', encoding='utf-8').write(kopf)
print('geschrieben:', sys.argv[2], '| Entwurfsmodus:', entwurf, '| Basis-URL:', basis)
