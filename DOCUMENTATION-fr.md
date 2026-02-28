[English version](DOCUMENTATION.md)

# ET5410 Web Controller — Documentation technique

## Presentation

Interface web de controle pour la charge electronique programmable DC **ET5410** (Hangzhou Zhongchuang Electronics). Application mono-fichier (`index.html`) communiquant via le protocole SCPI sur port serie USB.

**Materiels supportes :**
- ET5410 (150V / 40A / 400W)
- ET5411 (150V / 15A / 150W)
- ET5420 (150V / 20A / 200W)

**Fonctionnalites principales :**
- 12 modes de charge (CC, CV, CP, CR, CC+CV, CR+CV, Tran, List, Scan, Short, Battery, LED)
- Mesures temps reel avec graphique (V, A, W, R)
- Test de decharge batterie avec graphique, statistiques, arret automatique au cutoff et exports
- Recherche MPPT (scan lineaire + dichotomie) avec graphique et exports
- Sauvegarde/chargement de configurations (.ET5410)
- Console SCPI directe (Terminal)
- Qualification, protections, gestion fichiers appareil

## Architecture

```
index.html          Fichier unique : HTML + CSS + JS embarques
                    Zero dependance externe
                    Ouvrir directement via file:// ou serveur local
```

L'application repose sur la **Web Serial API** (Chrome 89+ / Edge 89+) pour communiquer avec l'appareil via un port serie USB virtuel.

### Principes de conception

- **Fichier unique** : tout le code est dans `index.html` (~2700 lignes)
- **Theme sombre** : adapte aux instruments de mesure
- **Polling sequentiel** : boucles `while` avec `await` (pas de `setInterval` pour eviter les chevauchements de commandes serie)
- **Garde SYST:LOCA** : empeche l'envoi de la commande de retour au mode local pendant les tests actifs

## Prerequis

| Prerequis | Detail |
|---|---|
| Navigateur | Chrome 89+ ou Edge 89+ (Web Serial API) |
| Cable | USB vers l'appareil ET5410 |
| Driver | Driver USB serie (installe automatiquement sous Windows 10/11) |

## Structure des fichiers

```
ET5410A-electronique-load/
  index.html                    Application web (fichier unique)
  CLAUDE.md                     Instructions projet pour Claude Code
  DOCUMENTATION.md              Documentation technique (EN)
  DOCUMENTATION-fr.md           Ce fichier (FR)
  USER_MANUAL.md                User manual (EN)
  USER_MANUAL-fr.md             Manuel utilisateur (FR)
  datasheet/
    ET5410SCPI.pdf              Documentation SCPI constructeur (45 pages)
    ET5410SCPI.txt              Reference SCPI corrigee et augmentee
  data/
    *.ET5410                    Fichiers de configuration sauvegardes
  scpi_scan.py                  Script de scan brute-force SCPI
  scan_batt_curr.py             Script de recherche commandes batterie
  scan_cutoff_mode.py           Script de recherche mode cutoff
  scan_cutoff_type.py           Script de recherche type cutoff
```

## Protocole SCPI

### Parametres serie

| Parametre | Valeur |
|---|---|
| Interface | USB (port serie virtuel) |
| Baud rates | 7200, 9600, 14400 (selon modele) |
| Data bits | 8 |
| Stop bits | 1 |
| Parite | Aucune |
| Terminaison | `0x0A` (LF) |

### Format des reponses

- **Valeurs numeriques** : prefixe `R` suivi de la valeur
  - Exemples : `R0.60`, `R 2.307`, `R155.00`
- **Valeurs texte/enum** : pas de prefixe
  - Exemples : `CC`, `ON`, `HIGH`, `NONE`, `PASS`
- **MEAS:ALL?** : `R <courant> <tension> <puissance> <resistance>` (separes par espaces)
  - Exemple : `R 1.234 12.345 15.23 10.00`
- **Erreurs** : `cmd err` ou `Rcmd err` (commande inconnue)

### Parsing dans le code

```javascript
// Retrait prefixe R
function stripPrefix(r) {
  const s = r.trim();
  if (/^R\s*[-.\d]/.test(s)) return s.substring(1).trim();
  return s;
}

// Parsing MEAS:ALL?
const cleaned = r.replace(/^[A-Za-z]\s+/, '');
const parts = cleaned.trim().split(/\s+/).map(s => parseFloat(s));
const [courant, tension, puissance, resistance] = parts;
```

## Modes de charge

