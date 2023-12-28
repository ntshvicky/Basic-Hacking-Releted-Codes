from scapy.all import Ether, ARP, srp, conf
import sys
import time

def arp_scan(iface, ip_range):
    print("[+] Scanning ", ip_range)
    curr_time = time.time()
    print("[+] Scanning started at: ", time.ctime(curr_time))
    conf.verb = 0
    broadcast = "ff:ff:ff:ff:ff:ff"
    ether_layer = Ether(dst=broadcast)
    arp_layer = ARP(pdst=ip_range)

    packet = ether_layer / arp_layer

    ans, unans = srp(packet, iface=iface, timeout=2, inter=0.1, verbose=False)

    for snd, rcv in ans:
        #if rcv[ARP].op == 2:
        print("[+] ", rcv[ARP].psrc, "is at ", rcv[ARP].hwsrc)
    
    duration = time.time() - curr_time
    print("[+] Scanning finished at: ", time.ctime(duration))

# scanner.py eth0 192.168.1.100/24
if __name__ == "__main__":
    if len(sys.argv)!= 3:
        print("Usage: sudo python3 scanner.py eth0 217.165.4.64/24")
    else:
        arp_scan(sys.argv[1], sys.argv[2])

