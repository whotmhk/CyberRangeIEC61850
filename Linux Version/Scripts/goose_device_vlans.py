#############################################################################
# This is for MSSD project Student ID 1007386
# Reference Credit - Source Goosestalker
############################################################################
import os, sys, datetime, inspect, logging
from pyasn1.codec.ber import decoder
from pyasn1.type import tag
from pyasn1.type import univ

# Setup logging to both file and console
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f'goose_VLANoutput_{current_time}.log'
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler(log_filename),
    logging.StreamHandler(sys.stdout)
], format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Update system path to include the Goose module directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from scapy.layers.l2 import Ether, Dot1Q
from scapy.all import rdpcap
from goose.goose import GOOSE, GOOSEPDU
from goose.goose_pdu import IECGoosePDU

# Global Variables for Debugging
DEBUG = 0   # 0: off, 1: Show Goose Payload, 2: Full Debug

# Requesting user input for the PCAP file
logging.info("Please enter the name of the PCAP file:")
inf = input()
try:
    packets = rdpcap(inf)
    logging.info(f"Total packets read: {len(packets)}")
except Exception as e:
    logging.error(f"Failed to read PCAP file: {e}")
    sys.exit(1)

# Define GOOSE type constant
GOOSE_TYPE = 0x88b8

# Function to check if a packet is a GOOSE packet
def gooseTest(pkt):
    isGoose = False
    if pkt.haslayer(Dot1Q):
        if pkt[Dot1Q].type == GOOSE_TYPE:
            isGoose = True
    if pkt.haslayer(Ether):
        if pkt[Ether].type == GOOSE_TYPE:
            isGoose = True
    return isGoose

# Function to decode GOOSE PDU using pyasn1
def goose_pdu_decode(encoded_data):
    if DEBUG > 2:
        from pyasn1 import debug
        debug.setLogger(debug.Debug('all'))
    g = IECGoosePDU().subtype(
        implicitTag=tag.Tag(
            tag.tagClassApplication,
            tag.tagFormatConstructed,
            1
        )
    )
    decoded_data, unprocessed_trail = decoder.decode(encoded_data, asn1Spec=g)
    return decoded_data

# Process packets and search for GOOSE
vlans = {}
goose_packets_count = 0
for p in packets:
    if gooseTest(p):
        goose_packets_count += 1
        d = GOOSE(p.load)
        gpdu = d[GOOSEPDU].original
        gd = goose_pdu_decode(gpdu)
        gocbRef = str(gd['gocbRef'])
        src_mac = p[Ether].src
        dst_mac = p[Ether].dst
        device = f'{src_mac} - {gocbRef}'
        if p.haslayer(Dot1Q):
            pvlan = p[Dot1Q].vlan
            prio = p[Dot1Q].prio
            if pvlan not in vlans:
                vlans[pvlan] = {'src': [device], 'dst': [dst_mac], 'prio': [prio]}
            else:
                if device not in vlans[pvlan]['src']:
                    vlans[pvlan]['src'].append(device)
                if dst_mac not in vlans[pvlan]['dst']:
                    vlans[pvlan]['dst'].append(dst_mac)
                if prio not in vlans[pvlan]['prio']:
                    vlans[pvlan]['prio'].append(prio)
    else:
        logging.info("Non-GOOSE packet detected.")

# Output results
logging.info(f"GOOSE packets processed: {goose_packets_count}")
if not vlans:
    logging.error('ERROR: No VLANs with GOOSE packets found in the PCAP.')
else:
    logging.info('Goose VLANS by Device Hardware Address')
    indent = '    '
    for vid in vlans:
        logging.info(f'VLAN ID: {vid} has Priorities: {", ".join(map(str, vlans[vid]["prio"]))}')
        logging.info(f'{indent}Source Devices:')
        for s in vlans[vid]['src']:
            logging.info(f'{indent*2}{s}')
        logging.info(f'{indent}Multicast Addresses:')
        for d in vlans[vid]['dst']:
            logging.info(f'{indent*2}{d}')
