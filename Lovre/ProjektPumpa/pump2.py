#!/usr/bin/env python3
import sys
import time
import subprocess

RELAY_BOARD_IP = "172.16.100.2"
COMMUNITY = "private"
RELAY_OID = "1.3.6.1.4.1.19865.1.2.2.1.0"  # P5.1

FLOW_L_PER_MIN = 2.5  # kalibriraj!

def set_relay(state):
    cmd = [
        "snmpset",
        "-v1",
        "-c", COMMUNITY,
        RELAY_BOARD_IP,
        RELAY_OID,
        "i", str(state)
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

def main():
    if len(sys.argv) != 2:
        print("Usage: pump.py <liters>")
        sys.exit(1)

    liters = float(sys.argv[1])
    seconds = (liters / FLOW_L_PER_MIN) * 60

    print(f"Pump ON for {seconds:.1f}s ({liters} L)")
    set_relay(1)
    time.sleep(seconds)
    set_relay(0)
    print("Pump OFF")

if __name__ == "__main__":
    main()
