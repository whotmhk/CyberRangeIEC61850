#############################################################################
# This is for MSSD Project Student ID 1007386
# Reference Credit -Source GooseStalker
############################################################################ 
import os, sys, datetime, inspect, logging
from pyasn1.codec.ber import decoder
from pyasn1.type import tag
from pyasn1.type import univ

# Setup the logger
current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f'goose_dataset_{current_time}.log'
logging.basicConfig(level=logging.INFO, handlers=[
    logging.FileHandler(log_filename),
    logging.StreamHandler(sys.stdout)
], format='%(asctime)s - Dataset - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Update system path to include the Goose module directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from scapy.layers.l2 import Ether, Dot1Q
from scapy.all import rdpcap
from goose.goose import GOOSE, GOOSEPDU
from goose.goose_pdu import IECGoosePDU

DEBUG = 0   # 0: off, 1: Show Goose Payload, 2: Full Debug

# Ask user to input the PCAP file name
logging.info("Please enter the name of the PCAP file:")
inf = input()
packets = rdpcap(inf)
logging.info("Total packets read: {}".format(len(packets)))

if not packets:
    logging.warning("No packets found in the file.")
else:
    goose_packets_found = 0

    GOOSE_TYPE = 0x88b8
    def gooseTest(pkt):
        isGoose = False
        if pkt.haslayer(Dot1Q):
            if pkt[Dot1Q].type == GOOSE_TYPE:
                isGoose = True
        if pkt.haslayer(Ether):
            if pkt[Ether].type == GOOSE_TYPE:
                isGoose = True
        return isGoose

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

    datasets = {}
    for p in packets:
        if gooseTest(p):
            logging.info("GOOSE packet found!")
            goose_packets_found += 1
            d = GOOSE(p.load)
            gpdu = d[GOOSEPDU].original
            gd = goose_pdu_decode(gpdu)
            src_mac = p[Ether].src
            gocbref = str(gd['gocbRef'])
            dataset = str(gd['datSet'])
            goid = str(gd['goID'])
            numDatSetEntries = int(gd['numDatSetEntries'])
            godata = f'{gocbref} - {dataset} - {goid} - {numDatSetEntries}'
            if src_mac in datasets:
                if godata not in datasets[src_mac]:
                    datasets[src_mac].append(godata)
            else:
                datasets[src_mac] = [godata]
        else:
            logging.info("Non-GOOSE packet or no recognizable GOOSE layer found.")

    logging.info("GOOSE packets found: {}".format(goose_packets_found))
    if goose_packets_found == 0:
        logging.warning("No GOOSE packets found. Check if the PCAP file contains GOOSE data or review the 'gooseTest' function.")

    logging.info('Goose Data by Device Hardware Address')
    indent = '    '
    for src in datasets:
        logging.info(f'Source Device: {src}')
        for e in datasets[src]:
            logging.info(f'{indent}{e}')
