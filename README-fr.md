[English version](README.md)

# ET5410 Web Controller

Interface web de controle pour la charge electronique programmable DC **ET5410 / ET5411 / ET5420** (Hangzhou Zhongchuang Electronics / East Tester). Fichier HTML unique, zero dependance — ouvrir dans Chrome et connecter via USB.

## Fonctionnalites

- **12 modes de charge** — CC, CV, CP, CR, CC+CV, CR+CV, Dynamique, List (50 etapes), Scan, Short, Battery, LED
- **Mesures temps reel** — Tension, Courant, Puissance, Resistance avec graphique en direct
- **Test de decharge batterie** — Test complet avec courbe de tension, statistiques (min/max/moy), pause/reprise, et multiples formats d'export (TXT, CSV, SVG, PNG, rapport PDF)
- **Scan MPPT** — Recherche du point de puissance maximale (panneau solaire) avec deux modes : scan lineaire (pas a pas) et dichotomie (recherche ternaire, ~10-15 mesures). Graphique temps reel avec marqueur MPP, export CSV/PNG.
- **Sauvegarde/Chargement** — Export et import de configurations vers des fichiers `.ET5410`
- **Test de qualification** — Verification pass/fail des limites V, I, P
- **Terminal SCPI** — Console de commandes directe pour utilisation avancee
- **Gestion systeme** — Protections (OV/OC/OP), ranges, stockage fichiers appareil
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

- **[Manuel utilisateur (FR)](USER_MANUAL-fr.md)** / **[User Manual (EN)](USER_MANUAL.md)** — Guide d'utilisation pas a pas
- **[Documentation technique (FR)](DOCUMENTATION-fr.md)** / **[Technical Documentation (EN)](DOCUMENTATION.md)** — Architecture, protocole SCPI, composants JavaScript
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
