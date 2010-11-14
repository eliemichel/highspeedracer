# ---------- ---------- ---------- #
#    Emulation de Pickle           #
#      Un equivalent existe en C++ # -> WIP
#                                  #
# **Creation pour le projet HSR**  #
# ---------- ---------- ---------- #
#   Ce fichier, comme tous les     #
# fichiers du projet HSR, est sous #
#      license CC BY-SA            #
# ---------- ---------- ---------- #

## Variables globales ##
VERSION = b'\x80' # Compatible avec Pickle -> Utiliser des chiffres eleves pour faire comprendre a Pickle que ce n'est pas la meme version.
TYPE = b'\x10'
TYPE_DICT = b'\x11'
TYPE_TPL = b'\x12'
TYPE_LIST = b'\x13'
TYPE_STR = b'\x14'
TYPE_INT = b'\x15'
TYPE_FLOAT = b'\x16'
STOP = b'\x01'
FIN = b'\x00'
obj = 'NULL'


## Types ##
types = {}
types['dict'] = type({})
types['tpl'] = type(())
types['list'] = type([])
types['str'] = type("")
types['int'] = type(0)
types['float'] = type(0.0)

# ---------- ---------- ---------- #
# ----------    DUMP    ---------- #
# ---------- ---------- ---------- #

def dump_obj(obj) :
	pass
def dump_dict(dict) :
	pass
def dump_tpl(tpl) :
	pass
def dump_list(list) :
	pass
def dump_str(str) :
	pass
def dump_int(int) :
	pass
def dump_float(float) :
	pass

def dump(obj) :
	"""Compresse un objet avec l'algo 1.0"""
	byte = b''
	byte += VERSION + b'\x10' # Version 1.0
	
	byte += dump_obj(obj)
	
	byte += FIN
	
	return byte


def dump_obj(obj) :
	"""Compresse un objet"""
	byte = b''
	if type(obj) == types['dict'] :
		byte += dump_dict(obj)
	elif type(obj) == types['tpl'] :
		byte += dump_tpl(obj)
	elif type(obj) == types['list'] :
		byte += dump_list(obj)
	elif type(obj) == types['str'] :
		byte += dump_str(obj)
	elif type(obj) == types['int'] :
		byte += dump_int(obj)
	elif type(obj) == types['float'] :
		byte += dump_float(obj)
		
	return byte

def dump_dict(dict) :
	"""Compresse un dictionnaire"""
	byte = b''
	byte += TYPE + TYPE_DICT
	for clef, contenu in dict.items() :
		byte += dump_str(clef)
		byte += dump_obj(contenu)
	byte += STOP + TYPE_DICT
	return byte

def dump_tpl(tpl) :
	"""Compresse un tuple"""
	byte = b''
	byte += TYPE + TYPE_TPL
	for contenu in tpl :
		byte += dump_obj(contenu)
	byte += STOP + TYPE_TPL
	return byte

def dump_list(list) :
	"""Compresse une liste"""
	byte = b''
	byte += TYPE + TYPE_LIST
	for contenu in list :
		byte += dump_obj(contenu)
	byte += STOP + TYPE_LIST
	return byte

def dump_str(str) :
	"""Compresse une chaine de caracteres"""
	byte = b''
	byte += TYPE + TYPE_STR
	byte += bytearray(str, "utf-8")
	byte += STOP + TYPE_STR
	return byte

def dump_int(int) :
	"""Compresse un nombre entier"""
	byte = b''
	byte += TYPE + TYPE_INT
	byte += bytearray(str(int), "utf-8")
	byte += STOP + TYPE_INT
	return byte

def dump_float(float) :
	"""Compresse un nombre a virgule flottante"""
	byte = b''
	byte += TYPE + TYPE_FLOAT
	byte += bytearray(str(float), "utf-8")
	byte += STOP + TYPE_FLOAT
	return byte


# ---------- ---------- ---------- #
# ----------    LOAD    ---------- #
# ---------- ---------- ---------- #

def load_obj(byte) :
	pass
def load_dict(byte) :
	pass
def load_tpl(byte) :
	pass
def load_list(byte) :
	pass
def load_str(byte) :
	pass
def load_int(byte) :
	pass
def load_float(byte) :
	pass


