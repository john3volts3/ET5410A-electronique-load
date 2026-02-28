# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Projet de contrôle/interface pour la charge électronique programmable DC **ET5410** (Hangzhou Zhongchuang Electronics). Le matériel cible supporte plusieurs variantes : ET5410 (40A), ET5411 (15A), ET5420 (20A).

## Hardware Documentation

- `datasheet/ET5410SCPI.pdf` — Documentation complète du protocole SCPI (45 pages), référence principale pour l'implémentation.

## Documentation (bilingual EN/FR)

- `README.md` (EN + FR) — Présentation du projet (bilingue, ancre `#fr`)
- `USER_MANUAL.md` (EN) / `USER_MANUAL-fr.md` (FR) — Manuel utilisateur
- `DOCUMENTATION.md` (EN) / `DOCUMENTATION-fr.md` (FR) — Documentation technique
- `datasheet/ET5410SCPI.txt` — Référence SCPI complète (corrigée et augmentée)

## Communication Protocol

- **SCPI** (Standard Commands for Programmable Instruments) version 2017.7
- **Interface série** : RS485, baud rate par défaut 115200 bps (configurable : 4800–57600)
- **Format trame** : pas d'en-tête + commande + pas de checksum + `0x0A` (LF)
- **Adressage** : 0–255 pour RS485 multi-appareils

## Device Capabilities

- **Modes de charge** : CC, CV, CP, CR, CCCV, CRCV, dynamique (TRAN), batterie (BATT), scan (SCAN), liste (LIST jusqu'à 50 étapes)
- **2 canaux indépendants**
- **Protections** : OV, OC, OP, OT, LRV (inversion polarité), UN (défaut mesure)
- **Sous-systèmes SCPI** : SYST, LOAD, QUAL, SYSSet, COMM, VOLT, CURR, POWE, RESI, TIME, LED, TRAN, BATT, SCAN, LIST, CH, FILE, MEAS, SELF

## Application Web (index.html)

- **Fichier unique** `index.html` — HTML + CSS + JS embarqués, zéro dépendance
- **Web Serial API** (Chrome 89+ / Edge 89+) pour communication USB série
- **Classe `ET5410`** : `connect()`, `disconnect()`, `send(cmd)`, `query(cmd)` avec terminaison `\n` (0x0A)
- **10 onglets** : Contrôle, MPPT, Mesures, Dynamique, Batterie, Scan, List, Qualification, Système, Terminal
- **Header** : titre, boutons Connecter/Déconnecter, radios PC/Auto, toggle thème ◐, status connexion
- **Thème dark/light** : palette Slate neutre (accent bleu-gris), toggle persisté via localStorage
- **Boutons ghost/outline** uniformes, cards avec h3 legend-style, police system-ui 18px
- **needs-conn** : classe sur les boutons d'action SCPI, désactivés quand non connecté (tooltip explicatif)
- **updateUIConnState(on)** : active/désactive tous les `.needs-conn` à la connexion/déconnexion
- **Couleurs graphiques** : voltage en rouge (#e05050 dark / #c03030 light) dans tous les graphiques (BATT, MPPT, Mesures, Contrôle live) ; `--color-volt` (jaune) conservé pour les valeurs textuelles hors graphiques
- **smartStep()** : incréments logarithmiques sur les spinners numériques
- **Off Delay** : champs Heures/Minutes/Secondes avec décompte en temps réel
- Ouvrir directement dans le navigateur via `file://` ou serveur local

## Language

Communiquer en français.
