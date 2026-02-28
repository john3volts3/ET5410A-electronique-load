[English version](USER_MANUAL.md)

# ET5410 Web Controller — Manuel utilisateur

## Demarrage rapide

1. **Ouvrir** `index.html` dans **Chrome** (89+) ou **Edge** (89+)
2. **Connecter** la charge electronique ET5410 via cable USB
3. Dans l'onglet **Connexion**, selectionner le baud rate (14400 par defaut) et cliquer **Connecter**
4. Le navigateur affiche la liste des ports serie : choisir celui de l'ET5410
5. L'identifiant de l'appareil s'affiche (ex: `East Tester, ET5410A+, ...`)

> **Note** : Si le message "Web Serial API: NON SUPPORTE" apparait, utilisez Chrome ou Edge.

---

## Onglet Connexion

Cet onglet gere la communication avec l'appareil.

| Element | Description |
|---|---|
| **Baud Rate** | Vitesse de communication (7200, 9600, 14400). Doit correspondre au reglage de l'appareil. |
| **Connecter** | Ouvre la connexion serie et lit la configuration de l'appareil |
| **Deconnecter** | Ferme la connexion et rend le controle au panneau avant (`SYST:LOCA`) |
| **Identifiant** | Affiche le modele, numero de serie et firmware apres connexion |

---

## Onglet Controle

C'est l'onglet principal pour piloter la charge.

### Selectionner un mode de charge

12 modes disponibles sous forme de boutons radio :

