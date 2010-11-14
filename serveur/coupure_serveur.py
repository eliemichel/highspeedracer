from socket import *
from time import clock, sleep
from Compresse import *

host = gethostname()
port = 3615
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((host, port))


paquet = b'\x21\x01' + dump("Admin")
sock.send(paquet)

sleep(0.3)

paquet = b'\x00\x01' + dump(0)
sock.send(paquet)


print("FIN")
sleep(0.3)

sock.close()
