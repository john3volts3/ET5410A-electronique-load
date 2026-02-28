**English** | [Francais](#fr)

# ET5410 Web Controller

Web-based controller for the **ET5410 / ET5411 / ET5420** programmable DC electronic load (Hangzhou Zhongchuang Electronics / East Tester). Single HTML file, zero dependencies — just open in Chrome and connect via USB.

## Features

- **12 load modes** — CC, CV, CP, CR, CC+CV, CR+CV, Dynamic, List (50 steps), Scan, Short, Battery, LED
- **Real-time measurements** — Voltage, Current, Power, Resistance with live graph
- **Battery discharge test** — Full test with voltage curve, statistics (min/max/avg), pause/resume, auto-stop on device cutoff, and multiple export formats (TXT, CSV, SVG, PNG, PDF report)
- **MPPT scanning** — Solar panel maximum power point tracking with two modes: linear scan (step-by-step) and dichotomy (ternary search, ~10-15 measurements). Real-time graph with MPP marker, CSV/PNG export.
- **Save/Load configurations** — Export and import settings to `.ET5410` files
- **Qualification testing** — Pass/fail limit checking for V, I, P
- **SCPI terminal** — Direct command console for advanced use
- **System management** — Protections (OV/OC/OP), ranges, device file storage
- **Decimal input** — Both period and comma accepted as decimal separator in all number fields
- **Dark theme** — Designed for lab/bench use

## Supported Hardware

| Model | Voltage | Current | Power |
|-------|---------|---------|-------|
| ET5410 | 150V | 40A | 400W |
| ET5411 | 150V | 15A | 150W |
| ET5420 | 150V | 20A | 200W |

## Quick Start

### Requirements

- **Browser**: Chrome 89+ or Edge 89+ (Web Serial API required)
- **Cable**: USB to the ET5410 device
- **Driver**: USB serial driver (auto-installed on Windows 10/11)

### Usage

1. Open `index.html` in Chrome or Edge (double-click — no server needed)
2. Select the baud rate (default: 14400) and click **Connect**
3. Choose the serial port corresponding to the ET5410
4. The device identifier is displayed (e.g. `East Tester, ET5410A+, ...`)

> The application uses the [Web Serial API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API) and runs entirely in the browser via `file://` — no server, no install, no dependencies.

## Documentation

- **[User Manual](USER_MANUAL.md)** / **[Manuel utilisateur](USER_MANUAL-fr.md)** — Step-by-step usage guide
- **[Technical Documentation](DOCUMENTATION.md)** / **[Documentation technique](DOCUMENTATION-fr.md)** — Architecture, SCPI protocol, JavaScript internals
- **[SCPI Reference](datasheet/ET5410SCPI.txt)** — Complete command reference (corrected and augmented)

## SCPI Protocol

Communication uses SCPI commands over a virtual USB serial port.

| Parameter | Value |
|-----------|-------|
| Baud rates | 7200, 9600, 14400 |
| Data bits | 8 |
| Stop bits | 1 |
| Parity | None |
| Terminator | `0x0A` (LF) |

**Undocumented commands discovered** via brute-force scanning (see `scan_*.py` scripts):

| Command | Description |
|---------|-------------|
| `BATT:BTC` | Battery cutoff capacity (Ah) |
| `BATT:BTE` | Battery cutoff energy (Wh) |
| `TIME:BTT` | Battery cutoff time (seconds) |
| `BATT:ENER?` | Discharged energy readback (Wh) |
| `CURR:BCC` | Battery current for non-voltage cutoff (A) |

## Project Structure

```
index.html                  Single-file web application (HTML + CSS + JS)
DOCUMENTATION.md            Technical documentation (EN)
DOCUMENTATION-fr.md         Documentation technique (FR)
USER_MANUAL.md              User manual (EN)
USER_MANUAL-fr.md           Manuel utilisateur (FR)
datasheet/
  ET5410SCPI.pdf            Manufacturer SCPI documentation (45 pages)
  ET5410SCPI.txt            Corrected and augmented SCPI reference
data/
  *.ET5410                  Sample configuration files
scan_*.py                   SCPI brute-force discovery scripts
```

## License

This project is licensed under the [MIT License](LICENSE).

---

<a id="fr"></a>

[English](#) | **Francais**

# ET5410 Web Controller

Interface web de controle pour la charge electronique programmable DC **ET5410 / ET5411 / ET5420** (Hangzhou Zhongchuang Electronics / East Tester). Fichier HTML unique, zero dependance — ouvrir dans Chrome et connecter via USB.

## Fonctionnalites

- **12 modes de charge** — CC, CV, CP, CR, CC+CV, CR+CV, Dynamique, List (50 etapes), Scan, Short, Battery, LED
- **Mesures temps reel** — Tension, Courant, Puissance, Resistance avec graphique en direct
- **Test de decharge batterie** — Test complet avec courbe de tension, statistiques (min/max/moy), pause/reprise, arret automatique au cutoff, et multiples formats d'export (TXT, CSV, SVG, PNG, rapport PDF)
- **Scan MPPT** — Recherche du point de puissance maximale (panneau solaire) avec deux modes : scan lineaire (pas a pas) et dichotomie (recherche ternaire, ~10-15 mesures). Graphique temps reel avec marqueur MPP, export CSV/PNG.
- **Sauvegarde/Chargement** — Export et import de configurations vers des fichiers `.ET5410`
- **Test de qualification** — Verification pass/fail des limites V, I, P
- **Terminal SCPI** — Console de commandes directe pour utilisation avancee
- **Gestion systeme** — Protections (OV/OC/OP), ranges, stockage fichiers appareil
- **Saisie decimale** — Point et virgule acceptes comme separateur decimal dans tous les champs numeriques
- **Theme sombre** — Concu pour une utilisation en laboratoire/atelier

## Materiel supporte

| Modele | Tension | Courant | Puissance |
|--------|---------|---------|-----------|
| ET5410 | 150V | 40A | 400W |
| ET5411 | 150V | 15A | 150W |
| ET5420 | 150V | 20A | 200W |

## Demarrage rapide

### Pre-requis

- **Navigateur** : Chrome 89+ ou Edge 89+ (Web Serial API requise)
- **Cable** : USB vers l'appareil ET5410
- **Driver** : Driver USB serie (installe automatiquement sous Windows 10/11)

### Utilisation

1. Ouvrir `index.html` dans Chrome ou Edge (double-clic — aucun serveur necessaire)
2. Selectionner le baud rate (defaut : 14400) et cliquer **Connecter**
3. Choisir le port serie correspondant a l'ET5410
4. L'identifiant de l'appareil s'affiche (ex: `East Tester, ET5410A+, ...`)

> L'application utilise la [Web Serial API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API) et fonctionne entierement dans le navigateur via `file://` — pas de serveur, pas d'installation, pas de dependances.

## Documentation

- **[Manuel utilisateur](USER_MANUAL-fr.md)** / **[User Manual](USER_MANUAL.md)** — Guide d'utilisation pas a pas
- **[Documentation technique](DOCUMENTATION-fr.md)** / **[Technical Documentation](DOCUMENTATION.md)** — Architecture, protocole SCPI, composants JavaScript
- **[Reference SCPI](datasheet/ET5410SCPI.txt)** — Reference complete des commandes (corrigee et augmentee)

## Protocole SCPI

La communication utilise des commandes SCPI sur un port serie USB virtuel.

| Parametre | Valeur |
|-----------|--------|
| Baud rates | 7200, 9600, 14400 |
| Data bits | 8 |
| Stop bits | 1 |
| Parite | Aucune |
| Terminaison | `0x0A` (LF) |

**Commandes non documentees decouvertes** par scan brute-force (voir scripts `scan_*.py`) :

| Commande | Description |
|----------|-------------|
| `BATT:BTC` | Cutoff capacite batterie (Ah) |
| `BATT:BTE` | Cutoff energie batterie (Wh) |
| `TIME:BTT` | Cutoff temps batterie (secondes) |
| `BATT:ENER?` | Lecture energie dechargee (Wh) |
| `CURR:BCC` | Courant batterie pour cutoff non-voltage (A) |

## Structure du projet

```
index.html                  Application web fichier unique (HTML + CSS + JS)
DOCUMENTATION.md            Documentation technique (EN)
DOCUMENTATION-fr.md         Documentation technique (FR)
USER_MANUAL.md              Manuel utilisateur (EN)
USER_MANUAL-fr.md           Manuel utilisateur (FR)
datasheet/
  ET5410SCPI.pdf            Documentation SCPI constructeur (45 pages)
  ET5410SCPI.txt            Reference SCPI corrigee et augmentee
data/
  *.ET5410                  Fichiers de configuration
scan_*.py                   Scripts de decouverte SCPI par brute-force
```

## Licence

Ce projet est sous [licence MIT](LICENSE).
