from scapy.all import sniff

class PacketSniffer:
    def __init__(self, filter_str=""):
        self.filter_str = filter_str

    def packet_callback(self, packet):
        print(packet.summary())
        with open("packet_summary.txt", "a") as f:
            f.buffer.write("[+][+] {}\n".format(packet.summary()).encode("utf-8"))

    def start_sniffing(self):
        sniff(prn=self.packet_callback, filter=self.filter_str, store=0)
