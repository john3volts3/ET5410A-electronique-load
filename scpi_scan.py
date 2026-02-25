"""
SCPI Brute-force scanner for ET5410A electronic load.
Usage: python scpi_scan.py [phase]
Phases:
  verify    — re-verify known BATT commands (BTC, BTE, CAPA, ENER, MODE)
  other_sub — try battery-related commands in other subsystems (TIME:, LOAD:, etc.)
  batt3     — continue 3-letter BATT: brute-force from BUA onwards (chunks of ~200)
  batt4     — systematic 4-letter BATT: scan with common prefixes

WARNING: Use long delays between commands — Asus USB chipset is fragile.
"""

import serial
import time
import sys
import string

PORT = 'COM3'
BAUD = 14400
TIMEOUT = 1.5
DELAY = 0.8
LOG_FILE = 'scpi_scan_results.log'

def scpi_query(ser, cmd):
    """Send a SCPI query and return the response (or None on timeout)."""
    ser.reset_input_buffer()
    ser.write((cmd + '\n').encode('ascii'))
    time.sleep(0.3)
    response = b''
    deadline = time.time() + TIMEOUT
    while time.time() < deadline:
        chunk = ser.read(ser.in_waiting or 1)
        if chunk:
            response += chunk
            if b'\n' in response:
                break
        else:
            time.sleep(0.05)
    text = response.decode('ascii', errors='replace').strip()
    return text if text else None

def run_scan(ser, cmds, phase_label, log):
    """Run a list of commands, return list of (cmd, response) for valid ones."""
    found = []
    log.write(f"\n--- {phase_label}: {time.strftime('%H:%M:%S')} ---\n")

    for i, cmd in enumerate(cmds, 1):
        show = (i <= 5 or i % 50 == 0 or i == len(cmds))
        if show:
            print(f"  [{i:4d}/{len(cmds)}] {cmd:22s} -> ", end='', flush=True)

        try:
            resp = scpi_query(ser, cmd)
        except Exception as e:
            msg = f"EXCEPTION: {e}"
            print(f"\n  [{i:4d}/{len(cmds)}] {cmd:22s} -> {msg}")
            log.write(f"  {cmd:22s} -> {msg}\n")
            log.flush()
            return found, True  # error flag

        is_valid = resp and 'cmd err' not in resp.lower()

        if is_valid:
            if not show:
                print(f"\n  [{i:4d}/{len(cmds)}] {cmd:22s} -> ", end='', flush=True)
            print(f"*** TROUVE: {resp} ***")
            log.write(f"  {cmd:22s} -> {resp}  <<<< FOUND\n")
            found.append((cmd, resp))
        else:
            if show:
                print(f"{'(timeout)' if not resp else resp}")
            log.write(f"  {cmd:22s} -> {resp or '(timeout)'}\n")

        log.flush()
        time.sleep(DELAY)

    return found, False

