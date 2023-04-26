import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
from skimage import color, filters, measure

# Load the image (replace with your image path)
img_path = 'C:/Users/m_jen/Downloads/Sem 8/Sen lab project/MJ/input_images/0uMCr004.jpg'
im = io.imread(img_path, as_gray=True)
im = im[10:-10, 10:-10]

im = filters.gaussian(im, sigma=5)

# Invert the image so that cells are white and background is black
#im = np.invert(im)

# Threshold the image to get a binary image with cells as 1s and background as 0s
#threshold = 0.4
#bw = im > threshold
thresh = filters.threshold_otsu(im)
binary = im < thresh
# Label the binary image to identify connected components (i.e., cells)
label_image = measure.label(binary, connectivity=1)

# Keep count of the number of cells that meet your criteria
cell_count = 0

# Define sphericity and size cutoffs (you can adjust these)
min_sphericity = 0.08
min_size = 500
max_size = 20000
min_intensity = 0.40
# Filter regions based on size and sphericity
cells = []
for region in measure.regionprops(label_image, intensity_image=im):
    if region.area > min_size and region.area < max_size:
        equivalent_diameter = region.equivalent_diameter
        perimeter = region.perimeter
        sphericity = 4 * np.pi * region.area / (perimeter ** 2)
        mean_intensity = region.mean_intensity
        if sphericity > min_sphericity and region.coords[:, 0].min() > 0 and region.coords[:, 0].max() < im.shape[0] - 1 and region.coords[:, 1].min() > 0 and region.coords[:, 1].max() < im.shape[1] - 1 and mean_intensity > min_intensity:
            cells.append(region)

# Display the thresholded image and final image with counted cells
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))
ax1.imshow(binary, cmap='gray')
ax1.set_title('Thresholded image')
ax2.imshow(im)
ax2.set_title(f'Number of cells: {len(cells)}')
for cell in cells:
    ax2.annotate('', xy=(cell.centroid[1], cell.centroid[0]), xytext=(cell.centroid[1]+10, cell.centroid[0]+10), color='red', arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle="->"))

plt.show()
#print('Number of chlamydomonas cells: ', cell_count)
