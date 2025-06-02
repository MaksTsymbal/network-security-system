# scripts/make_pcap.py
from scapy.all import IP, TCP, Raw, wrpcap

# Генеруємо один HTTP GET з SQLi
pkt = IP(src="10.0.0.2", dst="192.168.0.1") / \
      TCP(sport=12345, dport=80) / \
      Raw(b"GET /?id=' OR 1=1-- HTTP/1.1\r\nHost: example.com\r\n\r\n")

wrpcap("suricata/pcaps/test_sqli.pcap", [pkt])
print("PCAP згенеровано: suricata/pcaps/test_sqli.pcap")