def main():
    phase = sys.argv[1] if len(sys.argv) > 1 else 'verify'

    if phase == 'verify':
        # Re-verify known commands
        cmds = ['BATT:MODE?', 'BATT:CAPA?', 'BATT:ENER?', 'BATT:BTC?', 'BATT:BTE?']

    elif phase == 'other_sub':
        # Try battery cutoff commands in OTHER subsystems
        cmds = []
        # TIME: subsystem — battery time cutoff?
        time_suffixes = ['BATT', 'BAT', 'CUT', 'CUTB', 'DISC', 'BCAP', 'BVOL',
                         'BENT', 'BTIM', 'BCC', 'BCR', 'BC', 'BD', 'BE', 'BT']
        cmds += [f'TIME:{s}?' for s in time_suffixes]
        # LOAD: subsystem
        load_suffixes = ['BATT', 'BAT', 'CUT', 'CUTM', 'STOP', 'STOM', 'TERM',
                         'BTC', 'BTE', 'BTT', 'BTV', 'DISC', 'DMOD']
        cmds += [f'LOAD:{s}?' for s in load_suffixes]
        # SYSSet: subsystem
        cmds += [f'SYSSET:{s}?' for s in ['BATT', 'BAT', 'BTC', 'BTE', 'CUTM']]
        # VOLT: subsystem (battery voltage cutoff)
        volt_suffixes = ['BAT', 'BATT', 'DISC', 'CUT', 'CUTB', 'BC', 'BD', 'BT']
        cmds += [f'VOLT:{s}?' for s in volt_suffixes]
        # CURR: subsystem
        cmds += [f'CURR:{s}?' for s in ['BAT', 'BATT', 'CUT', 'DISC', 'BC', 'BD']]
        # Try colons: BATT:BT:C? style (subcommand levels)
        cmds += ['BATT:BT:C?', 'BATT:BT:E?', 'BATT:BT:T?', 'BATT:BT:V?', 'BATT:BT:M?']
        # Try BATT commands with longer names (5+ letters)
        cmds += ['BATT:TIMER?', 'BATT:ENERGY?', 'BATT:CAPAC?', 'BATT:VOLTA?',
                 'BATT:CUTOFF?', 'BATT:STOPM?', 'BATT:ENDMOD?', 'BATT:DISCHA?']

    elif phase == 'batt3':
        # Continue 3-letter BATT: scan from BUA
        # Chunk: provide start as 2nd arg, e.g. "batt3 BUA" or "batt3 DAA"
        start = sys.argv[2] if len(sys.argv) > 2 else 'BUA'
        letters = string.ascii_uppercase
        cmds = []
        started = False
        for a in letters:
            for b in letters:
                for c in letters:
                    combo = a + b + c
                    if not started:
                        if combo == start:
                            started = True
                        else:
                            continue
                    cmds.append(f'BATT:{combo}?')
                    if len(cmds) >= 300:  # chunk size ~5 min
                        break
                if len(cmds) >= 300:
                    break
            if len(cmds) >= 300:
                break
        if cmds:
            last_combo = cmds[-1].replace('BATT:', '').replace('?', '')
            print(f"  (3-letter range: {start} to {last_combo})")

    elif phase == 'batt4':
        # Targeted 4-letter BATT: scan with common starting letters
        letters = string.ascii_uppercase
        prefixes_2 = ['CA', 'CO', 'CU', 'CH', 'DI', 'DC', 'DM', 'EN', 'EL',
                       'MO', 'MA', 'ST', 'SE', 'TI', 'TM', 'VO', 'VA', 'RA',
                       'RE', 'PO', 'PA', 'LI', 'LO', 'BA', 'BC', 'BD', 'BE',
                       'BT', 'OV', 'OC', 'OP', 'OT']
        cmds = []
        for p in prefixes_2:
            for c in letters:
                for d in letters:
                    cmds.append(f'BATT:{p}{c}{d}?')
        # That's 32 * 676 = 21,632... way too many
        # Instead: just scan first 2 letters for 4-letter, then full 26*26
        # Actually let's just do the most likely 4-letter combos more carefully
        # Use common word patterns
        cmds = []
        four_letter_words = [
            # Time
            'TIME', 'TIMS', 'TIMV', 'TIML', 'TVAL', 'TOUT',
            # Voltage
            'VOLT', 'VCUT', 'VMIN', 'VMAX', 'VLIM', 'VBAT', 'VEND',
            # Current
            'CURR', 'IMAX', 'IMIN', 'ILIM', 'IVAL',
            # Energy
            'ENER', 'ECUT', 'ELIM', 'EVAL', 'EMAX',
            # Capacity
            'CAPA', 'CCUT', 'CLIM', 'CVAL', 'CMAX',
            # Stop/cutoff/end
            'STOP', 'CUTS', 'COFF', 'COFM', 'CUTM', 'CUTT', 'CUTE',
            'CUTC', 'CUTV', 'ENDL', 'ENDM', 'ENDT', 'ENDV', 'ENDE',
            'ENDC', 'TERM', 'TRMD', 'STMD', 'STPV', 'STPE', 'STPC',
            'STPT', 'SHDN',
            # Mode/status
            'MODE', 'STAT', 'TYPE', 'DMOD', 'CMOD', 'SMOD', 'TMOD',
            'BMOD', 'RMOD',
            # Discharge
            'DISC', 'DCHG', 'DCHR', 'DBAT',
            # Protection/limit
            'PROT', 'PLIM', 'PLEV', 'OVER', 'OLIM',
            # Run/state
            'RUNS', 'RUNT', 'AUTO', 'LOOP', 'CYCL', 'COUN',
        ]
        cmds = [f'BATT:{w}?' for w in four_letter_words]

    else:
        print("Phases: verify, other_sub, batt3, batt4")
        sys.exit(1)

    print(f"=== ET5410A SCPI Scanner — phase: {phase} ===")
    print(f"Port: {PORT} @ {BAUD} bps, {len(cmds)} commands")
    print(f"Estimated: ~{len(cmds) * (DELAY + 0.5) / 60:.1f} min")
    print()

    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        time.sleep(0.5)
    except Exception as e:
        print(f"ERREUR: impossible d'ouvrir {PORT}: {e}")
        sys.exit(1)

    print("Verification (*IDN?)...")
    idn = scpi_query(ser, '*IDN?')
    if idn:
        print(f"  OK: {idn}\n")
    else:
        print("  ERREUR: pas de reponse — verifier port/baud")
        ser.close()
        sys.exit(1)
    time.sleep(DELAY)

    with open(LOG_FILE, 'a') as log:
        log.write(f"\n{'='*60}\n")
        log.write(f"Phase: {phase} — {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"IDN: {idn}\n")
        log.write(f"{'='*60}\n")

        found, had_error = run_scan(ser, cmds, phase, log)

    ser.close()

    print(f"\n=== Resultats phase '{phase}' ===")
    print(f"Commandes valides: {len(found)}")
    for cmd, resp in found:
        print(f"  {cmd:22s} -> {resp}")
    if not found:
        print("  (aucune)")
    if had_error:
        print("  ATTENTION: scan interrompu par une erreur")
    print(f"Log: {LOG_FILE}")

if __name__ == '__main__':
    main()
