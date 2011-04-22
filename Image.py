#  ----------------------------  #
#      Par Bobibou pour HSR      #
#  ----------------------------  #


#  ----------------------------  #
#  Classe de chargement d'image  #
#  ----------------------------  #

class Image:
	"""Classe de chargement d'image"""
	from bge import texture as VT
	from bge import logic as gl
	import bgl
	import math
	
	def __init__(self, baseObj, img, mat,
				viewport=[0.0, 100.0, 0.0, 100.0],
				rect=None,
				col=[1.0, 1.0, 1.0, 1.0],
				verco=None,
				texco=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]):
		"""Initialisation de l'image
			Parametres :
				- baseObj : Objet contenant la texture de base
				- img : Nom de l'image
				- mat : Material de l'objet correspondant a l'image
				- viewport : Coordonnees minimales et maximales de l'affichage : [xmin, ymax, xmax, ymin]
				- rect : Coordonnees des coins de l'image pour un affichage rectangulaire : [x1, y1, x2, y2]
				- col : Couleur RVBA de l'image : [r, v, b, a]
				- verco : Liste des coordonnees x/y de chaque vertice.
				- texco : Liste des coordonnees u/v de chaque vertice."""
		VT = __class__.VT
		gl = __class__.gl
		
		self.ok = True
		self.angle = 0
		
		if verco == None  and rect == None :
			verco = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
		elif verco == None :
			verco = [(rect[0], rect[1]), (rect[2], rect[1]), (rect[2], rect[3]), (rect[0], rect[3])]
        
		self.texco = texco
		self.verco = verco
		
		self.bary = [0, 0]
		for i in range(len(self.verco)):
			self.bary[0] += self.verco[i][0]
			self.bary[1] += self.verco[i][1]
		self.bary[0] /= len(self.verco)
		self.bary[1] /= len(self.verco)
		
		self.couleur = col
		
		self.viewport = viewport
		
		root = gl.expandPath("//")

		VT_img_Img = VT.ImageFFmpeg(root + img)
		
		if VT_img_Img.status == 0 :
			print("Erreur: Image introuvable a l'adresse '" + root + img + "'")
			self.ok = False
			return
		
		VT_img_Mat = VT.materialID(baseObj, "MA" + mat)
		VT_img_Tex = VT.Texture(baseObj, VT_img_Mat)
		
		VT_img_Tex.source = VT_img_Img
		
		self.VT_img = VT_img_Tex
		
		self.rafraichir()
		
		return
	
	def rafraichir(self):
		"""Rafraichit l'image. Pour une image statique, un seul appel est necessaire.
		Il est automatiquement fait a l'initialisation.
		Pour une video, il faut le faire a chaque frame."""
		if self.ok :
			self.VT_img.refresh(True)
		return
	
	def afficher(self):
		"""Affiche l'image"""
		VT = __class__.VT
		gl = __class__.gl
		bgl = __class__.bgl
		math = __class__.math
		
		if self.ok :
			
			id = self.VT_img.bindId
	
			if id :  
				bgl.glMatrixMode(bgl.GL_PROJECTION)
				bgl.glLoadIdentity();
				vp = self.viewport
				bgl.glOrtho(vp[0], vp[1], vp[2], vp[3], -1.0, 1.0)
				
				bgl.glMatrixMode(bgl.GL_MODELVIEW)
				bgl.glLoadIdentity()
				
				bgl.glEnable(bgl.GL_TEXTURE_2D)
				bgl.glEnable(bgl.GL_BLEND) 
				bgl.glBindTexture(bgl.GL_TEXTURE_2D, id)
				
				bgl.glTranslatef(self.bary[0], self.bary[1], 0)
				bgl.glRotatef(math.degrees(self.angle), 0.0, 0.0, 1.0)
				bgl.glTranslatef(-self.bary[0], -self.bary[1], 0)
				
				bgl.glBegin(bgl.GL_QUADS)
				col = self.couleur
				for i in range(len(self.texco)):
					bgl.glColor4f(col[0], col[1], col[2], col[3])
					bgl.glTexCoord2f(self.texco[i][0], self.texco[i][1])
					bgl.glVertex2f(self.verco[i][0], self.verco[i][1])
				bgl.glEnd()
				
				bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
			else :
				self.ok = False
		
		return
	
	def setCouleur(self, r, v, b, a):
		"""Modifie la couleur de l'image.
			Parametres :
				- r : Composante rouge
				- v : Composante verte
				- b : Composante bleue
				- a : Transparence"""
		self.couleur = [r, v, b, a]
		
		return
	
	def setRect(self, x1, y1, x2, y2):
		"""Modifie les coordonnees de l'image rectangulaire.
			Parametres :
				- x1 : Abscisse du coin inferieur gauche
				- y1 : Ordonnee du coin inferieur gauche
				- x2 : Abscisse du coin superieur droit
				- y1 : Ordonnee du coin superieur droit"""
		self.verco = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
		
		self.bary = [0, 0]
		for i in range(len(self.verco)):
			self.bary[0] += self.verco[i][0]
			self.bary[1] += self.verco[i][1]
		self.bary[0] /= len(self.verco)
		self.bary[1] /= len(self.verco)
		
		return
	
	def setVert(self, verco):
		"""Modifie les coordonnees de tous les vertice.
			Des vertice peuvent etre ajoutes
			Parametres :
				- verco : Liste des coordonnees x/y de chaque vertice."""
		
		self.verco = verco
		
		self.bary = [0, 0]
		for i in range(len(self.verco)):
			self.bary[0] += self.verco[i][0]
			self.bary[1] += self.verco[i][1]
		self.bary[0] /= len(self.verco)
		self.bary[1] /= len(self.verco)
		
		return

	def setUV(self, texco):
		"""Modifie les coordonnees du depliage de tous les vertice.
			Des vertice peuvent etre ajoutes. C'est cette liste qui definie le nombre de vertice a afficher.
			Parametres :
				- texco : Liste des coordonnees u/v de chaque vertice."""
		
		self.texco = texco
		return
	
	def setViewPort(self, xmin, ymax, xmax, ymin):
		"""Definit les coordonnes minimales et maximales de l'affichage.
			Parametres :
				- xmin : Coordonnee X minimale
				- ymax : Coordonnee Y maximale
				- xmax : Coordonnee X maximale
				- ymin : Coordonnee Y minimale"""
		
		self.viewport = [xmin, ymax, xmax, ymin]
       
	def setAngle(self, a):
		"""Modifie l'orientation de l'objet
			Parametres :
				- a : Angle en radians"""
		
		self.angle = a
		return



