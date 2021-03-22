# Minimalista szokás követő webalkalmazás
## TODO
| Feladat | Teljesítve |
| --- | --- |
| Regisztráció implementálása | x |
| Bejelentkeztetés implementálása | x |
| Szokások listázása, naptár | X |
| Szokás hozzáadása | x |
| Szokás szerkesztése | x |
| Szokás törlése | x |
| Színek implementálása | x |
| Nav-bar makró nélkül | x |
| Frekvencia detektálás | x |
| Dinamikusan megjelenített naptárak |  |
| Prediktív tervezés |  |


## Célkitűzés
A minimalizmus, mint szoftverfejlesztési szemlélet alkalmazása. Kevés funkció, könnyű kezelés, egyszerű implementáció. A felhasználói felület is ezt tükrözze. A kód legyen tömör, de átlátható. Legyen megjegyzés mindenhol.
## Funkciók
- Fiók kezelés
    1. Regisztráció
    1. Bejelentkezés
    1. Kijelentkezés
- Szokás kezelés
    1. Szokás hozzáadása
    1. Szokás szerkesztése
    1. Szokás törlése
- Szokás nyomonkövetés
    1. Múltbéli dátumok kipipálása
    1. Jövőbeli dátumok megjelölése
    1. Jövőbeli dátumok automatikus megjelölése (prediktív modell)
- Értesítések
    1. Email értesítések
## Megkötések
- Az alkalmazás egyetlen egy oldalból álljon.
- Maximálisan 3 szín alkalmazása.
- A HTML fának legfeljebb 5 szintje legyen.
- A forrás állományok hossza maximálisan 64 sor (html, css, py, js).
- Egy függvény, metódus implementációjának hossza maximálisan 16 sor.
- Egy css szabály maximum 16 sor.
- Egy osztály implementációja maximálisan 32 sor.
- Változónevek, azonosítók max 4 karakteresek függvény implementációkon belül illetver privát attribútumoknál. Ha a rövidítés nem egyértelmű, akkor kommentek használata. Az osztálynevek, modul nevek, publikus attribútumok lehetnek hosszabbak, de max 16 karakter.
- Sorhossz max 64 karakter.
