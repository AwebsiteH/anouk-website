// Verschlüsselt mehrere HTML-Seiten mit EINEM Passwort und EINEM gemeinsamen Salt (AES-256-GCM, Schlüssel per PBKDF2).
// Weil alle Seiten denselben Schlüssel benutzen, muss das Passwort nur einmal eingegeben werden:
// die Passwort-Seite merkt sich den Schlüssel für die Browser-Sitzung und öffnet die anderen Seiten von allein.
//
// Aufruf: node werkzeuge/schuetzen-alle.js <zielordner> "<Passwort>" <seite1.html> [<seite2.html> ...]
// Beispiel: node werkzeuge/schuetzen-alle.js geschuetzt "GeheimesWort" arbeit/index.html arbeit/entwurf1.html arbeit/entwurf2.html
// Jede Seite landet unter ihrem eigenen Dateinamen im Zielordner. kopf.html und fonts/fonts.css werden,
// falls vorhanden, aus dem Ordner der ersten Quelldatei übernommen (wie bei schuetzen.js).
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const [, , destDir, password, ...sources] = process.argv;
if (!destDir || !password || sources.length === 0) {
  console.error('Aufruf: node schuetzen-alle.js <zielordner> "<Passwort>" <seite1.html> [<seite2.html> ...]');
  process.exit(1);
}
fs.mkdirSync(destDir, { recursive: true });

const ITERATIONS = 600000;
const baseDir = path.dirname(sources[0]);
const fontsCss = fs.existsSync(path.join(baseDir, "fonts", "fonts.css")) ? fs.readFileSync(path.join(baseDir, "fonts", "fonts.css"), "utf8") : "";
const kopf = fs.existsSync(path.join(baseDir, "kopf.html")) ? fs.readFileSync(path.join(baseDir, "kopf.html"), "utf8").replace(/<meta name="robots"[^>]*>/, "") : "";

// Ein Salt und damit ein Schlüssel für alle Seiten dieses Durchlaufs.
const salt = crypto.randomBytes(16);
const key = crypto.pbkdf2Sync(password, salt, ITERATIONS, 32, "sha256");

