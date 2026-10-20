"""Eksport grafik do PNG przez headless Chrome (render 2×, zapis w rozmiarze docelowym).

  python3 eksport.py            — wszystko
  python3 eksport.py tlo        — tylko tło Facebooka
  python3 eksport.py 3          — tylko szablon nr 3
  python3 eksport.py obrazy     — tylko odśwież obrazy wbudowane w szablony.html

Przed eksportem obrazy z assets/ są wbudowywane w szablony.html (blok OBRAZY na końcu pliku),
żeby plik wyświetlał się w całości także w podglądach bez dostępu do folderu assets/.
"""
import base64, io, mimetypes, os, re, subprocess, sys, tempfile, time
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HERE = os.path.dirname(os.path.abspath(__file__))
SZABLONY = {1: "funkcja", 2: "ekran-aplikacji", 3: "liczba", 4: "haslo", 5: "lista", 6: "komunikat", 7: "ptak-pol", 8: "aplikacja"}


def shot(url, w, h, out):
    tmp = tempfile.mktemp(suffix=".png")
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                          "--allow-file-access-from-files", "--force-device-scale-factor=2",
                          f"--window-size={w},{h}", "--virtual-time-budget=6000",
                          f"--screenshot={tmp}", url],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # headless Chrome potrafi nie zakończyć się po zapisaniu pliku — czekamy na plik i zamykamy proces
    for _ in range(120):
        if os.path.exists(tmp) and os.path.getsize(tmp) > 0:
            time.sleep(0.5)
            break
        time.sleep(0.25)
    p.kill()
    Image.open(tmp).convert("RGB").resize((w, h), Image.LANCZOS).save(out, optimize=True)
    os.remove(tmp)
    print("zapisano", os.path.relpath(out, HERE))


def wbuduj_obrazy():
    path = os.path.join(HERE, "szablony.html")
    html = open(path, encoding="utf-8").read()
    head, rest = html.split("<!-- OBRAZY:START -->", 1)
    _, tail = rest.split("<!-- OBRAZY:END -->", 1)
    data = {}
    for src in sorted(set(re.findall(r'(?:src|data-mask)="(assets/[^"]+)"', head))):
        mime = mimetypes.guess_type(src)[0] or ("image/webp" if src.endswith(".webp") else "application/octet-stream")
        # lekka kopia podglądowa (eksport PNG i tak bierze oryginały z assets/)
        im = Image.open(os.path.join(HERE, src))
        im.thumbnail((900, 900))
        buf = io.BytesIO()
        if im.mode == "RGBA":
            im.save(buf, "WEBP", quality=70); mime = "image/webp"
        else:
            im.convert("RGB").save(buf, "JPEG", quality=68); mime = "image/jpeg"
        data[src] = f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()
    entries = ",\n".join(f'"{k}":"{v}"' for k, v in data.items())
    block = ("<!-- OBRAZY:START -->\n<!-- wygenerowane przez eksport.py — nie edytuj; obrazy podmieniaj w assets/ -->\n"
             "<script>(function(){const IMG={\n" + entries + "\n};"
             "if(!/export/.test(location.search))document.querySelectorAll('img[src^=\"assets/\"]').forEach(i=>{const d=IMG[i.getAttribute('src')];if(d)i.src=d;});document.querySelectorAll('[data-mask]').forEach(m=>{const k=m.dataset.mask,u=(IMG[k]&&!/export/.test(location.search))?IMG[k]:k;m.style.webkitMaskImage=m.style.maskImage='url('+u+')';});})();</script>\n"
             "<!-- OBRAZY:END -->")
    open(path, "w", encoding="utf-8").write(head + block + tail)
    print(f"wbudowano {len(data)} obrazów, szablony.html = {os.path.getsize(path)/1e6:.1f} MB")


def main(args):
    wbuduj_obrazy()
    if args == ["obrazy"]:
        return
    os.makedirs(os.path.join(HERE, "eksport"), exist_ok=True)
    base = "file://" + HERE
    if not args or "tlo" in args:
        shot(f"{base}/tlo-facebook.html", 1640, 624, os.path.join(HERE, "eksport", "tlo-facebook.png"))
    for n, name in SZABLONY.items():
        if not args or str(n) in args:
            shot(f"{base}/szablony.html?p={n}&export", 1080, 1350,
                 os.path.join(HERE, "eksport", f"post-{n}-{name}.png"))


if __name__ == "__main__":
    main(sys.argv[1:])
