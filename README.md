# ARP-Spoofy

An ARP spoofing tool

Set up a MITM hack by temporarily switching a target IP's MAC address with a gateway's MAC address

Based on Zaid Sabih's tutorial in <https://www.udemy.com/course/learn-python-and-ethical-hacking-from-scratch>

## Table of Contents

[Requirements](##Requirements)  
[Installation](##Installation)  
[Configuration](##Configuration)  
[Execution](##Execution)  
[Contribution](##Contribution)  

## Requirements

- Python 3

- Pip and the `scapy` library

- a target IP and gateway IP

## Installation

```bash
git clone https://github.com/abraidotti/ARP-Spoofy
cd ARP-Spoofy
```

## Configuration

None

## Execution

Make sure to specify valid IPv4 addresses

```bash
python3 arp-spoofy.py --target 192.168.0.1 --gateway 192.168.0.1
```

## Contribution

If you'd like to contribute, file a pull request or github issue to discuss.

TODO:

- add automatic gateway IP recognition
