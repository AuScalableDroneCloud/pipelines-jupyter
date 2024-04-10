"""Class to represent hyperspectral data"""
import os
import rasterio
import cv2
import numpy as np

RGB_WAVELENGTH = (700, 530, 470)

BIL_EXTENSION = '.bil'
HDR_EXTENSION = '.hdr'
H5PY_EXTENSION = '.hdf5'

# Network Constants
NUM_CONVOLUTION_LAYERS = 4
NUM_HYPERSPECTRAL_CHANNELS = 480
NUM_FLUORESCENCE_CHANNELS = 5

# Various default paths
RESULTS_PATH = os.path.join('', 'results')
TRAIN_RESULTS_PATH = os.path.join(RESULTS_PATH, 'train')
MODELS_PATH = os.path.join(TRAIN_RESULTS_PATH, 'models')
TRAIN_LOG_PATH = os.path.join(TRAIN_RESULTS_PATH, 'logs')
TEST_RESULTS_PATH = os.path.join(RESULTS_PATH, 'test')
TEMP_DIR = 'temp'


def load_hyperspectral_image(filepath):
    """Loads a hyperspectral image

    IMPORTANT: Both the .hdr and .bil files must be named identically

    Args:
        filepath (str): Filepath to the hyperspectral file (with or without out an extension)

    Returns:
        (rasterio.io.DatasetReader): The rasterio object representing the hyperspectral data
    """
    bil_filepath = os.path.splitext(filepath)[0] + BIL_EXTENSION
    return rasterio.open(bil_filepath)


def extract_hyperspectral_wavelengths(filepath):
    """Extracts the wavelengths of the hyperspectral data from the HDR file

    IMPORTANT: Both the .hdr and .bil files must be named identically

    Args:
        filepath (str): Filepath to the hyperspectral file (with or without out an extension)

    Returns:
        (list): List of hyperspectral wavelengths
    """
    wavelengths = []
    hdr_filepath = os.path.splitext(filepath)[0] + HDR_EXTENSION

    # Extract the data from the hdr file
    with open(hdr_filepath, 'r') as hdr_file:
        contents = hdr_file.readlines()
        contents = [content.rstrip() for content in contents]
        wl_start_idx = contents.index('WAVELENGTHS')
        wl_end_idx = contents.index('WAVELENGTHS_END')
        wavelengths = contents[wl_start_idx + 1:wl_end_idx]
    return wavelengths



