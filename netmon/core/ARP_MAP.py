from scapy.all import Ether, ARP, srp1
#srp layer2
import ipaddress
import netifaces
import pprint
from socket import gaierror
from nmb.NetBIOS import NetBIOS


def ARPRequest(ipaddr, timeout=0.1):
    ether=Ether(dst="ff:ff:ff:ff:ff:ff")
    arp=ARP(pdst=ipaddr)
    ans = srp1(ether/arp,timeout=timeout, verbose=False)
    if not ans:
        return None
    return ans.src

def do_nothing(*args, **kwargs):
    pass


def ARPMapNetwork(network,
                  timeout=0.1):

    for ip in network:
        mac = ARPRequest(str(ip), timeout)
        if not mac:
            yield ip
        if mac:
            yield (ip, mac)


def get_iface_network(iface):
    loc = netifaces.ifaddresses(iface)[2]
    ipadd = loc[0]["broadcast"]
    mask = loc[0]["netmask"]
    anded = list()
    for ip, m in zip(ipadd.split('.'),mask.split('.')):
       anded.append(str(int(ip) & int(m)))
    subnet = '.'.join(anded)
    nm = get_nm(ipaddress.ip_address(unicode(mask)))
    return ipaddress.ip_network(unicode("{}/{}".format(subnet, nm)))



def get_nm(nm):
    c = 0
    for l in nm.packed:
         c+="{0:b}".format((ord(l))).count('1')
    return c



