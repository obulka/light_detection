"""Contains object detection classes."""
# 3rd Party Imports
import cv2
import numpy as np
import skimage.measure


class ObjectDetector:
    """Base class for object detectors."""

    def __init__(self, image_path=None, image=None):
        """Initialize a light detector object.

        Keyword Args:
            image_path (str):
                Path to the image to detect lights in.
                Default is None.
                Preferred if both arguments are specified.

            image (np.array(:,:,:), uint8):
                The BGR formatted image data to detect lights in.
                Default is None.

        Raises:
            FileNotFoundError:
                If the file cannot be read and `image` is nto specified.
            TypeError: If neither parameter is specified.
        """
        if not image_path and not image:
            raise TypeError("A parameter must be specified.")

        if image_path:
            # Load the image as a BGR numpy array.
            new_image = cv2.imread(image_path)
            if new_image is None:
                if image:
                    print("File not found, using image that was passed.")
                else:
                    raise FileNotFoundError("The file path is invalid.")

        if new_image is None:
            new_image = image.copy()

        self._original_img = new_image.copy()
        self._working_img = new_image

    def _erode_dilate_img(self, erode_iters=2, dilate_iters=4):
        """Erode and dilate the working image.

        Keyword Args:
            erode_iters (int):
                Number of erosion iterations to perform.
                Default is 2.

            dilate_iters (int):
                Number of dilation iterations to perform.
                Default is 4.
        """
        self._working_img = cv2.erode(
            self._working_img,
            None,
            iterations=erode_iters,
        )
        self._working_img = cv2.dilate(
            self._working_img,
            None,
            iterations=dilate_iters,
        )

    def _gaussian_blur_img(self, blur_length=5):
        """Apply a gaussian blur to the working image.

        Keyword Args:
            blur_length (int):
                The length to use in Gaussian blurring the image.
                Must be odd. Default is 5.
        """
        self._working_img = cv2.GaussianBlur(
            self._working_img,
            (blur_length,) * 2,
            0.,
        )

    def _get_contours(self, sort=False):
        """Find the contours in the mask, sorted from left to right.

        Returns:
            list(np.array((:, 1, 2), int)): Contains the image contours.
        """
        contours = cv2.findContours(
            self._working_img.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        if len(contours) == 2:
            contours = contours[0]
        elif len(contours) == 3:
            contours = contours[1]
        else:
            raise ValueError(
                f"Contours must be of size 2 or 3, currently size: {len(contours)}",
            )
        if sort:
            contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
        return contours

    def _preprocess_img(self):
        """Preprocess the working image for object detection."""

    def _threshold_img(self, threshold=128):
        """Automatically threshold the working image."""
        self._working_img = cv2.threshold(
            self._working_img,
            threshold,
            255,
            cv2.THRESH_BINARY,
        )[1]

    @property
    def gray_scale_img(self):
        """np.array((:,:), np.uint8):
                The grayscale version of the original image.
        """
        return cv2.cvtColor(self._original_img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def show_image(image, window_title="Image"):
        """Display an image.

        Args:
            image (np.array((:,:,...), np.uint8)): The image to show.

        Keyword Args:
            window_title (str): The title to display on the window.
        """
        cv2.imshow(window_title, image)
        cv2.waitKey(0)

    def show_working_image(self):
        """Display the current working image."""
        self.show_image(self._working_img, "Working Image")


class LightDetector(ObjectDetector):
    """Object capable of finding light sources in an image."""

    def __init__(self, image_path=None, image=None, blur_length=5, threshold=210):
        """Initialize a light detector object.

        Keyword Args:
            image_path (str):
                Path to the image to detect lights in.
                Default is None.
                Preferred if both arguments are specified.

            image (np.array(:,:,:), uint8):
                The BGR formatted image data to detect lights in.
                Default is None.

            blur_length (int):
                The length to use in Gaussian blurring the image.
                Must be odd. Default is 5.

            threshold (np.uint8):
                The value to threshold the image on.
                Default is 210.

        Raises:
            TypeError: If neither parameter is specified.
        """
        super(LightDetector, self).__init__(image_path, image)

        self._blur_length = blur_length
        self._threshold = threshold
        self._light_contours = []

        self._working_img = self.gray_scale_img

        self._preprocess_img()

    def _mask_lights(self, min_size=300):
        """Perform a connected component analysis on the thresholded
        image, then initialize a mask to store only the "large"
        components.

        Keyword Args:
            min_size (int):
                The minimum number of pixels in a light source.
        """
        labels = skimage.measure.label(self._working_img, neighbors=8, background=0)
        self._working_img = np.zeros(self._working_img.shape, dtype=np.uint8)

        for label in np.unique(labels):
            # Ignore the background label
            if label == 0:
                continue

            # Construct the label mask
            label_mask = np.zeros(self._working_img.shape, dtype=np.uint8)
            label_mask[labels == label] = 255

            # Count the number of pixels in the component
            num_pixels = cv2.countNonZero(label_mask)

            # If the number of pixels is large enough,
            # add it to the final mask of blobs
            if num_pixels > min_size:
                self._working_img = cv2.add(self._working_img, label_mask)

    def _preprocess_img(self):
        """Preprocess a greyscale image for object detection."""
        self._gaussian_blur_img(self._blur_length)
        self._threshold_img(self._threshold)
        self._erode_dilate_img()
        self._mask_lights()

    def _reprocess_image(self):
        """Reprocess the original image and reset the `lights`
        parameter.
        """
        self._working_img = self.gray_scale_img
        self._preprocess_img()
        self._reset_lights()

    def _reset_lights(self):
        """Reset the `lights` parameter to be empty."""
        self._light_contours = []

    def _set_lights(self):
        """Find the lights in the image."""
        self._light_contours = self._get_contours()

    @property
    def gaussian_blur_length(self):
        """int: The edge length of the gaussion blur kernel."""
        return self._blur_length

    @gaussian_blur_length.setter
    def gaussian_blur_length(self, new_length):
        """Set the length of the gaussion blur kernel.

        Args:
            new_length (int): The new kernel edge length
        """
        self._blur_length = new_length
        self._reprocess_image()

    @property
    def light_contours(self):
        """list(np.array((:, 1, 2), int)): Contains contours of lights."""
        if not self._light_contours:
            self._set_lights()
        return self._light_contours

    @property
    def threshold(self):
        """np.uint8: The value to threshold the image on."""
        return self._threshold

    @threshold.setter
    def threshold(self, new_threshold):
        """Change the value the image should be thresholded on.

        Args:
            new_threshold (np.uint8): The new value to threshold on.
        """
        self._threshold = new_threshold
        self._reprocess_image()

    def show_lights(self, colour=(0, 0, 255), thickness=3):
        """Display the lights.

        Keyword Args:
            colour (tuple(uint8)):
                The BGR colour to mark the lights with.

            thickness (int):
                The line thickness to use in marking the lights.
        """
        display_image = self._original_img.copy()

        for contour in self.light_contours:
            # draw the light on the image
            center, radius = cv2.minEnclosingCircle(contour)

            cv2.circle(
                display_image,
                (int(center[0]), int(center[1])),
                int(radius),
                colour,
                thickness,
            )
        # show the output image
        self.show_image(display_image, "Lights")