#  ---------------------------------  #
#  Classe de chargement d'un rendeur  #
#  ---------------------------------  #

class Render(Image):
	"""Classe de chargement d'un rendeur
	(herite de Image)"""
	import VideoTexture as VT
	from bge import logic as gl
	import bgl
	
	def __init__(self, baseObj, camera, mat, flip = False,
				viewport=[0.0, 100.0, 0.0, 100.0],
				rect=None,
				col=[1.0, 1.0, 1.0, 1.0],
				verco=None,
				texco=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]):
		"""Initialisation du rendeur
			Parametres :
				- baseObj : Objet contenant la texture de base
				- camera : Objet source du rendu
				- mat : Material de l'objet correspondant a l'image
				- flip : Si le rendu doit etre retourne (pour un retroviseur par exemple)
				- viewport : Coordonnees minimales et maximales de l'affichage : [xmin, ymax, xmax, ymin]
				- rect : Coordonnees des coins de l'image pour un affichage rectangulaire : [x1, y1, x2, y2]
				- col : Couleur RVBA de l'image : [r, v, b, a]
				- verco : Liste des coordonnees x/y de chaque vertice.
				- texco : Liste des coordonnees u/v de chaque vertice."""
		
		VT = __class__.VT
		gl = __class__.gl
		
		self.ok = True
		self.angle = 0
		
		if verco == None  and rect == None :
			verco = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
		elif verco == None :
			verco = [(rect[0], rect[1]), (rect[2], rect[1]), (rect[2], rect[3]), (rect[0], rect[3])]
		
		self.texco = texco
		self.verco = verco
		
		self.bary = [0, 0]
		for i in range(len(self.verco)):
			self.bary[0] += self.verco[i][0]
			self.bary[1] += self.verco[i][1]
		self.bary[0] /= len(self.verco)
		self.bary[1] /= len(self.verco)
		
		self.couleur = col
		
		self.viewport = viewport
		
		VT_img_Render = VT.ImageRender(gl.getCurrentScene(), camera)
		VT_img_Render.scale = True
		VT_img_Render.flip = flip
		
		VT_img_Mat = VT.materialID(baseObj, "MA" + mat)
		VT_img_Tex = VT.Texture(baseObj, VT_img_Mat)
		
		VT_img_Tex.source = VT_img_Render
		
		self.VT_img = VT_img_Tex
		
		self.rafraichir()
		
		return
		

#  --------------------------------  #
#  Classe de chargement d'une video  #
#  --------------------------------  #

class Video(Image):
	"""Classe de chargement d'une video
	(herite de Image)"""
	import VideoTexture as VT
	from bge import logic as gl
	import bgl
	
	def __init__(self, baseObj, video, mat,
				viewport=[0.0, 100.0, 0.0, 100.0],
				rect=None,
				col=[1.0, 1.0, 1.0, 1.0],
				verco=None,
				texco=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]):
		"""Initialisation de la video
			Parametres :
				- baseObj : Objet contenant la texture de base
				- video : Nom de la video
				- mat : Material de l'objet correspondant a l'image
				- viewport : Coordonnees minimales et maximales de l'affichage : [xmin, ymax, xmax, ymin]
				- rect : Coordonnees des coins de l'image pour un affichage rectangulaire : [x1, y1, x2, y2]
				- col : Couleur RVBA de l'image : [r, v, b, a]
				- verco : Liste des coordonnees x/y de chaque vertice.
				- texco : Liste des coordonnees u/v de chaque vertice."""
		
		VT = __class__.VT
		gl = __class__.gl
		
		self.ok = True
		self.angle = 0
		
		if verco == None  and rect == None :
			verco = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
		elif verco == None :
			verco = [(rect[0], rect[1]), (rect[2], rect[1]), (rect[2], rect[3]), (rect[0], rect[3])]
		
		self.texco = texco
		self.verco = verco
		
		self.bary = [0, 0]
		for i in range(len(self.verco)):
			self.bary[0] += self.verco[i][0]
			self.bary[1] += self.verco[i][1]
		self.bary[0] /= len(self.verco)
		self.bary[1] /= len(self.verco)
		
		self.couleur = col
		
		self.viewport = viewport
		
		root = gl.expandPath("//")

		VT_img_Video = VT.VideoFFmpeg(root + video)
		
		if VT_img_Video.status == 0 :
			print("Erreur: Video introuvable a l'adresse '" + root + video + "'")
			self.ok = False
			return
		
		
		VT_img_Video.play()
		
		VT_img_Mat = VT.materialID(baseObj, "MA" + mat)
		VT_img_Tex = VT.Texture(baseObj, VT_img_Mat)
		
		VT_img_Tex.source = VT_img_Video
		
		self.VT_img = VT_img_Tex
		
		self.rafraichir()
		
		return
		
