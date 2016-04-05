import cPickle as pickle
import matplotlib.pylab as plt
from os import listdir
from vispy import app, scene, visuals
import numpy as np
import sys

def pickle2cmap(spectrogram_pickle):
	Ss = pickle.load(open(picklejar+spectrogram_pickle,'rb'))
	Ss /= Ss.max()
	colors = plt.cm.viridis(Ss[::-1,:])
	return (colors[:,:,:3]*255).astype(np.ubyte)


class Canvas(scene.SceneCanvas):
	"A calendar canvas that adds interactivity to the Image visual, and has time and frequency ticks"
	def __init__(self):
		#pdb.set_trace()
		scene.SceneCanvas.__init__(self, keys='interactive', size=(198*n_hours,2909))
		self.view = self.central_widget.add_view()

		# change camera pan and zoom such that only the x-axis is translated and scaled on mouse events
		#self.view.camera._viewbox.events.mouse_move.disconnect(self.view.camera.viewbox_mouse_event)
		self.show()
		scene.visuals.GridLines(parent=self.view.scene, scale=(2909./6000,1.98)) # 6 min grid


picklejar = "/home/ben/Documents/HypoSafe/pickled_specs/"
pickles = listdir(picklejar)
pickles.sort()
n_hours = len(pickles)


win = Canvas()
c = 0
for syltet_agurk in pickles[:n_hours]:
	day, hour = map(int,syltet_agurk.split("_")[:2])
	image = scene.visuals.Image(data=pickle2cmap(syltet_agurk), parent=win.view.scene)
	image.transform = visuals.transforms.AffineTransform()
	image.transform.translate([(day-12)*2909,(hour-6)*198, 0])
	win.view.add(image)
	c += 1

win.view.camera = scene.PanZoomCamera(rect=(-10, -10, 2909+20, n_hours*198+20), aspect=1.0)
win.view.camera.flip = (False,True,False) #flip y axis
app.run()

# On bandpass filtering
# 1. save the parameters that made the filter, and the filter coeffs themselves
# 2. plot the unfiltered and filtered eeg in the same plot to check for phase desync
# 3. use a high order Butterworth filter, to make the frequency repsonse flat in the passband, and the a linear phase response