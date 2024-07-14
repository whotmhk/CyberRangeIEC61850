#############################################################################
# This is for MSSD Project Student ID 1007386
# Reference Goosestalker
############################################################################
import datetime
from scapy.all import sniff, PcapWriter

class GooseSniffer:
    def __init__(self, interface):
        self.interface = interface

    def sniff_goose(self, timeout=60):
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"capture_{current_time}.pcap"
        print(f"Sniffing GOOSE traffic on {self.interface} for {timeout} seconds...")
        traffic = sniff(iface=self.interface, timeout=timeout, filter="ether proto 0x88b8")
        pcap_file = file_name
        PcapWriter(pcap_file, append=True, sync=True).write(traffic)
        print(f"File saved as: {pcap_file}")

if __name__ == "__main__":
    interface = input("Enter the network interface name (e.g., eth0): ")
    sniffer = GooseSniffer(interface)
    sniffer.sniff_goose(60)
