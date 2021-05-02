"""Utilities for resizing images.
Image resizing, snippet repurposed from:
https://djangosnippets.org/snippets/10597/"""

import random
import string
import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def get_random_string(length):
    """Creates random string for unique image names."""
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters)
                         for i in range(length))
    # print random string
    return result_str.lower()


def image_resize(self, image_title, width, height):
    """Function to resize the images for smaller memory."""
    # Checks if the instance already exists
    this_object = None
    image_field = getattr(self, image_title)
    try:
        # If it exists, selects current image, if not goes to next step
        this_object = self.__class__.objects.get(pk=self.id)
        object_image = getattr(this_object, image_title)
    except self.__class__.DoesNotExist:
        pass
    try:
        img = Image.open(image_field)
        img_format = img.format.lower()

        # Prevents images from being copied on every save
        # will save a new copy on an upload
        if (this_object and f'{image_field.name}'
            .replace(' ', '_').replace('(', '').replace(')', '')
                not in object_image.name) or (not this_object):
            # Image is resized
            output_size = (width, height)
            img = img.resize(size=(output_size))

            # Converts format while in memory
            output = BytesIO()
            img.save(output, format=img_format)
            output.seek(0)

            # Replaces the Imagefield value with the newly converted image
            image_field = InMemoryUploadedFile(
                output,
                'ImageField',
                f'{image_field.name.split(".")[0]}_\
                    {get_random_string(8)}.{img_format}',
                'image/jpeg', sys.getsizeof(output),
                None)
            return image_field
        # if the image doesn't need to be changed, returns false
        return False
    # If uploading multiple images on a new file there can this error.
    except ValueError:
        return False


def responsive_images(self, image_title, width, height, thumb=False):
    """Uses the resize_image function to create three different sized images
    Returned from largest to smallest."""
    lg_image = image_resize(self, image_title, width, height)
    md_image = image_resize(self, image_title, width//3*2, height//3*2)
    sm_image = image_resize(self, image_title, width//3, height//3)

    if thumb is True:
        xs_image = image_resize(self, image_title, 48, 64)
        return lg_image, md_image, sm_image, xs_image

    return lg_image, md_image, sm_image
