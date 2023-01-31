import cv2
from image_tools.constants import *


def resize(image, factor):
    """
    Resize image by a factor, maintaining aspect ratio
    :param image: to resize
    :param factor: to resize by
    """
    dims = image.shape
    new_dims = (int(dims[1] * factor), int(dims[0] * factor))
    return cv2.resize(image, new_dims)


def crop_about(image, center, crop_dims):
    """
    Crop image to dimensions about a center
    :param image: to crop
    :param center: coordinates top crop about
    :param crop_dims: of resultant cropped image
    """
    (x, y) = center
    (w, h) = crop_dims
    cropped = image[int(y - h/2): int(y + h/2), int(x - w/2): int(x + w/2)]
    return cropped


def crop_about_gui(image, crop_dims, cropped_filename):
    """
    Display image and at user's click, crop image to dimensions about input point
    :param image: to crop
    :param crop_dims: of resultant cropped image
    :param cropped_filename: to save cropped image
    """
    def set_mouse_crop(event, x, y, flags, param):
        nonlocal crop_center
        if event == cv2.EVENT_LBUTTONDOWN:
            crop_center = (x, y)

    crop_center = None
    cv2.imshow(CROP_GUI_TITLE, image)
    cv2.setMouseCallback(CROP_GUI_TITLE, set_mouse_crop)

    while True:
        if crop_center:
            cropped_image = crop_about(image, crop_center, crop_dims)
            break
        cv2.waitKey(CROP_GUI_DELAY)

    cv2.imwrite(cropped_filename, cropped_image)
    cv2.destroyAllWindows()
