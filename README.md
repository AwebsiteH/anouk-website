# Anouk · Dance & Creative Arts

Persönliche Visitenkarten-Website (Entwurf). Online unter:
https://awebsiteh.github.io/anouk-website/

## Was liegt hier?

| Datei / Ordner | Zweck |
| --- | --- |
| `index.html` | Die Startseite, passwortgeschützt (verschlüsselt). Nach dem Passwort erscheint das Auswahlmenü mit den vier Entwürfen. |
| `entwurf4.html` | **Aktueller Stand**: Überarbeitung nach Anouks Feedback. Blaues Design als Basis, Zweiteilung, ein Neon-Akzent, korrigierte Inhalte. Offene Punkte sind auf der Seite markiert. |
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

## Fotos

Fotos werden **nicht** als lose Dateien abgelegt: Eine Datei wie `fotos/start.jpg` im Repository könnte jeder aufrufen, auch ohne Passwort. Stattdessen werden Fotos in die Arbeitsdatei eingebettet und so mit der Seite zusammen verschlüsselt:

1. Foto vorbereiten: auf ca. 1400 px Breite verkleinern, als JPEG mit Qualität 75–80 speichern (unter 300 KB).
2. Einbetten: `python3 werkzeuge/foto-einbetten.py arbeit/entwurf4.html start fotos/start.jpg`
   Der Name (`start`) bezeichnet die Stelle auf der Seite. In Entwurf 4 gibt es: `start` (großes Startfoto), `portraet`, `tanz1`, `tanz2` (Hochformat 3:4), `tanz3` (Querformat 16:9).
3. Danach die Seite wie unten beschrieben schützen und veröffentlichen.

Entfernen: `python3 werkzeuge/foto-einbetten.py arbeit/entwurf4.html start --weg`

Die derzeit eingebetteten Bilder sind **Beispielfotos**. Sie tragen auf der Seite das Schild „Beispielfoto“, weil an der jeweiligen Fotostelle in der Arbeitsdatei `data-beispiel` steht. Sobald ein echtes Foto eingebettet ist, dieses Wort an der Stelle löschen.

## Neue Version veröffentlichen

1. Arbeitsdateien bearbeiten (lokal, z. B. in einem Ordner `arbeit/`).
2. Nur für das Theater-Konzept: `python3 werkzeuge/bauen.py arbeitsdatei.html arbeit/entwurf_original.html "https://awebsiteh.github.io/anouk-website"`
3. Die geänderten Seiten schützen. Damit sie zum selben Schlüssel wie die bereits veröffentlichten Seiten passen, den Salt einer veröffentlichten Seite übernehmen:
   `node werkzeuge/schuetzen-alle.js --wie index.html geschuetzt "<Passwort>" arbeit/entwurf4.html`
   (Ohne `--wie` bekommen die Seiten einen neuen gemeinsamen Schlüssel; dann müssen **alle** Seiten in einem Durchlauf geschützt werden.)
4. Den Inhalt von `geschuetzt/` in dieses Repository übernehmen und einen Commit machen.
5. GitHub Pages veröffentlicht automatisch innerhalb weniger Minuten.

`werkzeuge/schuetzen.js` schützt wie bisher eine einzelne Seite; sie bekommt dann aber einen eigenen Schlüssel und fragt das Passwort erneut ab.

## Später ohne Passwort

In der Arbeitsdatei `var ENTWURF = true;` auf `false` setzen, mit `bauen.py` bauen und die **unverschlüsselte** Seite ins Repository übernehmen. Der Suchmaschinen-Hinweis „noindex“ verschwindet dann automatisch.
