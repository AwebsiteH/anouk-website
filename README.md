# Anouk · Dance & Creative Arts

Persönliche Visitenkarten-Website (Entwurf). Online unter:
https://awebsiteh.github.io/anouk-website/

## Was liegt hier?

| Datei / Ordner | Zweck |
| --- | --- |
| `index.html` | Die veröffentlichte Seite, passwortgeschützt (verschlüsselt). Enthält beide Sprachen und die Versionen in Leichter Sprache. |
| `fonts/` | Lokal gespeicherte Schriften (SIL Open Font License), damit keine Daten an Google gehen. |
| `og.png`, `apple-touch-icon.png` | Vorschaubild für Messenger und Icon für Smartphones. |
| `werkzeuge/` | Skripte zum Bauen, Übersetzen und Verschlüsseln der Seite. |
| `.nojekyll` | Sagt GitHub Pages, die Dateien unverändert auszuliefern. |

Die unverschlüsselte Arbeitsdatei liegt **nicht** in diesem öffentlichen Repository, sonst wäre der Passwortschutz wirkungslos.

## Neue Version veröffentlichen

1. Arbeitsdatei bearbeiten (lokal).
2. `python3 werkzeuge/bauen.py arbeitsdatei.html index.html "https://awebsiteh.github.io/anouk-website"`
3. `node werkzeuge/schuetzen.js index.html geschuetzt/index.html "<Passwort>"`
4. Die Datei `geschuetzt/index.html` als `index.html` in dieses Repository übernehmen und einen Commit machen.
5. GitHub Pages veröffentlicht automatisch innerhalb weniger Minuten.

## Später ohne Passwort

In der Arbeitsdatei `var ENTWURF = true;` auf `false` setzen, mit `bauen.py` bauen und die **unverschlüsselte** `index.html` ins Repository übernehmen. Der Suchmaschinen-Hinweis „noindex“ verschwindet dann automatisch.
