from scapy.all import Ether, ARP, srp1
#srp layer2
import ipaddress
import netifaces
import pprint
from socket import gaierror
import os

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

def exists_in_path(cmd):
  assert not os.path.dirname(cmd)

  extensions = os.environ.get("PATHEXT", "").split(os.pathsep)
  for directory in os.environ.get("PATH", "").split(os.pathsep):
    base = os.path.join(directory, cmd)
    options = [base] + [(base + ext) for ext in extensions]
    for filename in options:
      if os.path.exists(filename):
        return True
  return False


if exists_in_path('nbtscan'):
    from subprocess import check_output
    def queryNBName(ip):
        try:
            out = check_output("nbtscan  -t 10 -s : {}".format(ip), shell=True)
            return out.split(':')[1].strip()
        except IndexError:
            return None


else:
    def queryNBName(ip):
        raise NotImplementedError()


queryNBName('1.1.1.1')

