"""
Scan: chercher la commande SCPI du sélecteur de type cutoff batterie.
Approche double:
  1. Query (CMD?) - cherche les commandes qui retournent une valeur
  2. Set (CMD 0) - cherche les commandes SET-only qui retournent "Rexecu success"
Filtre "Rcmd err" = commande inconnue.
"""
import serial
import time
import sys

PORT = 'COM3'
BAUD = 14400
TIMEOUT = 1.0
DELAY = 0.6

def send_recv(ser, cmd):
    ser.reset_input_buffer()
    ser.write((cmd + '\n').encode())
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
    return text

def is_valid(text):
    """True si la réponse n'est PAS une erreur."""
    if not text:
        return False
    if 'err' in text.lower():
        return False
    return True

def main():
    print("=== SCAN CUTOFF TYPE SELECTOR ===")
    print(f"Port: {PORT}, Baud: {BAUD}")

    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit(1)

    time.sleep(1)
    ser.reset_input_buffer()
    time.sleep(0.3)

    # Vérifier connexion
    r = send_recv(ser, '*IDN?')
    print(f"*IDN? -> {r}")
    if not is_valid(r):
        time.sleep(0.5)
        r = send_recv(ser, '*IDN?')
        print(f"*IDN? (retry) -> {r}")
    if not is_valid(r):
        print("Pas de connexion")
        ser.close()
        sys.exit(1)
    print()
    time.sleep(DELAY)

    found_query = []
    found_set = []

    # === PHASE 1: Candidats ciblés (query + set) ===
    targeted = [
        # Pattern BT* (comme BTC, BTE, BTT)
        'BATT:BTM', 'BATT:BTMO', 'BATT:BTMOD', 'BATT:BTMODE',
        'BATT:BTS', 'BATT:BTSE', 'BATT:BTSEL',
        'BATT:BTCU', 'BATT:BTCUT',
        'BATT:BTTY', 'BATT:BTTYP', 'BATT:BTTYPE',
        'BATT:BTCO', 'BATT:BTCON', 'BATT:BTCOND',
        # Pattern CUT/CUTOFF
        'BATT:CUT', 'BATT:CUTO', 'BATT:CUTOF', 'BATT:CUTOFF',
        'BATT:CUTM', 'BATT:CUTMO', 'BATT:CUTMOD',
        'BATT:CUTT', 'BATT:CUTTY', 'BATT:CUTTYP',
        # Pattern court
        'BATT:CT', 'BATT:CM', 'BATT:TY', 'BATT:CO', 'BATT:SE',
        'BATT:MOD', 'BATT:MODE2', 'BATT:SEL', 'BATT:TYPE', 'BATT:COND',
        'BATT:END', 'BATT:STOP', 'BATT:TERM', 'BATT:OFF',
        # Dans TIME: (comme BTT)
        'TIME:BTM', 'TIME:BTMO', 'TIME:BTMOD',
        'TIME:CUT', 'TIME:CUTM', 'TIME:CUTMOD',
        'TIME:MOD', 'TIME:TYPE', 'TIME:SEL',
        # Dans CURR: (comme BCC)
        'CURR:BCM', 'CURR:BCMO', 'CURR:BCMOD',
        'CURR:BCT', 'CURR:BCTY', 'CURR:BCTYP',
        'CURR:BCS', 'CURR:BCSE', 'CURR:BCSEL',
        # Autres subsystèmes
        'LOAD:CUT', 'LOAD:CUTM', 'LOAD:CUTMOD', 'LOAD:CUTOFF',
        'LOAD:BCUT', 'LOAD:BATTCUT',
        'CH:CUT', 'CH:CUTM', 'CH:CUTMOD', 'CH:CUTOFF',
        'SYSSet:CUT', 'SYSSet:CUTM',
    ]

    print(f"--- Phase 1: {len(targeted)} candidats cibles ---\n")
    for cmd in targeted:
        # Test query
        r = send_recv(ser, cmd + '?')
        if is_valid(r):
            found_query.append((cmd + '?', r))
            print(f"  *** QUERY {cmd}? -> {r}")
        time.sleep(0.3)

        # Test set (valeur 0)
        r = send_recv(ser, cmd + ' 0')
        if is_valid(r):
            found_set.append((cmd + ' 0', r))
            print(f"  *** SET   {cmd} 0 -> {r}")
        time.sleep(0.3)

    # === PHASE 2: Brute-force BATT:XX (2 lettres) ===
    import string
    known_batt = {'MODE', 'CAPA', 'ENER', 'BTC', 'BTE'}

    print(f"\n--- Phase 2: Brute-force BATT:XX (2 lettres, U-Z restant) ---\n")
    count = 0
    for c1 in 'UVWXYZ':  # A-T déjà scannés sans résultat
        for c2 in string.ascii_uppercase:
            suffix = c1 + c2
            if suffix in known_batt:
                continue
            cmd = 'BATT:' + suffix

            # Query
            r = send_recv(ser, cmd + '?')
            if is_valid(r):
                found_query.append((cmd + '?', r))
                print(f"  *** QUERY {cmd}? -> {r}")

            time.sleep(0.3)

            # Set
            r = send_recv(ser, cmd + ' 0')
            if is_valid(r):
                found_set.append((cmd + ' 0', r))
                print(f"  *** SET   {cmd} 0 -> {r}")

            time.sleep(0.3)
            count += 1

        if count % 26 == 0:
            print(f"  ... {c1}* done ({count}/676)")

    # === PHASE 3: Brute-force BATT:XXX (3 lettres, seulement les plus probables) ===
    prefixes_3 = ['CUT', 'MOD', 'SEL', 'TYP', 'END', 'STO', 'CON', 'OFF', 'BTM', 'BTS', 'BTC']
    print(f"\n--- Phase 3: BATT:XXX (3 lettres, préfixes probables + 1 lettre) ---\n")
    for pfx in prefixes_3:
        for c in string.ascii_uppercase:
            suffix = pfx + c
            if suffix in known_batt:
                continue
            cmd = 'BATT:' + suffix

            r = send_recv(ser, cmd + '?')
            if is_valid(r):
                found_query.append((cmd + '?', r))
                print(f"  *** QUERY {cmd}? -> {r}")
            time.sleep(0.2)

            r = send_recv(ser, cmd + ' 0')
            if is_valid(r):
                found_set.append((cmd + ' 0', r))
                print(f"  *** SET   {cmd} 0 -> {r}")
            time.sleep(0.2)

    ser.close()

    print(f"\n{'='*50}")
    print(f"=== RESULTATS ===")
    if found_query:
        print(f"\nQUERY ({len(found_query)}):")
        for cmd, r in found_query:
            print(f"  {cmd} -> {r}")
    if found_set:
        print(f"\nSET ({len(found_set)}):")
        for cmd, r in found_set:
            print(f"  {cmd} -> {r}")
    if not found_query and not found_set:
        print("  Aucune commande trouvee.")

    with open('scan_cutoff_type_results.log', 'w') as f:
        f.write(f"Scan cutoff type - {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for cmd, r in found_query:
            f.write(f"QUERY: {cmd} -> {r}\n")
        for cmd, r in found_set:
            f.write(f"SET: {cmd} -> {r}\n")
    print("\nResultats sauvegardes dans scan_cutoff_type_results.log")

if __name__ == '__main__':
    main()
