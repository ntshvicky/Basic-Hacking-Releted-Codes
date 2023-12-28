import threading
from domain_ip_info import DomainIPInfo
from ip import IPLocation
from mac import Mac_changer
import uuid

from packet_sniffer import PacketSniffer

def get_mac_address2():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[i:i+2] for i in range(0, 11, 2)])

def executePacketSnifferBg():
    sniffer = PacketSniffer(filter_str="")
    sniffer.start_sniffing()

if __name__ == "__main__":
    #by interface
    mac_changer = Mac_changer()
    mc = mac_changer.get_mac_address("en4")
    print(mc)
    print("============================")

    #by uuid
    print(get_mac_address2())
    print("============================")

    # Usage:
    ip_location = IPLocation()
    location_data = ip_location.get_location()
    print(location_data)
    print("============================")

    print("Run packet sniffer in background")
    
    thread = threading.Thread(target=executePacketSnifferBg)
    thread.start()

    print("============================")

    domain_ip_info = DomainIPInfo("google.com")
    general_info = domain_ip_info.get_general_info()
    whois_info = domain_ip_info.get_whois_info()

    print("General Information:")
    print(general_info)

    print("\nWHOIS Information:")
    print(whois_info)


    print("Done")

    