
NETWORKING &
THE OSI MODEL
A Complete Study Guide for Cyber Operations

Alex Rivera  |  Cyber Defense & Incident Response  |  2026

CONTENTS

Chapter 1  —  What is Networking?
          Goals, PAN / LAN / MAN / WAN
Chapter 2  —  IP Addresses Deep Dive
          Octets, Classes A–E, IPv4 vs IPv6, NAT & DHCP
Chapter 3  —  The OSI Model
          All 7 Layers, Protocols, Data Flow
Chapter 4  —  Key Protocols & Port Numbers
          TCP vs UDP, Essential Ports, DNS / DHCP / HTTP(S)
Chapter 5  —  Servers, Clients & Network Devices
          Roles, Routers, Switches, Firewalls
Chapter 6  —  Security Concepts
          CIA Triad, Common Attacks, Defence Tips

CHAPTER 1
What is Networking?

Networking is the practice of connecting devices so they can communicate and share resources. Without networking, every device would be an island — your laptop couldn't reach Google, your phone couldn't send a message, and your printer couldn't receive a document from across the room.

Goals of Networking
Share Resources — Files, printers, internet connections, all shared efficiently across devices.
Enable Communication — Email, messaging, VoIP calls, all rely on network protocols.
Remote Access — Access data stored on another machine, anywhere in the world.
Centralised Management — IT teams can manage hundreds of devices from a single location.

Types of Networks
Networks are categorised by the geographical area they cover. From your earphones to the entire planet, each type has a different scale and use case.



CHAPTER 2
IP Addresses Deep Dive

An IP (Internet Protocol) address is a unique numerical label assigned to every device on a network. Think of it as a postal address — without it, data packets would have no idea where to go.
Anatomy of an IP Address
An IPv4 address like 192.168.0.1 is made of four octets (8-bit numbers) separated by dots:


Total: 8 x 4 = 32 bits  ->  2^32 = approximately 4.3 billion unique addresses.

IP Address Classes
IPv4 addresses are divided into classes based on the value of the first octet. Each class serves a different scale of organisation:



IPv4 vs IPv6
IPv4's ~4.3 billion addresses seemed enormous in 1983, but with billions of IoT devices, it ran out. Enter IPv6:



DHCP — Automatic IP Assignment
DHCP (Dynamic Host Configuration Protocol) is the service inside your router that automatically hands out IP addresses. When your phone joins a Wi-Fi network, it broadcasts a request and DHCP replies with an available address — no manual configuration needed.
Dynamic IP — Assigned automatically by DHCP. May change each session. Good for everyday devices.
Static IP — Manually set. Never changes. Essential for servers, printers, and network cameras.

CHAPTER 3
The OSI Model
Open Systems Interconnection — the universal language of networking

The OSI model is a conceptual framework that describes how data travels from one device to another across a network. It breaks the journey into 7 distinct layers, each with a specific job.
When you hit Enter on a Google search, your data travels DOWN all 7 layers on your machine, across the network, then back UP the 7 layers on Google's servers.

The 7 Layers











CHAPTER 4
Key Protocols & Port Numbers

Protocols are agreed-upon rules that define how data is transmitted. Port numbers identify which specific service on a machine should receive the data.
TCP vs UDP
Both operate at OSI Layer 4 (Transport) but have very different philosophies:


Essential Port Numbers
Ports are virtual endpoints. Think of an IP address as a building and the port as the specific office number inside it.



CHAPTER 5
Servers, Clients & Network Devices

Server vs Client

Network Devices at a Glance

CHAPTER 6
Security Concepts

The CIA Triad
The three pillars of information security — every security decision maps back to at least one:


Common Network Attacks



"Security is not a product, but a process." — Bruce Schneier