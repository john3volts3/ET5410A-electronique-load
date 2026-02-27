"""
Scan ciblé: chercher la commande SCPI du sélecteur de mode cutoff batterie.
Approche: tester des mots SCPI plausibles (3-7 lettres) dans BATT: et TIME:
Filtre les réponses "cmd err" / "Rcmd err" (= commande inconnue).
"""
import serial
import time
import sys

PORT = 'COM3'
BAUD = 14400
DELAY = 0.5
TIMEOUT = 0.8

# Commandes déjà connues
KNOWN = {
    'BATT:MODE', 'BATT:CAPA', 'BATT:ENER', 'BATT:BTC', 'BATT:BTE',
    'TIME:OFFDELAY', 'TIME:WA', 'TIME:WB', 'TIME:STEP', 'TIME:BTT',
}

def build_candidates():
    """Génère des noms SCPI plausibles basés sur le vocabulaire courant."""
    words = [
        # Cutoff / stop / end / termination
        'CUT', 'CUTO', 'CUTOF', 'CUTOFF', 'CUTM', 'CUTMO', 'CUTMOD', 'CUTMODE',
        'CUTT', 'CUTTY', 'CUTTYP', 'CUTTYPE',
        'STOP', 'STOPM', 'STOPMO', 'STOPMOD', 'STOPMODE',
        'STOPT', 'STOPTY', 'STOPTYP', 'STOPTYPE',
        'END', 'ENDM', 'ENDMO', 'ENDMOD', 'ENDMODE',
        'ENDT', 'ENDTY', 'ENDTYP', 'ENDTYPE',
        'TERM', 'TERMI', 'TERMIN', 'TERMINATE',
        'TERMM', 'TERMMO', 'TERMMOD', 'TERMMODE',
        # Type / mode / select / condition
        'TYPE', 'TYP', 'TYPM', 'TYPMO', 'TYPMOD', 'TYPMODE',
        'SEL', 'SELE', 'SELEC', 'SELECT',
        'COND', 'CONDI', 'CONDIT', 'CONDITION',
        # Off / over / limit / discharge
        'OFF', 'OFFM', 'OFFMO', 'OFFMOD', 'OFFMODE',
        'OFFT', 'OFFTY', 'OFFTYP', 'OFFTYPE',
        'OVER', 'OVERM', 'OVERMOD', 'OVERMODE',
        'LIM', 'LIMI', 'LIMIT',
        'DIS', 'DISC', 'DISCH', 'DISCHAR',
        # Battery test patterns (comme BTC/BTE/BTT)
        'BTS', 'BTM', 'BTSM', 'BTMO', 'BTMOD', 'BTMODE',
        'BTST', 'BTSTO', 'BTSTOP',
        'BTEN', 'BTEND',
        'BTCU', 'BTCUT', 'BTCUTOFF',
        'BTSE', 'BTSEL', 'BTSELECT',
        'BTTY', 'BTTYP', 'BTTYPE',
        'BTCO', 'BTCON', 'BTCOND',
        # Threshold / compare (comme SCAN:THTYpe, SCAN:COMPare)
        'THTY', 'THTYP', 'THTYPE',
        'COMP', 'COMPA', 'COMPAR', 'COMPARE',
        # Set / config / run / test / state
        'SET', 'SETM', 'SETMOD', 'SETMODE',
        'CONF', 'CONFIG',
        'RUN', 'RUNM', 'RUNMOD', 'RUNMODE',
        'TEST', 'TESTM', 'TESTMOD', 'TESTMODE',
        'STAT', 'STATE', 'STATUS',
        'PROT', 'PROTECT',
        'PAR', 'PARA', 'PARAM',
        'VAL', 'VALU', 'VALUE',
        'SWI', 'SWITCH',
    ]

    candidates = []
    for prefix in ['BATT:', 'TIME:']:
        for w in words:
            cmd = prefix + w
            if cmd.upper() not in KNOWN:
                candidates.append(cmd)

    # Autres sous-systèmes avec mots clés battery
    for prefix in ['CH:', 'LOAD:', 'SYSSet:', 'SYST:']:
        for w in ['BCUT', 'BCUTOFF', 'BCUTMOD', 'BCUTMODE', 'BCUTTYP', 'BCUTTYPE',
                   'BATTCUT', 'BATTCUTOFF', 'BATTMOD', 'BATTMODE', 'BATTTYP', 'BATTTYPE',
                   'BATTEND', 'BATTENDMODE',
                   'BATTSTOP', 'BATTSTOPMODE',
                   'CUTOFF', 'CUTMODE', 'CUTTYPE', 'ENDMODE', 'ENDTYPE', 'STOPMODE',
                   'CUT', 'END', 'STOP', 'TERM']:
            cmd = prefix + w
            candidates.append(cmd)

    # Dédupliquer
    seen = set()
    unique = []
    for c in candidates:
        up = c.upper()
        if up not in seen:
            seen.add(up)
            unique.append(c)
    return unique

def query(ser, cmd):
    ser.reset_input_buffer()
    ser.write((cmd + '?\n').encode())
    time.sleep(0.2)
    response = b''
    end_time = time.time() + TIMEOUT
    while time.time() < end_time:
        if ser.in_waiting:
            response += ser.read(ser.in_waiting)
            if b'\n' in response:
                break
        time.sleep(0.05)
    text = response.decode('ascii', errors='replace').strip()
    if not text or 'err' in text.lower():
        return None
    return text

def main():
    candidates = build_candidates()
    print(f"=== SCAN CUTOFF MODE (mots SCPI plausibles) ===")
    print(f"Port: {PORT}, Baud: {BAUD}, Delay: {DELAY}s")
    print(f"{len(candidates)} candidates a tester (~{len(candidates)*DELAY/60:.1f} min)")
    print()

    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    except Exception as e:
        print(f"ERREUR ouverture port: {e}")
        sys.exit(1)

    time.sleep(1)

    found = []
    try:
        for i, cmd in enumerate(candidates):
            if (i+1) % 25 == 0:
                print(f"  ... {i+1}/{len(candidates)}")

            r = query(ser, cmd)
            if r:
                found.append((cmd, r))
                print(f"  *** FOUND: {cmd}? -> {r}")

            time.sleep(DELAY)

    except KeyboardInterrupt:
        print("\n--- Scan interrompu ---")
    finally:
        ser.close()

    print(f"\n=== SCAN TERMINE ===")
    if found:
        print(f"\n{len(found)} COMMANDE(S) TROUVEE(S):")
        for cmd, resp in found:
            print(f"  {cmd}? -> {resp}")
    else:
        print("Aucune nouvelle commande trouvee.")

    with open('scan_cutoff_results.log', 'w') as f:
        f.write(f"Scan cutoff mode - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Candidates: {len(candidates)}\n\n")
        for cmd, resp in found:
            f.write(f"FOUND: {cmd}? -> {resp}\n")
        if not found:
            f.write("Aucun resultat.\n")
    print("Resultats sauvegardes dans scan_cutoff_results.log")

if __name__ == '__main__':
    main()
