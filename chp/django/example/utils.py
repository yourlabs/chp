from collections import UserList
from ipaddress import IPv4Address, IPv4Network


class IP_List(UserList):
    """ A list of IP networks that can be used for comparison.

    This class allows an IP address to be checked against a list of
    networks for Django's INTERNAL_IPS setting. (Django only
    ever needs to do "ip in INTERNAL_IPS" so `contains` is sufficient for
    this purpose.)

    For example, to make localhost and the entire block of 192.168.1.*
    considered to be internal, use::

        INTERNAL_IPS = IP_List(['127.0.0.1', '192.168.1.0/24'])
    """
    def __init__(self, *args):
        super().__init__([IPv4Network(arg) for arg in args])

    def __contains__(self, ip):
        ip = IPv4Address(ip)
        return any([(ip in addr) for addr in self])

    def __len__(self):
        return super().__len__()

    def __getitem__(self, i):
        return super().__getitem__(i)