| Mode | Description |
|---|---|
| **CC** | Courant constant — la charge maintient un courant fixe |
| **CV** | Tension constante — la charge maintient une tension fixe |
| **CP** | Puissance constante |
| **CR** | Resistance constante |
| **CC+CV** | Deux etapes : courant constant puis tension constante |
| **CR+CV** | Deux etapes : resistance constante puis tension constante |
| **Tran** | Test dynamique — alternance entre deux niveaux |
| **List** | Profil multi-etapes (jusqu'a 50 etapes programmables) |
| **Scan** | Balayage progressif en courant, tension ou puissance |
| **Short** | Mode court-circuit |
| **Battery** | Test de decharge batterie (voir section dediee) |
| **LED** | Test de LED avec coefficient |

### Configurer les parametres

Selon le mode selectionne, les champs de parametres correspondants apparaissent :

- **CC** : valeur du courant (A)
- **CV** : valeur de la tension (V)
- **CP** : valeur de la puissance (W)
- **CR** : valeur de la resistance (Ohm)
- **CC+CV** : courant (A) + tension (V)
- **CR+CV** : resistance (Ohm) + tension (V)
- **LED** : courant (A), tension (V), coefficient

Des limites de protection (Vmax, Imax, Pmax) et le delai d'extinction sont aussi configurables.

### Activer / Desactiver la charge

- Cliquer **ON** pour activer la charge
- Cliquer **OFF** pour la desactiver

> **Important** : Changer de mode desactive automatiquement la charge.

### Mesures en direct

Quand la charge est activee (ON), les mesures s'affichent en temps reel :

- **TENSION** (jaune) — en Volts
- **COURANT** (bleu) — en Amperes
- **PUISSANCE** (orange) — en Watts
- **RESISTANCE** (violet) — en Ohms (uniquement pour les modes CR, CR+CV, List, LED)

Un **graphique** se dessine en temps reel sous les valeurs. Vous pouvez :

- **Afficher** : choisir le canal a tracer (Tension, Courant, Puissance, Resistance)
- **Intervalle** : ajuster la frequence de rafraichissement (100 a 10000 ms)
- **Points max** : limiter le nombre de points affiches (50 a 2000)
- **Effacer** : remettre le graphique a zero

---

## Sauvegarder / Charger une configuration

### Sauvegarder

1. Configurer le mode et les parametres souhaites
2. Cliquer **Sauver config** (en haut a droite de la carte "Mode de charge")
3. L'explorateur de fichiers s'ouvre avec un nom propose : `-ET5410-2026-02-27-CC.ET5410`
4. **Ajouter votre nom** devant le tiret (ex: `MonTest-ET5410-2026-02-27-CC.ET5410`)
5. Choisir l'emplacement et cliquer Enregistrer

Le fichier sauvegarde contient :
- Le mode de charge selectionne
- Les parametres systeme (limites, ranges, trigger)
- Les parametres specifiques au mode

### Charger

1. Cliquer **Charger config**
2. Selectionner un fichier `.ET5410`
3. Le mode et tous les parametres sont restaures automatiquement

> **Note** : Le fichier ne contient que les parametres du mode qui etait selectionne au moment de la sauvegarde.

---

## Test Batterie

Le mode Battery permet de realiser un test complet de decharge de batterie avec suivi en temps reel.

### Configuration

1. Selectionner le mode **Battery** dans l'onglet Controle
2. Choisir le **mode de decharge** :
   - **CC** (Courant constant) — decharge a courant fixe
   - **CR** (Resistance constante) — decharge a resistance fixe
3. Choisir le **type de coupure** :
   - **Voltage** — arret quand la tension atteint le seuil
   - **Capacite** — arret quand la capacite dechargee atteint le seuil (Ah)
   - **Energie** — arret quand l'energie dechargee atteint le seuil (Wh)
   - **Temps** — arret apres une duree definie (heures, minutes, secondes)
4. Configurer les **valeurs** : tension de coupure, courant/resistance, seuils

> **Attention** : Le type de coupure (Voltage/Capacite/Energie/Temps) doit aussi etre selectionne sur le panneau avant de l'appareil via le bouton SET. L'application ne peut pas changer ce reglage par commande SCPI.

### Deroulement du test

| Bouton | Action |
|---|---|
| **Start** | Demarre le test, active la charge, lance le suivi |
| **Pause** | Met le test en pause (charge OFF), conserve les donnees. Le label "PAUSE" clignote. |
| **Reprendre** | Relance le test depuis ou il s'etait arrete |
| **Stop** | Arrete definitivement le test, desactive la charge |
| **Reset** | Efface toutes les donnees et le graphique |

### Statistiques affichees

Pendant le test, 6 indicateurs sont mis a jour en temps reel :

| Indicateur | Description |
|---|---|
| **TENSION** | Tension instantanee de la batterie (V) |
| **CONSIGNE** | Courant (A) ou resistance (Ohm) programme |
| **PUISSANCE** | Puissance instantanee (W) |
| **CAPACITE** | Capacite dechargee cumulee (Ah) |
| **ENERGIE** | Energie dechargee cumulee (Wh) |
| **DUREE** | Temps ecoule (HH:MM:SS) |

### Graphique de decharge

Le graphique affiche la **courbe de tension** au fil du temps.

**Navigation :**
- **Zoom -** / **Zoom +** : changer l'echelle de temps (1 min a 480 min)
- **Auto** : ajuste automatiquement le zoom
- **Theme** : basculer entre fond sombre et fond clair

**Tooltip interactif** : survolez le graphique avec la souris pour voir les valeurs exactes (tension + temps) a la position du curseur.

### Exports

| Bouton | Format | Contenu |
|---|---|---|
| **TXT** | Texte tab-separe | Temps (s) et Tension (V) |
| **Excel** | CSV point-virgule | Temps (s) et Tension (V) — s'ouvre dans Excel |
| **SVG** | Image vectorielle | Graphique complet (grille, courbe, labels) |
| **Image** | PNG | Statistiques + graphique |
| **PDF** | Rapport imprimable | Parametres, resultats, statistiques min/max/moy, graphique en theme clair, tableau de donnees |

---

## Onglet Mesures

Cet onglet permet un suivi independant des mesures, sans lien avec le mode de charge.

### Utilisation

1. Cliquer **Demarrer** pour lancer le polling
2. Les 4 valeurs se mettent a jour en continu : Tension, Courant, Puissance, Resistance
3. Ajuster l'**intervalle** (ms) pour la frequence de rafraichissement
4. Cliquer **Arreter** pour stopper le polling

### Graphique

- **Afficher** : choisir le canal a tracer (Tension, Courant, Puissance, Resistance)
- **Points max** : nombre maximum de points affiches
- **Effacer** : remettre le graphique a zero

> **Note** : L'onglet Mesures peut fonctionner en meme temps que le test batterie ou les mesures live du Controle.

---

## Onglet MPPT

L'onglet MPPT permet de rechercher le **point de puissance maximale** (Maximum Power Point) d'une source DC (panneau solaire, generateur) en balayant le courant de charge.

### Choix du mode

Deux modes de recherche sont disponibles via les boutons radio en haut de la configuration :

| Mode | Description |
|---|---|
| **Scan lineaire** | Balayage du courant de depart au courant max par increments fixes (step). Trace les courbes tension et puissance. Exhaustif mais plus lent. |
| **Dichotomie** | Recherche ternaire qui divise l'intervalle en 3, compare la puissance aux deux tiers, et elimine le tiers le moins performant. Converge en ~10-15 mesures. Affiche les points en nuage. |

### Configuration

Les champs affiches dependent du mode selectionne :

**Mode Scan lineaire :**

| Parametre | Description |
|---|---|
| **Courant depart (A)** | Courant initial du balayage |
| **Courant max (A)** | Courant de fin du balayage |
| **Step (A)** | Increment entre chaque mesure |
| **Tension min (V)** | Seuil d'arret si la tension tombe en dessous |
| **Delai entre steps (ms)** | Temps d'attente entre chaque mesure |

**Mode Dichotomie :**

| Parametre | Description |
|---|---|
| **Courant depart (A)** | Borne inferieure de l'intervalle de recherche |
| **Courant max (A)** | Borne superieure de l'intervalle de recherche |
| **Delai (ms)** | Temps d'attente entre chaque mesure (500 ms recommande) |

> **Note** : En mode dichotomie, le champ **Step** (masque) sert de tolerance de convergence. Le champ **Tension min** (masque) reste actif comme seuil de securite.

### Deroulement

| Bouton | Action |
|---|---|
| **Start** | Lance la recherche : passe en mode CC, active la charge, commence les mesures |
| **Stop** | Arrete la recherche en cours et desactive la charge |
| **Reset** | Efface les donnees et le graphique |

### Resultat MPP

A la fin de la recherche, le point de puissance maximale est affiche :

- **MPP Courant** (bleu) — courant optimal en Amperes
- **MPP Tension** (jaune) — tension au point optimal en Volts
- **MPP Puissance** (vert) — puissance maximale en Watts
- **MPP Resistance** (violet) — resistance equivalente en Ohms

### Graphique

Le graphique affiche les mesures en temps reel pendant la recherche :

- **Mode scan** : courbes continues (jaune = tension, orange = puissance)
- **Mode dichotomie** : nuage de points (cercles jaunes = tension, cercles orange = puissance)
- **Point MPP** : cercle vert avec label de puissance et ligne verticale pointillee
- **Theme** : basculer entre fond sombre et fond clair

### Exports

| Bouton | Format | Contenu |
|---|---|---|
| **Export CSV** | CSV point-virgule | Courant (A), Tension (V), Puissance (W) |
| **Export PNG** | Image PNG | Statistiques + graphique |

### Sauvegarder / Charger la configuration MPPT

Les boutons **Sauver config** / **Charger config** en haut de la carte sauvegardent tous les parametres MPPT (mode, courants, delais) ainsi que les parametres systeme dans un fichier `.ET5410`.

> **Conseil** : Pour un panneau solaire, commencer avec un delai de 500 ms. Des delais plus courts (100-200 ms) peuvent donner des mesures imprecises si la source a une capacite parasite.

---

## Onglet Qualification

Permet de tester si les mesures sont dans les limites definies.

### Configuration

1. Definir les **limites** pour chaque grandeur :
   - Tension : V High / V Low
   - Courant : I High / I Low
   - Puissance : P High / P Low
2. Selectionner les **ranges** de tension et de courant (HIGH ou LOW)
3. Activer le test : **Test = ON**
4. Cliquer **Lire** pour obtenir le resultat : **PASS** ou **FAIL**

---

## Onglet Systeme

Gestion des parametres systeme de l'appareil.

### Protections

| Parametre | Description |
|---|---|
| **Vmax** | Limite de surtension (V) |
| **Imax** | Limite de surcourant (A) |
| **Pmax** | Limite de surpuissance (W) |
| **Von / Voff** | Seuils de tension d'activation/desactivation |
| **Off Delay** | Delai avant extinction (s) |

### Reglages

| Parametre | Description |
|---|---|
| **Mode demarrage** | Comportement au demarrage (ON/OFF) |
| **Langue** | Langue de l'appareil |
| **Baud Rate** | Vitesse de communication serie |

### Gestion des fichiers appareil

L'appareil peut stocker des configurations en memoire interne :

| Bouton | Action |
|---|---|
| **Stocker** | Sauvegarde la config dans un slot de l'appareil |
| **Rappeler** | Charge une config depuis un slot |
| **Supprimer** | Efface un slot |
| **Verifier** | Verifie si un slot contient des donnees |

---

## Onglet Terminal

Console SCPI pour communication directe avec l'appareil.

### Utilisation

1. Taper une commande dans le champ de saisie (ex: `*IDN?`, `MEAS:ALL?`, `CH:MODE CC`)
2. Appuyer sur **Entree** ou cliquer **Envoyer**
3. La reponse s'affiche dans le journal en dessous

### Boutons rapides

- **MEAS:ALL?** — Lire toutes les mesures
- **CH:MODE?** — Lire le mode actuel
- **CRANge?** — Lire le range de courant

### Exemples de commandes

```
*IDN?                  Identification de l'appareil
CH:MODE?               Mode actuel (CC, CV, CR, etc.)
CH:MODE CC             Passer en mode CC
CH:SW ON               Activer la charge
CH:SW OFF              Desactiver la charge
MEAS:ALL?              Toutes les mesures (I V P R)
CURR:CC 1.5            Regler le courant CC a 1.5A
VOLT:CV 12.0           Regler la tension CV a 12V
SYST:LOCA              Rendre le controle au panneau avant
```

---

## Astuces

- **Ouverture rapide** : ouvrez `index.html` directement depuis l'explorateur de fichiers (double-clic) — pas besoin de serveur web
- **Nom de config** : le nom propose commence par `-` pour vous permettre d'ecrire votre nom devant (ex: `BattLiPo4S-ET5410-2026-02-27-CC.ET5410`)
- **Export Excel** : le format CSV utilise le point-virgule comme separateur — Excel l'ouvre correctement en Europe
- **Stabilite USB** : si le port USB se bloque, debrancher et rebrancher le cable, puis reconnecter
- **Plusieurs onglets** : les mesures live (Controle), le polling (Mesures) et le test batterie peuvent coexister simultanement
- **Changement de mode** : changer de mode desactive automatiquement la charge — c'est un comportement de l'appareil, pas de l'application
