# Bettet ein Foto in eine Arbeitsdatei ein, damit es mit der Seite zusammen verschlüsselt wird.
# Lose Bilddateien im öffentlichen Repository wären für jeden sichtbar, auch ohne Passwort.
#
# Aufruf: python3 werkzeuge/foto-einbetten.py <arbeitsdatei.html> <name> <foto.jpg>
# Beispiel: python3 werkzeuge/foto-einbetten.py arbeit/entwurf4.html start fotos/start.jpg
#
# <name> ist der Wert von data-foto="..." an der Stelle der Seite, wo das Foto erscheinen soll
# (zum Beispiel data-foto="start" für das große Startfoto). Fehlt der Vorrat in der Datei, wird er angelegt.
# Entfernen: python3 werkzeuge/foto-einbetten.py arbeit/entwurf4.html start --weg
import sys, re, base64, mimetypes, os

if len(sys.argv) != 4:
    print(__doc__ or "Aufruf: python3 foto-einbetten.py <arbeitsdatei.html> <name> <foto.jpg | --weg>"); sys.exit(1)
seite, name, foto = sys.argv[1:4]
html = open(seite, encoding="utf-8").read()

if foto == "--weg":
    daten = ""
else:
    typ = mimetypes.guess_type(foto)[0] or "image/jpeg"
    daten = "data:" + typ + ";base64," + base64.b64encode(open(foto, "rb").read()).decode("ascii")
    groesse = os.path.getsize(foto)
    if groesse > 400_000:
        print("Hinweis: Das Foto ist %d KB groß. Besser vorher auf ca. 1400 px Breite verkleinern und als JPEG (Qualität 75–80) speichern." % (groesse // 1024))

muster = re.compile(r'(<script type="text/plain" data-foto="%s">)(.*?)(</script>)' % re.escape(name), re.S)
if muster.search(html):
    html = muster.sub(lambda m: m.group(1) + daten + m.group(3), html, count=1)
    print("Foto-Vorrat", repr(name), "ersetzt" if daten else "geleert")
else:
    if not daten:
        print("Kein Vorrat", repr(name), "in", seite); sys.exit(1)
    block = '<script type="text/plain" data-foto="%s">%s</script>\n' % (name, daten)
    marke = "<!-- FOTO-VORRAT -->"
    if marke in html:
        html = html.replace(marke, marke + "\n" + block, 1)
    else:
        html = html.replace("</body>", block + "</body>", 1)
    print("Foto-Vorrat", repr(name), "angelegt")

open(seite, "w", encoding="utf-8").write(html)
print("geschrieben:", seite, "(%d KB)" % (len(html.encode("utf-8")) // 1024))