def load(byte) :
	"""Decompresse un objet"""
	fin = 0
	for b in byte :
		if b == FIN[0] :
			break
		else :
			fin += 1
	byte = byte[0:fin]
	
	proto = byte[0:2]
	byte = byte[2:]
	if(proto[0:1] == VERSION) : # Si le premier caractere est bien l'informateur de version
		if(not proto[1:2] == b'\x10') : # Version 1.0
			print("Compresse.load(byte) : protocole illisible par la fonction.")
			raise AttributeError
	else : # Sinon, on provoque une erreur
		print(byte)
		print("Compresse.load(byte) : attribut errone, impossible de lire le protocole.")
		print(AttributeError)
	
	obj = load_obj(byte)
	
	return obj[0]

def load_obj(byte) :
	"""Decompresse un objet"""
	
	# On recherche la balise de debut d'objet
	debut = 0
	for b in byte :
		if b == TYPE[0] : # Si c'est une balise de debut d'objet...
			break # On arrete la recherche
		else : # Sinon...
			debut += 1 # On passe au caractere suivant
	byte = byte[debut:] # On ne garde que le contenu
	
	proto = byte[0:2] # On recupere le prototype de l'objet : balise de type + type
	byte = byte[2:] # On retire le prototype de la liste de bytes
	type = proto[1:2] # On recupere le type : deuxieme caractere du prototype
	
	# On recherche la balise de fin correspondant au meme objet
	# Cette balise doit avoir le meme type que la balise de debut et ne doit pas etre contenue dans l'objet.
	# On compte donc le nombre d'objet imbriques
	contenus_ouverts = 0
	fin = 0
	for b in byte :
		if b == TYPE[0] : contenus_ouverts += 1 # Si on trouve une balise d'ouverture, on entre dans un nouveau contnu imbrique
		if b == STOP[0] : # Si c'est une balise de fin...
			if byte[fin + 1] == type[0] and contenus_ouverts <= 0 : # Et si le type correspond et et que l'on est pas dans le contenu de l'objet...
				break # On arrete la recherche
			else : # Sinon
				contenus_ouverts -= 1 # On sort du contenu imbrique
		fin += 1 # On passe au caractere suivant
	byte = byte[0:fin] # On ne garde que le contenu
	
	# On decompresse en fonction du type
	if type == TYPE_DICT :
		obj = load_dict(byte)
	elif type == TYPE_TPL :
		obj = load_tpl(byte)
	elif type == TYPE_LIST :
		obj = load_list(byte)
	elif type == TYPE_STR :
		obj = load_str(byte)
	elif type == TYPE_INT :
		obj = load_int(byte)
	elif type == TYPE_FLOAT :
		obj = load_float(byte)
	
	return [obj, debut, fin]

def load_dict(byte) :
	"""Decompresse un dictionnaire"""
	obj = {}
	
	while not byte == b'' :
		clef = None
		while not type(clef) == types['str'] : # On recherche jusqu'a ce que l'on trouve une chaine de caracteres
			retour = load_obj(byte) # On charge la clef
			clef = retour[0]
			debut = retour[1]
			fin = retour[2]
		byte = byte[debut+fin+4:] # On retire la clef
		
		retour = load_obj(byte) # On charge le contenu
		contenu = retour[0]
		debut = retour[1]
		fin = retour[2]
		byte = byte[debut+fin+4:] # On retire le contenu
		
		obj[clef] = contenu # On assigne le contenu a la clef
	
	return obj

def load_tpl(byte) :
	"""Decompresse un tuple"""
	obj = ()
	
	while not byte == b'' :
		retour = load_obj(byte) # On charge le contenu
		contenu = retour[0]
		debut = retour[1]
		fin = retour[2]
		byte = byte[debut+fin+4:] # On retire le contenu
		
		obj += (contenu,) # On ajoute le contenu au tuple
	
	return obj

def load_list(byte) :
	"""Decompresse une liste"""
	obj = []
	
	while not byte == b'' :
		retour = load_obj(byte) # On charge le contenu
		contenu = retour[0]
		debut = retour[1]
		fin = retour[2]
		byte = byte[debut+fin+4:] # On retire le contenu
		
		obj += [contenu,] # On ajoute le contenu a la liste
	
	return obj

def load_str(byte) :
	"""Decompresse une chaine de caracteres"""
	return byte.decode("utf-8") # On decode la chaine encodee en utf-8


def load_int(byte) :
	"""Decompresse un nombre entier"""
	return int(byte)

def load_float(byte) :
	"""Decompresse un nombre a virgule flottante"""
	return float(byte)