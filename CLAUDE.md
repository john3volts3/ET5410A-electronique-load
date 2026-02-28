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
- **UI language** : English (all labels, messages, tooltips, PDF report)
- **7 tabs** : Connection, Control, MPPT, Measurements, Qualification, System, Terminal (+ inline sub-sections: Dynamic/TRAN, Scan, List, Battery when corresponding mode is selected)
- **Header** : title, Connect/Disconnect buttons, PC/Auto radios, theme toggle ◐, connection status (sticky with tabs-nav via `#sticky-top`)
- **Dark/light theme** : neutral Slate palette (blue-grey accent), toggle persisted via localStorage
- **Ghost/outline buttons**, cards with h3 legend-style, system-ui 18px font
- **needs-conn** : class on SCPI action buttons, disabled when not connected (explanatory tooltip)
- **updateUIConnState(on)** : enables/disables all `.needs-conn` on connect/disconnect
- **Graph colors** : voltage in red (#e05050 dark / #c03030 light) in all graphs (BATT, MPPT, Measurements, Control live); `--color-volt` (yellow) kept for text values outside graphs
- **smartStep()** : logarithmic increments on numeric spinners
- **Comma decimal separator** : all number inputs accept comma (converted to period via `execCommand('insertText')`)
- **Battery auto-stop** : `battPoll()` checks `CH:SW?` each cycle; if `OFF` → `battStop(false)` + green "COMPLETED" label
- **Off Delay** : Hours/Minutes/Seconds fields with real-time countdown
- Open directly in browser via `file://` or local server

## Language

Communiquer en français.
