from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
from skimage import io
import matplotlib.pyplot as plt


# load the image and convert it to a floating point data type
image = img_as_float(io.imread("../Files/frames/3.jpg"))

# loop over the number of segments
#for numSegments in (50,100):
    # apply SLIC and extract (approximately) the supplied number
    # of segments

numSegments = 4
segments = slic(image, n_segments=numSegments, compactness=10, sigma=4)

# show the output of SLIC
fig = plt.figure("Superpixels -- %d segments" % (numSegments))
ax = fig.add_subplot(1, 1, 1)
ax.imshow(mark_boundaries(image, segments))
plt.axis("off")

# show the plots
plt.show()
