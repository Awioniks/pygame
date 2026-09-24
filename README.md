# Zombie Killer

Prosta gra survival shooter 2D napisana w Pythonie z użyciem Pygame Zero.
Gracz steruje zombie killerem, strzela do zombie i przechodzi kolejne poziomy.

## Funkcje

- losowe przeszkody generowane na każdym poziomie,
- zombie rozmieszczone w losowych miejscach,
- zombie podążające za graczem, gdy znajdują się w jego zasięgu,
- strzelanie pociskami,
- kolizje gracza, zombie, pocisków i przeszkód,
- odejmowanie życia po kontakcie z zombie przez około sekundę,
- maksymalnie 10 poziomów,
- więcej zombie i przeszkód na każdym kolejnym poziomie,
- menu z przyciskami Start, Music i Exit,
- kierunkowe grafiki gracza,
- muzyka w tle.

## Sterowanie

| Klawisz / działanie | Funkcja |
| --- | --- |
| `W`, `A`, `S`, `D` lub strzałki | Ruch gracza |
| `SPACJA` | Strzał w kierunku ostatniego ruchu |
| `ESC` | Zamknięcie gry |
| Przycisk `START` | Rozpoczęcie lub zresetowanie gry |
| Przycisk `MUSIC` | Włączenie lub wyłączenie muzyki |
| Przycisk `EXIT` | Zamknięcie gry |

## Instalacja

Utwórz środowisko wirtualne:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Zainstaluj zależności:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Uruchomienie

```bash
source .venv/bin/activate
pgzrun main.py
```

Na macOS można dodatkowo wyśrodkować okno gry:

```bash
SDL_VIDEO_CENTERED=1 pgzrun main.py
```

## Struktura projektu

```text
pygame/
├── main.py
├── requirements.txt
├── images/
│   ├── zombie.png
│   ├── zombie_killer.png
│   ├── zombie_killer_left.png
│   ├── zombie_killer_right.png
│   ├── zombie_killer_up.png
│   └── zombie_killer_down.png
└── music/
    └── zombie_music.wav
```

## Technologie

- Python 3.12+
- Pygame Zero 1.2.1