| Mode | Valeur SCPI | Commande valeur | Description |
|---|---|---|---|
| CC | `CC` | `CURR:CC <n>` | Courant constant |
| CV | `CV` | `VOLT:CV <n>` | Tension constante |
| CP | `CP` | `POWE:CP <n>` | Puissance constante |
| CR | `CR` | `RESI:CR <n>` | Resistance constante |
| CC+CV | `CCCV` | `CURR:CCCV`, `VOLT:CCCV` | 2 etapes courant puis tension |
| CR+CV | `CRCV` | `RESI:CRCV`, `VOLT:CRCV` | 2 etapes resistance puis tension |
| Tran | `TRAN` | `TRAN:MODE`, `CURR:TA/TB`, etc. | Test dynamique/transitoire |
| List | `LIST` | `LIST:MODE`, `LIST:NUM`, etc. | Profil multi-etapes (50 max) |
| Scan | `SCAN` | `SCAN:TYPE`, `CURR:STARt/END`, etc. | Balayage courant/tension/puissance |
| Short | `SHOR` | — | Court-circuit |
| Battery | `BATT` | `BATT:MODE`, `VOLT:BCC1`, etc. | Test de decharge batterie |
| LED | `LED` | `CURR:LED`, `VOLT:LED`, `LED:COEFf` | Test LED |

## Commandes SCPI decouvertes (non documentees)

Ces commandes ont ete trouvees par scan brute-force et ne figurent pas dans la documentation constructeur :

| Commande | Sous-systeme | Description | Exemple reponse |
|---|---|---|---|
| `BATT:BTC <n>` / `?` | BATT | Cutoff capacite (Ah) | `R10.000` |
| `BATT:BTE <n>` / `?` | BATT | Cutoff energie (Wh) | `R50.000` |
| `TIME:BTT <n>` / `?` | TIME | Cutoff temps (secondes) | `R600` |
| `BATT:ENER?` | BATT | Energie dechargee (Wh, lecture seule) | `R136.032` |
| `CURR:BCC <n>` / `?` | CURR | Courant CC pour cutoff non-voltage | `R1.000` |

**Pattern de nommage** : `BT` = **B**attery **T**est + premiere lettre (**C**apacity, **E**nergy, **T**ime).

**Limitation** : le selecteur de mode cutoff (Voltage/Capacite/Energie/Temps) n'a pas de commande SCPI correspondante. Il ne peut etre change que depuis le panneau avant de l'appareil.

## Architecture JavaScript

### Classe ET5410

```
class ET5410 {
  connect(baudRate)     Ouvre le port serie via Web Serial API
  disconnect()          Envoie SYST:LOCA puis ferme le port
  send(cmd)             Envoie une commande sans attendre de reponse
  query(cmd)            Envoie une commande et attend la reponse
}
```

### Systeme de polling

Trois systemes de polling independants coexistent :

| Systeme | Variable de controle | Fonction boucle | Utilisation |
|---|---|---|---|
| Controle (live) | `ctrlLiveTimer` / `ctrlLivePollId` | `ctrlLivePollLoop()` | Mesures live quand charge ON |
| Batterie | `battTimer` / `battPollId` | `battPollLoop()` | Test de decharge batterie (arret auto via `CH:SW?`) |
| Mesures | `measTimer` | `setInterval(measPoll)` | Onglet Mesures independant |
| MPPT | `mpptTimer` / `mpptPollId` | `mpptPollLoop()` / `mpptDichoLoop()` | Recherche point de puissance max |

**Pattern anti-doublon** (controle et batterie) :
```javascript
async function xxxPollLoop(myId) {
  while (xxxTimer && xxxPollId === myId) {
    const t0 = Date.now();
    await xxxPoll();
    const elapsed = Date.now() - t0;
    if (xxxTimer && xxxPollId === myId) {
      await new Promise(r => setTimeout(r, Math.max(0, interval - elapsed)));
    }
  }
}
```

### Gestion pcSession

`pcSession` empeche l'envoi de `SYST:LOCA` entre chaque commande (ce qui ferait clignoter l'ecran de l'appareil).

```javascript
// Garde dans send() et query()
if (!pcSession && !battTimer && !ctrlLiveTimer && !cmd.startsWith('SYST:LOCA')) {
  await sendLocalReturn();
}
```

**Coordination** : chaque systeme de polling met `pcSession = true` au demarrage et ne le remet a `false` que si les deux autres sont inactifs.

### Arret automatique batterie

A la fin de chaque cycle `battPoll()`, l'application interroge `CH:SW?` pour verifier si l'appareil a automatiquement coupe la charge (cutoff atteint). Si la reponse est `OFF`, `battStop(false)` est appele (sans envoyer de commande OFF, puisque l'appareil l'a deja fait) et un label vert "COMPLETED" s'affiche.

