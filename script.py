import dpkt
from datetime import datetime


def parse_pcap(pcap_obj):
    for ts, pkt in pcap_obj:
        # eth = dpkt.ethernet.Ethernet(pkt)
        # #if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
        # #    continue
        # ip = eth.data
        # if ip.p == dpkt.ip.IP_PROTO_TCP:
        #     print("Le paquet est un paquet TCP")
        print('Hello')
        print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))


def main():
    pcap_pathname = '/home/pierre/Documents/Projet_ELE8704/pcap/HangoutWIFI.pcap'
    pcap_file = open(pcap_pathname, 'r')
    pcap_obj = dpkt.pcap.Reader(pcap_file)
    print('Beginning parsing...')
    parse_pcap(pcap_obj)


if __name__ == '__main__':
    main()