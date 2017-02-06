#!/usr/bin/env python
"""
Gathers libvirt statistics for running instances and outputs
in a format that can be used with telegraf's exec plugin
"""
import json
import sys
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


def write_telegraf_line(data):
    """ Takes a dict and formats and prints the output in telegraf format """
    print json.dumps(data)


def get_cpu_stats(dom, conn):
    """ Collect CPU statistics """


def get_memory_stats(dom, conn):
    """ Collect memory statistics """


def get_network_stats(dom, conn):
    """ Collect network statistics """
    network_stats = {}
    vm = conn.lookupByID(dom)
    tree = ElementTree.fromstring(vm.XMLDesc())
    iface = tree.find('devices/interface/target').get('dev')
    tmp = vm.interfaceStats(iface)
    network_stats = dict([('instance name', str(vm.name())),
                         ('read bytes', str(tmp[0])),
                         ('read packets', str(tmp[1])),
                         ('read errors', str(tmp[2])),
                         ('read drops', str(tmp[3])),
                         ('write bytes', str(tmp[4])),
                         ('write packets', str(tmp[5])),
                         ('write errors', str(tmp[6])),
                         ('write drops', str(tmp[7]))])
    return network_stats


def get_stats(conn):
    """ Grabs list of domains and iterates over each one to gather stats """
    domains = conn.listDomainsID()
    for dom in domains:
        write_telegraf_line(get_network_stats(dom, conn))
    conn.close()
    exit(0)

if __name__ == "__main__":
    setup_connection()
# vi:ts=4 et:
