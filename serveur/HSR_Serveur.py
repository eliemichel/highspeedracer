from socket import *
from _thread import start_new_thread
from time import clock, sleep
from queue import *
from Compresse import *

def debug(text) : print(text)

# --- --- --- #
host = ""     #
port = 3615   #
maxi = 8      #
# --- --- --- #

## Traiter ##
def traiter(cl, id):
	tps = clock()
	# Informations
	nom = "[Inconnu]"
	vaisseau = ""
	
	run = True
	while run :
		try :
			# Tentative de réception de données.
			data = cl.recv(1024)
		except :
			continue
		else :
			if not data == b'' :
				index = 0
				byte = data[index:(index+1)]
				info = b''
				# Recherche de l'info du paquet située avant l'opcode \x01.
				while not byte == b'\x01' :
					index += 1
					info += byte
					byte = data[index:(index+1)]
				data = load(data[(index+1):]) # Décompression du paquet
				
				# Analyse du paquet
				if info == b'\x00' : # Coupure du serveur
					msg = [b'\x0a',  "Coupure du serveur par " + nom]
					debug(msg[1])
					q.put(["message", msg])
					q.put(["FIN", "#"])
					break
				if info == b'\x01' : # Lancement du jeu
					msg = [b'\x42', "Partie lancée"]
					debug(msg[1])
					q.put(["message", msg])
				elif info == b'\x05' : # Le joueur quitte le jeu
					msg = [b'\x41',  nom + " a quitte HSR."]
					debug(msg[1])
					q.put(["FIN", cl])
					q.put(["message", msg])
					break
				elif info == b'\x11' : # Ping (paquet vide à retourner au joueur)
					cl.send(b'\x11\x01' + dump(0))
				elif info == b'\x21' : # Info : Nom
					nom = data
					q.put(["nom", nom, id])
					msg = [b'\x41', nom + " a rejoint HSR."]
					debug(msg[1])
					q.put(["message", msg])
				elif info == b'\x22' : # Info : Vaisseau
					vaisseau = data
					msg = [b'\x22',  [id, data]]
					#q.put(["ssr", msg, cl]) # Diffuser l'info aux precedents joueurs
					q.put(["vsx", vaisseau, id]) # S'enregistrer dans la liste pour les joueurs suivants
					#q.put(["info", "vsx", cl]) # Recuperer la liste des precedents joueurs
				elif info == b'\x3a' : # Ingame : Position/Rotation
					msg = [b'\x3a',  [id, data]]
					q.put(["ssr", msg, cl])
				elif info == b'\x51' : # Message
					msg = [b'\x51', [nom, data]]
					debug(msg)
					q.put(["message", msg])
				
## ##

## Diffuser ##
def diffuser(clients, msg) :
	paquet = msg[0] + b'\x01' + dump(msg[1])
	for c in clients :
		c.send(paquet)
## ##

## Diffuser sans retour ##
def diffuser_ssr(clients, cl, msg) :
	paquet = msg[0] + b'\x01' + dump(msg[1])
	for c in clients :
		if not cl == c :
			c.send(paquet)
## ##

# ---------- ---------- ---------- #

## Main ##
print("-- Serveur HSR --")
print("--       v3.2  --")

# Création de la socket
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(maxi)
sock.setblocking(False)

# Création des liens et listes
q = Queue()
retour = Queue()
clients = ()
id = 0
vaisseaux = {}
noms = {}

course = False # Si la course est lancee ou non
tps_lancement = clock() # Date du lancement du serveur
maxTps = 20 # Temps d'attente limite
maxJoueurs = maxi # Nombre maximum de joueurs

#@ sock blocking mode : OFF

run = True
while run :
	if not course :
		try :
			cl, addr = sock.accept()
		except : pass
		else :
			id += 1
			clients += (cl,)
			start_new_thread(traiter, (cl, id))
	
	try :
		ret = q.get(False)
	except : pass
	else :
		if ret[0] == "FIN" :
			if str(ret[1]) == "#" : break # On quitte le jeu
			else : # On retire un joueur
				oldClients = clients
				clients = ()
				for c in oldClients :
					if not c == ret[1] :
						clients += (c,)
		elif ret[0] == "message" :
			diffuser(clients, ret[1])
		elif ret[0] == "ssr" :
			diffuser_ssr(clients, ret[2], ret[1])
		elif ret[0] == "vsx" :
			vaisseaux[ret[2]] = ret[1]
		elif ret[0] == "nom" :
			noms[ret[2]] = ret[1]
		elif ret[0] == "GO" :
			# Diffusion des informations
			for id, nom in noms.items() :
				paquet = b'\x21\x01' + dump([id, nom])
				diffuser_ssr(clients, paquet)
			for id, vsx in vaisseaux.items() :
				paquet = b'\x22\x01' + dump([id, vsx])
				diffuser_ssr(clients, paquet)
			# Lancement de la course
			course = True
			msg = [b'\x42',  0]
			diffuser(clients, msg)
			print("---GO---")
			
		"""
		elif ret[0] == "info" :
			if ret[1] == "vsx" :
				debug("diff")
				for id, vsx in vaisseaux.items() :
					paquet = b'\x22\x01' + dump([id, vsx])
					ret[2].send(paquet)
		"""
	"""
	if ((clock() - tps_lancement > maxTps and len(clients) > 0) or id >= maxJoueurs) and not course :
		course = True
		msg = [b'\x42',  0]
		diffuser(clients, msg)
		print("---GO---")
	"""
	
sock.close()
for c in clients :
	c.close()
	
## ##
