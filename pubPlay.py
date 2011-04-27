from bge import texture as VT
from bge import logic as G

def init_pub():
	cont = G.getCurrentController()
	obj = cont.owner

	matID = VT.materialID(obj, 'MApub')
	G.video = VT.Texture(obj, matID)

	S1 = G.expandPath("//circuits/circuitdesertlau3/pub.avi")
	video_source = VT.VideoFFmpeg(S1)
	video_source.repeat = -1
	video_source.scale = True
	video_source.flip = True

	G.video.source = video_source
	G.video.source.play()


def update():
	G.video.refresh(True)