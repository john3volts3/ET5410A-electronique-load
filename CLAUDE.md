# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Projet de contrôle/interface pour la charge électronique programmable DC **ET5410** (Hangzhou Zhongchuang Electronics). Le matériel cible supporte plusieurs variantes : ET5410 (40A), ET5411 (15A), ET5420 (20A).

## Hardware Documentation

- `datasheet/ET5410SCPI.pdf` — Documentation complète du protocole SCPI (45 pages), référence principale pour l'implémentation.

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
- **10 onglets** : Connexion, Contrôle, Mesures, Dynamique, Batterie, Scan, List, Qualification, Système, Terminal
- **Thème sombre** adapté instruments de mesure
- Ouvrir directement dans le navigateur via `file://` ou serveur local

## Language

Communiquer en français.
