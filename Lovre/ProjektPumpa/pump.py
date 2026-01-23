#!/usr/bin/env python3
import sys
import time
from pysnmp.hlapi import *

# SNMP postavke relejske pločice
RELAY_BOARD_IP = "172.16.100.2"
COMMUNITY = "private"
RELAY_OID = "1.3.6.1.4.1.19865.1.2.2.1.0"  # P5.1

# Kalibracija pumpe (izmjeri stvarno!)
FLOW_L_PER_MIN = 2.5

def set_relay(state):
    next(
        setCmd(
            SnmpEngine(),
            CommunityData(COMMUNITY, mpModel=0),  # SNMP v1
            UdpTransportTarget((RELAY_BOARD_IP, 161), timeout=1, retries=3),
            ContextData(),
            ObjectType(ObjectIdentity(RELAY_OID), Integer(state))
        )
    )

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