function gate(payload) {
  return `<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Anouk | Zugang</title>
${kopf}
<style>
${fontsCss}
:root { --bg: #1b1630; --surface: #26203f; --ink: #f2f0f8; --muted: #b3acc6; --line: #3d3658; --spot: #ffd23f; --red: #ff8a78; --ok: #5fd6c4; color-scheme: dark; }
*, *::before, *::after { box-sizing: border-box; }
html, body { height: 100%; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: "Atkinson Hyperlegible", system-ui, sans-serif; font-size: 1.1rem; line-height: 1.6; display: grid; place-items: center; padding: 1.5rem max(16px, env(safe-area-inset-right, 0px)) 1.5rem max(16px, env(safe-area-inset-left, 0px)); }
.gate { width: 100%; max-width: 26rem; display: flex; flex-direction: column; gap: 1.25rem; }
.kicker { font-family: "Unbounded", sans-serif; font-weight: 600; font-size: .78rem; letter-spacing: .16em; text-transform: uppercase; color: var(--red); margin: 0; }
h1 { font-family: "Unbounded", sans-serif; font-weight: 800; font-size: clamp(2.6rem, 12vw, 4rem); line-height: 1; letter-spacing: -.03em; margin: 0; }
h1 span { display: inline-block; padding: .18em .3em .22em; background: var(--spot); color: #1b1630; border-radius: 999px; }
p { margin: 0; }
.muted { color: var(--muted); }
form { display: flex; flex-direction: column; gap: .75rem; background: var(--surface); border: 1px solid var(--line); border-radius: 18px; padding: 1.25rem; }
label { font-weight: 700; }
input { font: inherit; font-size: 1.15rem; padding: .85rem 1rem; border-radius: 12px; border: 2px solid var(--line); background: var(--bg); color: var(--ink); width: 100%; min-height: 52px; }
input:focus-visible { outline: 3px solid var(--spot); outline-offset: 2px; }
button { font-family: "Unbounded", sans-serif; font-weight: 600; font-size: .9rem; min-height: 52px; padding: .8rem 1.2rem; border-radius: 999px; border: 0; background: var(--spot); color: #1b1630; cursor: pointer; }
button:focus-visible { outline: 3px solid var(--ink); outline-offset: 3px; }
button[disabled] { opacity: .6; cursor: wait; }
.status { min-height: 1.5em; font-weight: 700; color: var(--red); }
.status.ok { color: var(--ok); }
.fine { font-size: .9rem; }
body.opening .gate { visibility: hidden; }
</style>
</head>
<body>
<main class="gate">
  <p class="kicker">Dance &amp; Creative Arts</p>
  <h1><span>Anouk</span></h1>
  <p>Diese Seite ist geschützt.<br>Bitte geben Sie das Passwort ein.</p>
  <p class="muted fine" lang="en">This page is password-protected. Please enter the password.</p>
  <form id="form" autocomplete="off">
    <label for="pw">Passwort</label>
    <input id="pw" type="password" autocomplete="current-password" autofocus required>
    <button type="submit" id="go">Seite öffnen · Open page</button>
    <p class="status" id="status" aria-live="polite"></p>
  </form>
  <p class="muted fine">Sie haben kein Passwort? Dann fragen Sie bitte die Person, von der Sie den Link bekommen haben.<br><span lang="en">No password? Please ask the person who sent you the link.</span></p>
</main>
<script id="payload" type="application/json">${JSON.stringify(payload)}</script>
<script>
(function () {
  var payload = JSON.parse(document.getElementById("payload").textContent);
  var form = document.getElementById("form"), pw = document.getElementById("pw"), go = document.getElementById("go"), status = document.getElementById("status");
  function b64(s) { var bin = atob(s), arr = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i); return arr; }
  function toB64(buf) { var bin = "", arr = new Uint8Array(buf); for (var i = 0; i < arr.length; i++) bin += String.fromCharCode(arr[i]); return btoa(bin); }
  if (!window.crypto || !crypto.subtle) { status.textContent = "Ihr Browser unterstützt diese Seite nicht. Bitte einen aktuellen Browser verwenden."; go.disabled = true; return; }

  function deriveKey(password) {
    var enc = new TextEncoder();
    return crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveKey"]).then(function (base) {
      return crypto.subtle.deriveKey({ name: "PBKDF2", salt: b64(payload.salt), iterations: payload.iterations, hash: "SHA-256" }, base, { name: "AES-GCM", length: 256 }, true, ["decrypt"]);
    });
  }
  function mount(html) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    document.replaceChild(document.adoptNode(doc.documentElement), document.documentElement);
    Array.prototype.slice.call(document.querySelectorAll("script")).forEach(function (old) {
      var s = document.createElement("script");
      Array.prototype.forEach.call(old.attributes, function (a) { s.setAttribute(a.name, a.value); });
      s.textContent = old.textContent;
      old.parentNode.replaceChild(s, old);
    });
    if (location.hash) { var t = document.querySelector(location.hash); if (t && t.scrollIntoView) t.scrollIntoView(); }
  }
  function open(key) {
    return crypto.subtle.decrypt({ name: "AES-GCM", iv: b64(payload.iv) }, key, b64(payload.data)).then(function (buf) {
      var html = new TextDecoder().decode(buf);
      return crypto.subtle.exportKey("raw", key).then(function (raw) { try { sessionStorage.setItem("anouk-key", toB64(raw)); } catch (e) {} }, function () {}).then(function () { mount(html); });
    });
  }
  function whenLoaded(fn) { if (document.readyState === "complete") fn(); else window.addEventListener("load", fn); }
  var saved = null;
  try { saved = sessionStorage.getItem("anouk-key"); } catch (e) {}
  if (saved) {
    // Schlüssel aus dieser Sitzung vorhanden: Seite ohne erneute Eingabe öffnen, Passwortfeld dabei nicht aufblitzen lassen.
    document.body.className = "opening";
    whenLoaded(function () {
      crypto.subtle.importKey("raw", b64(saved), { name: "AES-GCM" }, true, ["decrypt"]).then(open).catch(function () {
        try { sessionStorage.removeItem("anouk-key"); } catch (e) {}
        document.body.className = "";
      });
    });
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    status.className = "status"; status.textContent = "Wird geprüft … · Checking …"; go.disabled = true;
    deriveKey(pw.value).then(function (key) { return new Promise(function (resolve, reject) { whenLoaded(function () { open(key).then(resolve, reject); }); }); }).catch(function () {
      status.textContent = "Das Passwort stimmt nicht. Bitte noch einmal versuchen. · Wrong password, please try again.";
      go.disabled = false; pw.select();
    });
  });
})();
</script>
</body>
</html>
`;
}

sources.forEach(function (src) {
  const html = fs.readFileSync(src, "utf8");
  const iv = crypto.randomBytes(12); // der IV bleibt pro Seite verschieden, nur Salt und Schlüssel sind gemeinsam
  const cipher = crypto.createCipheriv("aes-256-gcm", key, iv);
  const encrypted = Buffer.concat([cipher.update(html, "utf8"), cipher.final(), cipher.getAuthTag()]);
  const payload = { salt: salt.toString("base64"), iv: iv.toString("base64"), iterations: ITERATIONS, data: encrypted.toString("base64") };
  const dest = path.join(destDir, path.basename(src));
  const page = gate(payload);
  fs.writeFileSync(dest, page);
  console.log("Geschützte Seite geschrieben:", dest, "(" + Math.round(page.length / 1024) + " KB)");
});
console.log("Fertig: " + sources.length + " Seiten, ein gemeinsames Passwort.");
