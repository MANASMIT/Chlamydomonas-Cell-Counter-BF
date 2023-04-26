import skimage.io as io
import skimage.filters as filters
import skimage.measure as measure
from scipy import ndimage
import matplotlib.pyplot as plt

# Load the image (replace with your image path)
img_path = 'C:/Users/m_jen/Downloads/Sem 8/Sen lab project/MJ/Images/Cr dcfda CLONE 3 AND 189/Pre Cu Stress DCFDA/CLONE3_6uM18.jpg'
im = io.imread(img_path, as_gray=True)

# Apply threshold to get binary image with fluorescing cells as 1s and background as 0s
threshold = 0.5 # adjust this as per your requirement
binary = im > threshold

# Fill holes in the binary image
filled = ndimage.binary_fill_holes(binary)

# Label the binary image to identify connected components (i.e., cells)
label_image = measure.label(filled, connectivity=1)
cell_count = 0

# Define size cutoffs (you can adjust these)
min_size = 400
max_size = 20000
min_intensity = 0.60
# Filter regions based on size
cells = []
for region in measure.regionprops(label_image, intensity_image=im):
    if region.area > min_size and region.area < max_size:
        mean_intensity = region.mean_intensity
        if mean_intensity > min_intensity:
            cells.append(region)


# Display the thresholded image and final image with counted cells
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4))
ax1.imshow(filled, cmap='gray')
ax1.set_title('Thresholded image')
ax2.imshow(im)
ax2.set_title(f'Number of cells: {len(cells)}')
for cell in cells:
    ax2.annotate('', xy=(cell.centroid[1], cell.centroid[0]), xytext=(cell.centroid[1]+10, cell.centroid[0]+10), color='red', arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle="->"))

plt.show()
print('Number of fluorescing cells: ', len(cells))
