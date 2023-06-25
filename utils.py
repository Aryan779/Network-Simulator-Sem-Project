import ipaddress

from netaddr import IPNetwork

def get_network_addr(ip_address, subnet_mask="255.255.255.0"):
    ip = ipaddress.ip_interface(f"{ip_address}/{subnet_mask}")
    network_ip = ip.network.network_address
    return str(network_ip)

def check_subnet(ip1,ip2):
    """Checks If IP Exists In That Subnet."""
    # 225 = Broadcast Address, 0 = Network Address
    subnet = "255.255.0.0"
    if IPNetwork("{}/{}".format(ip1,subnet)) == IPNetwork("{}/{}".format(ip2,subnet)):
        return True
    return False

class packet:
    def __init__(self,num,dest_mac_addr=None,src_mac_addr=None,dest_ip_addr=None,src_ip_addr=None,data=None):
        self.num=num
        self.dest_mac_addr=dest_mac_addr
        self.src_mac_addr=src_mac_addr
        self.dest_ip_addr=dest_ip_addr
        self.src_ip_addr=src_ip_addr
        self.data=data
        print("packet structure: ",end="")
        print("dest mac_addr: ",self.dest_mac_addr," ","src mac_addr: ",self.src_mac_addr,end=" ")
        print("dest ip_addr: ",self.dest_ip_addr," ","src ip_addr: ",self.src_ip_addr,end=" ")
        print(data)
