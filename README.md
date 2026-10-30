# Anouk · Dance & Creative Arts

Persönliche Visitenkarten-Website (Entwurf). Online unter:
https://awebsiteh.github.io/anouk-website/

## Was liegt hier?

| Datei / Ordner | Zweck |
| --- | --- |
| `index.html` | Die Startseite, passwortgeschützt (verschlüsselt). Nach dem Passwort erscheint das Auswahlmenü mit den vier Entwürfen. |
| `entwurf_original.html` | Das Theater-Konzept (bisherige Seite). Enthält beide Sprachen und die Versionen in Leichter Sprache. |
| `entwurf1.html` | Entwurf 1 „Fluid Motion“: bewegte Farbe, atmende Schrift, keine Boxen. |
| `entwurf2.html` | Entwurf 2 „The Split“: zwei Bühnen (Tanz / Mensch), Naht zum Verschieben, auf dem Smartphone Wischen. |
| `entwurf3.html` | Entwurf 3 „Editorial“: Skizzenbuch trifft Modemagazin, Off-White, Tiefschwarz, ein Neon. |
| `fonts/` | Lokal gespeicherte Schriften (SIL Open Font License), damit keine Daten an Google gehen. |
| `og.png`, `apple-touch-icon.png` | Vorschaubild für Messenger und Icon für Smartphones. |
| `werkzeuge/` | Skripte zum Bauen, Übersetzen und Verschlüsseln der Seiten. |
| `.nojekyll` | Sagt GitHub Pages, die Dateien unverändert auszuliefern. |

Alle Seiten sind verschlüsselt und teilen sich einen Schlüssel: Das Passwort wird einmal auf der Startseite eingegeben, danach öffnen sich Menü und Entwürfe in derselben Browser-Sitzung von allein.

Die unverschlüsselten Arbeitsdateien liegen **nicht** in diesem öffentlichen Repository, sonst wäre der Passwortschutz wirkungslos.

## Neue Version veröffentlichen

1. Arbeitsdateien bearbeiten (lokal, z. B. in einem Ordner `arbeit/`).
2. Nur für das Theater-Konzept: `python3 werkzeuge/bauen.py arbeitsdatei.html arbeit/entwurf_original.html "https://awebsiteh.github.io/anouk-website"`
3. Alle Seiten gemeinsam schützen, damit sie denselben Schlüssel haben:
   `node werkzeuge/schuetzen-alle.js geschuetzt "<Passwort>" arbeit/index.html arbeit/entwurf1.html arbeit/entwurf2.html arbeit/entwurf3.html arbeit/entwurf_original.html`
4. Den Inhalt von `geschuetzt/` in dieses Repository übernehmen und einen Commit machen.
5. GitHub Pages veröffentlicht automatisch innerhalb weniger Minuten.

`werkzeuge/schuetzen.js` schützt wie bisher eine einzelne Seite; sie bekommt dann aber einen eigenen Schlüssel und fragt das Passwort erneut ab.

## Später ohne Passwort

In der Arbeitsdatei `var ENTWURF = true;` auf `false` setzen, mit `bauen.py` bauen und die **unverschlüsselte** Seite ins Repository übernehmen. Der Suchmaschinen-Hinweis „noindex“ verschwindet dann automatisch.
