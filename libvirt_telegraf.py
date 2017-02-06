#!/usr/bin/env python
"""
Gathers libvirt statistics for running instances and outputs
in a format that can be used with telegraf's exec plugin
"""
from xml.etree import ElementTree
import libvirt

LIBVIRT_CONN = 'qemu:///system'


def setup_connection():
    """ Initiates a connection and if successful starts stats gathering """
    try:
        conn = libvirt.openReadOnly(LIBVIRT_CONN)
    except OSError:
        print('Failed to open libvirt connection:', LIBVIRT_CONN)
    else:
        get_stats(conn)


def write_telegraf_line(conn, dom, data):
    """ Takes a dict and formats and prints the output in telegraf format """
    virt_machine = conn.lookupByID(dom)
    line = ''.join("{}={}i,".format(key, val) for key, val in data.items())
    line = line[:-1]
    print 'libvirt,instance={} {}'.format(virt_machine.name(), line)


def get_network_stats(conn, dom):
    """ Collect network statistics """
    network_stats = {}
    virt_machine = conn.lookupByID(dom)
    tree = ElementTree.fromstring(virt_machine.XMLDesc())
    iface = tree.find('devices/interface/target').get('dev')
    tmp = virt_machine.interfaceStats(iface)
    network_stats = dict([('read_bytes', str(tmp[0])),
                          ('read_packets', str(tmp[1])),
                          ('read_errors', str(tmp[2])),
                          ('read_drops', str(tmp[3])),
                          ('write_bytes', str(tmp[4])),
                          ('write_packets', str(tmp[5])),
                          ('write_errors', str(tmp[6])),
                          ('write_drops', str(tmp[7]))])
    return network_stats


def get_stats(conn):
    """ Grabs list of domains and iterates over each one to gather stats """
    domains = conn.listDomainsID()
    for dom in domains:
        write_telegraf_line(conn, dom, get_network_stats(conn, dom))
    conn.close()
    exit(0)

if __name__ == "__main__":
    setup_connection()
# vi:ts=4 et:
