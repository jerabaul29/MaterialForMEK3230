import numpy as np
import matplotlib.pyplot as plt
from skimage import io, img_as_float
from skimage.color import rgb2gray

###############################################################################
# all functions ###############################################################
###############################################################################


def plot_images(images, titles=None):
    """This function takes a list of images with
    their titles as arguments and plots side by side."""
    n_ims = len(images)
    if titles is None:
        titles = ['(%d)' % i for i in range(1, n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image, title in zip(images, titles):
        a = fig.add_subplot(1, n_ims, n)  # Subplot
        if image.ndim == 2:  # Is image grayscale?
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
        a.set_xlabel('Number of pixels')
        a.set_ylabel('Number of pixels')
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show()


class generateDataOnClick:
    def __init__(self, verbose=0):
        self.position_on_click_accumulator = []
        self.verbose = verbose

        if self.verbose > 0:
            print(" ")
            print("To use this function: clik on the positions you are")
            print("interested in, then once finished close the plot.")
            print(" ")

    def position_on_click(self, event):
        # x, y = event.x, event.y
        if event.button == 1:
            if event.inaxes is not None:
                if self.verbose > 0:
                    print('data coords: ' + str(event.xdata) + " , " + str(event.ydata))
                self.position_on_click_accumulator.append((event.xdata, event.ydata))
                plt.axvline(event.xdata, color='r')
                plt.show()

    def return_positions(self):
        return self.position_on_click_accumulator


def compute_distance(tuple_1, tuple_2):
    return np.sqrt((tuple_1[0] - tuple_2[0])**2 + (tuple_1[1] - tuple_2[1])**2)

###############################################################################
# processing of one image #####################################################
###############################################################################

# Name of the file ------------------------------------------------------------
filename = 'DSC_0476.JPG'
upload_image = io.imread(filename)  # Upload the image
image_rgb = img_as_float(upload_image[0])  # Convert the image to a np array
image_gray = rgb2gray(image_rgb)  # Convert to gray image

# Show both color and gray images ---------------------------------------------
plot_images(images=[image_rgb[300:, :], image_gray[300:, :]],
            titles=['RGB image', 'Gray image'])

# select two points on the image for performing calibration -------------------
plt.figure()
plt.imshow(image_gray)
plt.xlabel('Number of pixels')
plt.ylabel('Number of pixels')

generate_data_on_click_object = generateDataOnClick(verbose=1)

plt.connect('button_press_event', generate_data_on_click_object.position_on_click)
plt.show()

selected_positions_pixels = generate_data_on_click_object.return_positions()

print(selected_positions_pixels)

# perform calibration ---------------------------------------------------------
# distances in the real world are given in m
distance_real_world = 0.07
distance_pixels = compute_distance(selected_positions_pixels[0], selected_positions_pixels[1])

pixels_to_real_world = distance_real_world / distance_pixels

print("pixels_to_real_world: " + str(pixels_to_real_world))

# measure the length of a droplet ---------------------------------------------
plt.figure()
plt.imshow(image_gray)
plt.xlabel('Number of pixels')
plt.ylabel('Number of pixels')

generate_data_on_click_object = generateDataOnClick(verbose=1)

plt.connect('button_press_event', generate_data_on_click_object.position_on_click)
plt.show()

selected_positions_pixels = generate_data_on_click_object.return_positions()

length_droplet_meters = compute_distance(selected_positions_pixels[0], selected_positions_pixels[1]) * pixels_to_real_world
print("length droplet (m): " + str(length_droplet_meters))
