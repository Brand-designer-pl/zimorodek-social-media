# Zimorodek — social media (Facebook)

Grafiki na Facebooka w kierunku wizualnym landingu `../hero-aplikacje` (Manrope + Italiana, granat #004978, niebieski #0080D1, akcent #E07C00, jasna woda, mleczne szkło, soczyste zdjęcia zimorodka). Pracuj po polsku.

## Pliki
- `tlo-facebook.html` → `eksport/tlo-facebook.png` (1640×624). Kadr = ostatnia klatka filmu z landingu (`assets/kadr-hero.png`), napis „ZIMORODEK” za ptakiem przez `assets/maska-napisu.png` (ten sam rozmiar i pozycja co kadr). Napis i hasło mieszczą się w środkowych ~1110 px widocznych na telefonie.
- `szablony.html` — 8 szablonów postów 1080×1350 (4:5): 1 funkcja, 2 ekran aplikacji, 3 liczba, 4 hasło (jezioro + jasna nakładka), 5 lista (bez tła — decyzja użytkownika), 6 komunikat, 7 ptak na pół (kadr z landingu, napis za ptakiem przez maskę `data-mask`), 8 aplikacja ogólna (styl jak Longwave: logo, hasło, telefon, kafle zalet). Teksty edytuj w HTML; podgląd wszystkich: `szablony.html`, jeden: `szablony.html?p=3`. Logo wbudowane jako `<symbol id="logo">`.
- Blok `OBRAZY` na końcu `szablony.html` generuje `eksport.py` (lekkie kopie 900 px jako data URI), żeby podgląd bez dostępu do `assets/` (panel aplikacji) pokazywał zdjęcia; eksport (`?export`) używa oryginałów. Panel nie otwiera plików ~1,7 MB — nie wbudowuj pełnych rozdzielczości.
- `eksport.py` — eksport PNG przez headless Chrome (render 2×): `python3 eksport.py` / `python3 eksport.py tlo 3`. Nadpisuje pliki w `eksport/`.
- `assets/` — kopie z landingu i prezentacji; `foto-*.jpg` = ujęcia Magnific Seedream 5 Pro z `../prezentacja-konferencja/ujecia-magnific/`.

## Zasady
- Treści tylko z potwierdzonych materiałów (prezentacja, landing). Nie wymyślaj liczb, opinii ani ekranów aplikacji; komunikat w szablonie 6 jest podpisany jako przykład. Ekran batymetrii to prawdziwy zrzut (jezioro Dadaj); `assets/ekran-szukaj.webp` (wyszukiwarka akwenów, szablon 8) — prawdziwy zrzut od użytkownika 2026-10-20.
- Jeden aktualny plik na grafikę, eksporty pod stałymi nazwami — nadpisuj, bez wersji v2/final. Nie publikuj na Facebooku bez polecenia.