class HyperspectralImage:
    def __init__(self, filepath, white_calib, dark_calib):
        """Constructor for hyperspectral image

        Args:
            filepath (str): Filepath to the hyperspectral file (with or without out an extension)
        """
        self.base_filepath = os.path.splitext(filepath)[0]
        self.image = load_hyperspectral_image(self.base_filepath)
        self.wavelengths = extract_hyperspectral_wavelengths(self.base_filepath)

        self.white_image = load_hyperspectral_image(os.path.splitext(white_calib)[0])
        self.white_wavelengths = extract_hyperspectral_wavelengths(os.path.splitext(white_calib)[0])
        self.dark_image = load_hyperspectral_image(os.path.splitext(dark_calib)[0])
        self.dark_wavelengths = extract_hyperspectral_wavelengths(os.path.splitext(dark_calib)[0])
        self.get_calib_values()

    def get_calib_values(self):
        '''
        calculate white and dark calibration values
        '''
        white = []
        dark = []
        for w_wl_idx in range(len(self.white_wavelengths)):
            white_im = self.white_image.read(w_wl_idx + 1)
            white.append(white_im)
        white_array = np.stack(white, axis=2)
        self.white_calib = white_array.mean(0)


        for d_wl_idx in range(len(self.dark_wavelengths)):
            dark_im = self.dark_image.read(d_wl_idx + 1)
            dark.append(dark_im)
        dark_array = np.stack(dark, axis=2)
        self.dark_calib = dark_array.mean(0)



    def _get_hyperspec_attributes(self, attr=None):
        """Gets all attributes related to the hyperspectral image

        Goes through all attributes associated with the hyperspectral image and returns
        them as a dict. Can also specify to just receive a single attribute
        """
        if attr is not None:
            attrs = getattr(self.image, attr)
        else:
            attrs = {}
            for attr in dir(self.image):
                try:
                    attrs[attr] = getattr(self.image, attr)
                except:
                    attrs[attr] = None
        return attrs

    def get_closest_wavelength(self, wavelength):
        """Given a wavelength, searches the list of wavelengths to find the closest one"""
        closest_wavelength = min(self.wavelengths, key=lambda x: abs(float(x) - wavelength))
        closest_idx = self.wavelengths.index(closest_wavelength)
        return closest_idx, closest_wavelength

    def extract_image_layer(self, wavelength, normalized=False, crop_region=None):
        """Extracts the image layer with wavelength closest to the specified parameter

        This is extracted as a 16 bit unsigned array
        The range of data is realistically 12-bit however
        Returns both the index of the wavelength and the image layer

        NOTE: Rasterio indexing starts at 1, hence 1 is always added to the index
            (To shift from python 0 indexing to rasterio 1 indexing)

        Closest wavelength to one given is extracted

        Data returned in order: HW

        Args:
            wavelength (int/float): Wavelength of light to extract
            normalized (bool): If true, normalizes the image to the range of [0-255]
            crop_region (2x2 numpy ndarray): The top-left/bottom-right x,y coordinates of the crop
                to take
        """
        wavelength_idx, _ = self.get_closest_wavelength(wavelength)
        im = self.image.read(wavelength_idx + 1)
        white_calib_values = self.white_calib[:, wavelength_idx]
        white_calib_values = white_calib_values.reshape(1, white_calib_values.shape[0])
        white_calib_values = np.tile(white_calib_values, [im.shape[0], 1])

        dark_calib_values = self.dark_calib[:, wavelength_idx]
        dark_calib_values = dark_calib_values.reshape(1, dark_calib_values.shape[0])
        dark_calib_values = np.tile(dark_calib_values, [im.shape[0], 1])

        im_cal = (im - dark_calib_values) / (white_calib_values - dark_calib_values + 1e-10)
        im_cal[im_cal > 1] = 1
        im_cal[im_cal < 0] = 0

        if crop_region is not None:
            im_cal = im_cal[crop_region[0][1]:crop_region[1][1], crop_region[0][0]:crop_region[1][0]]
            im = im[crop_region[0][1]:crop_region[1][1], crop_region[0][0]:crop_region[1][0]]

        return wavelength_idx, im_cal

    def extract_rgb_layers(self, rgb_wavelengths, normalized=True, crop_region=None):
        """Creates an RGB image using given wavelengths

        Given a hyperspectral image, creates an RGB image using frequencies given
        as arguments. If parameter set, will scale the image from 12-bit to 8-bit

        Args:
            rgb_wavelengths (float 3-tuple): (R,G,B) light frequencies

        Returns:
            (tuple): red, green, blue wavelength indexes
            (numpy ndarray): Array representing the image
        """
        red_idx, red_image = self.extract_image_layer(rgb_wavelengths[0], normalized=normalized,
                                                      crop_region=crop_region)
        green_idx, green_image = self.extract_image_layer(rgb_wavelengths[1], normalized=normalized,
                                                          crop_region=crop_region)
        blue_idx, blue_image = self.extract_image_layer(rgb_wavelengths[2], normalized=normalized,
                                                        crop_region=crop_region)

        rgb_im = np.stack([red_image, green_image, blue_image], axis=2)

        return (red_idx, green_idx, blue_idx), rgb_im

    def extract_all_layers(self, normalized=False, crop_region=None):
        """Extracts all layers (wavelengths) of the hyperspectral image

        Data returned in format: HWC (Where channels are all 480 wavelengths)

        Returns:
            (list of float): All extracted wavelength values
            (numpy ndarray): The hyperspectral image data in format HWC
        """
        output_images = []
        for wavelength in self.wavelengths:
            output_images.append(
                self.extract_image_layer(float(wavelength), normalized=normalized, crop_region=crop_region)[1])
        return [float(wavelength) for wavelength in self.wavelengths], np.stack(output_images, axis=2)


    def threshold_image(self, wavelength, threshold, max=1):
        """Performs a binary threshold on an image at a specific wavelength

        Output is a thresholded 'mask' consisting of integer values in range [0, 1]

        Included when initially trying to coregister images
        """
        wavelength_idx, im = self.extract_image_layer(wavelength)
        # This gets the image to only have 2 binary values, 0 and <max> (here max=1)
        _, thresholded_image = cv2.threshold(im, threshold, max, cv2.THRESH_BINARY)
        # Converts the type to 8 bit unsigned
        thresholded_image = thresholded_image.astype('uint8')
        return wavelength_idx, thresholded_image