### Separateur decimal virgule

Tous les champs `<input type="number">` acceptent le point et la virgule comme separateur decimal. Un listener `keydown` intercepte la touche virgule et insere un point a la position du curseur via `document.execCommand('insertText')`.

## MPPT (Maximum Power Point Tracking)

### Architecture

Le systeme MPPT utilise un helper commun `mpptMeasureAt(current)` reutilise par les deux modes :

```javascript
async function mpptMeasureAt(current) {
  // 1. Envoie CURR:CC <current>
  // 2. Attend le delai configure (mppt-delay ou mppt-dicho-delay)
  // 3. Lit MEAS:ALL? → [ci, v, p, r]
  // 4. Enregistre le point dans mpptData (avec ci mesure)
  // 5. Met a jour mpptBest si p > meilleure puissance
  // 6. Redessine le graphique
  // 7. Retourne { v, p } ou { v, p, lowV: true } si v < Vmin, ou null si erreur
}
```

### Mode Scan lineaire

`mpptPollLoop(myId)` → `mpptPoll()` → `mpptMeasureAt(mpptCurrentI)`

Boucle simple : mesure au courant actuel, incremente `mpptCurrentI` de `iStep`, arret quand `mpptCurrentI > iMax` ou `v < vMin`.

### Mode Dichotomie (recherche ternaire)

`mpptDichoLoop(myId)` → `mpptMeasureAt(m1)`, `mpptMeasureAt(m2)`

```
Algorithme :
  lo = iStart, hi = iMax
  Tant que (hi - lo) > tolerance :
    m1 = lo + (hi - lo) / 3
    m2 = hi - (hi - lo) / 3
    Mesurer P a m1 et m2
    Si V < Vmin a m1 → hi = m1 (courant trop eleve)
    Si V < Vmin a m2 → hi = m2 (courant trop eleve)
    Si P(m1) < P(m2) → lo = m1
    Sinon → hi = m2
  Mesure finale a (lo + hi) / 2
```

Convergence typique : ~10-15 mesures (au lieu de centaines pour le scan).

### Graphique

- **Mode scan** : courbes lineaires reliant les points (tension jaune, puissance orange)
- **Mode dichotomie** : nuage de points (cercles r=4), axe X fixe [iStart, iMax]
- **Point MPP** : cercle vert (r=6) + label + ligne verticale pointillee (commun aux 2 modes)

### Gestion V < Vmin en dichotomie

Quand `mpptMeasureAt` detecte `v < vMin`, elle retourne `{ v, p, lowV: true }` au lieu de `null`. La boucle dichotomie reduit alors `hi` (borne superieure) au lieu de s'arreter, ce qui recentre la recherche vers les courants plus bas.

## Fichiers de configuration (.ET5410)

### Format

Fichier texte avec paires `cle=valeur`, commentaires `#` :

```
# ET5410 Configuration
# Date: 2026-02-27 14:30:00
# Mode: CC

ctrl-mode=CC

# Systeme
ctrl-vmax=60
ctrl-imax=40
ctrl-pmax=400
ctrl-offdelay=0
ctrl-vrange=HIGH
ctrl-crange=HIGH
ctrl-trig=MAN

# CC
ctrl-cc-val=1.500
```

### Contenu sauvegarde

- **Toujours** : mode, parametres systeme (limites, ranges, trigger, off delay)
- **Selon le mode** : uniquement les parametres specifiques au mode selectionne
- **MPPT** : parametres MPPT + mode (scan/dicho) + parametres systeme
- **Nom propose** : `-ET5410-AAAA-MM-JJ-MODE.ET5410` (le tiret initial permet a l'utilisateur de prefixer son nom)

## Exports

### Test batterie

| Format | Contenu | Extension |
|---|---|---|
| TXT | Donnees tab-separees (temps, tension) | `.txt` |
| CSV | Donnees point-virgule (convention europeenne) | `.csv` |
| SVG | Graphique vectoriel (grille + courbe + labels) | `.svg` |
| PNG | Image stats + graphique | `.png` |
| PDF | Rapport complet (parametres, resultats, statistiques, graphique, tableau) | via impression |

### Theme du graphique

Le graphique batterie supporte deux themes :

| Theme | Fond | Grille | Courbe tension | Curseur |
|---|---|---|---|---|
| Dark | `#000000` | `#333333` | `#ff5252` | `rgba(255,255,255,0.4)` |
| Light | `#ffffff` | `#cccccc` | `#d32f2f` | `rgba(0,0,0,0.3)` |

Le PDF est toujours genere en theme clair pour l'impression.
