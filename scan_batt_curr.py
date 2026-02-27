"""
Scan: chercher la commande SCPI du courant batterie pour les modes
cutoff Time/Energy/Capacity (différent de CURR:BCC1/2/3 qui est pour Voltage).
"""
import serial
import time
import sys

PORT = 'COM3'
BAUD = 14400
TIMEOUT = 1.0
DELAY = 0.5

def query(ser, cmd):
    ser.reset_input_buffer()
    ser.write((cmd + '\n').encode())
    time.sleep(0.3)
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

def main():
    print(f"=== SCAN COURANT BATTERIE (non-Voltage cutoff) ===")
    print(f"Port: {PORT}, Baud: {BAUD}")
    print()

    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    except Exception as e:
        print(f"ERREUR ouverture port: {e}")
        sys.exit(1)

    time.sleep(1)
    # Vider le buffer résiduel
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    time.sleep(0.5)

    # Vérifier connexion (2 tentatives)
    for attempt in range(2):
        r = query(ser, '*IDN?')
        print(f"*IDN? (tentative {attempt+1}) -> {r}")
        if r and 'err' not in r.lower():
            break
        time.sleep(1)
    else:
        print("Pas de reponse valide - verifier connexion")
        ser.close()
        sys.exit(1)
    print()
    time.sleep(DELAY)

    # D'abord lire CURR:BCC1 pour référence
    r = query(ser, 'CURR:BCC1?')
    print(f"CURR:BCC1? (reference voltage-cutoff) -> {r}")
    time.sleep(DELAY)

    # Candidats pour le courant batterie non-voltage
    candidates = [
        # Pattern BT* comme BTC/BTE/BTT
        'CURR:BT?', 'CURR:BTI?', 'CURR:BTA?', 'CURR:BTB?', 'CURR:BTC?',
        'CURR:BTD?', 'CURR:BTCC?', 'CURR:BTCR?',
        # Pattern BATT
        'CURR:BATT?', 'CURR:BAT?', 'CURR:BA?',
        'BATT:CURR?', 'BATT:CUR?', 'BATT:I?',
        'BATT:BTI?', 'BATT:BTA?', 'BATT:BTCC?',
        # Pattern CC/discharge
        'CURR:DIS?', 'CURR:DISC?', 'CURR:DISCH?',
        'CURR:BC?', 'CURR:BCC?', 'CURR:BD?',
        # Sous-systèmes alternatifs
        'LOAD:CURR?', 'LOAD:BCURR?', 'LOAD:BATT?',
        'CH:CURR?', 'CH:BCURR?',
        # CURR simple
        'CURR:CC?',
        # Pattern set/value
        'CURR:SET?', 'CURR:VAL?', 'CURR:LEV?',
    ]

    print(f"\n--- Test de {len(candidates)} candidats ---\n")
    found = []
    for cmd in candidates:
        r = query(ser, cmd)
        is_err = not r or 'err' in r.lower()
        status = 'ERR' if is_err else 'OK'
        if not is_err:
            found.append((cmd, r))
            print(f"  *** {cmd} -> {r}")
        else:
            print(f"      {cmd} -> {r or '(vide)'}")
        time.sleep(DELAY)

    # Si rien trouvé, brute-force CURR:B** (2 lettres après B)
    if not found:
        print(f"\n--- Brute-force CURR:B + 2 lettres ---\n")
        import string
        for c1 in string.ascii_uppercase:
            for c2 in string.ascii_uppercase:
                cmd = f'CURR:B{c1}{c2}?'
                if cmd in ['CURR:BCC?']:  # déjà testé
                    continue
                r = query(ser, cmd)
                if r and 'err' not in r.lower():
                    found.append((cmd, r))
                    print(f"  *** {cmd} -> {r}")
                time.sleep(0.3)
            # Progress
            print(f"  ... CURR:B{c1}*")

    ser.close()

    print(f"\n=== RESULTATS ===")
    if found:
        for cmd, r in found:
            print(f"  {cmd} -> {r}")
    else:
        print("  Aucune commande trouvee.")

if __name__ == '__main__':
    main()
