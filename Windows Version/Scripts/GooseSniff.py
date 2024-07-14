######################################################################################################
# This is for MSSD Project Student ID 1007386
# Reference : Goose Stalker
######################################################################################################




import datetime
import psutil
import socket
from scapy.all import sniff, PcapWriter

class GooseSniffer:
    def __init__(self, interface):
        self.interface = interface

    def sniff_goose(self, timeout=60):
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"capture_{current_time}.pcap"
        print(f"Sniffing GOOSE traffic on {self.interface} for {timeout} seconds...")
        
        try:
            # Adjusting filter to capture all GOOSE traffic
            filter_expr = "ether proto 0x88b8"
            traffic = sniff(iface=self.interface, timeout=timeout, filter=filter_expr)
            if traffic:
                print(f"Captured {len(traffic)} packets with filter.")
                for pkt in traffic:
                    print(pkt.summary())
                pcap_file = file_name
                PcapWriter(pcap_file, append=True, sync=True).write(traffic)
                print(f"File saved as: {pcap_file}")
            else:
                print("No traffic captured with filter. Trying without filter...")
                traffic = sniff(iface=self.interface, timeout=timeout)
                if traffic:
                    print(f"Captured {len(traffic)} packets without filter.")
                    for pkt in traffic:
                        print(pkt.summary())
                    pcap_file = file_name
                    PcapWriter(pcap_file, append=True, sync=True).write(traffic)
                    print(f"File saved as: {pcap_file}")
                else:
                    print("No traffic captured without filter.")
        except Exception as e:
            print(f"An error occurred while sniffing: {e}")

def list_interfaces():
    interfaces = psutil.net_if_addrs()
    interface_list = []
    for i, (iface, addrs) in enumerate(interfaces.items()):
        mac = ip = None
        for addr in addrs:
            if addr.family == socket.AF_LINK:
                mac = addr.address
            elif addr.family == socket.AF_INET:
                ip = addr.address
        interface_list.append((iface, mac, ip))
        print(f"{i}: {iface} - MAC: {mac}, IP: {ip}")
    return interface_list

if __name__ == "__main__":
    try:
        print("Available network interfaces:")
        interfaces = list_interfaces()
        
        choice = input("Enter the **number** corresponding to the network interface you want to use: ")
        interface = interfaces[int(choice)][0]
        print(f"Selected interface: {interface}")
        sniffer = GooseSniffer(interface)
        sniffer.sniff_goose(60)
    except ValueError:
        print("Invalid input. Please enter a number from the list.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("Press Enter to exit...")
