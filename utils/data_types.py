# Copyright      2018  Johns Hopkins University (author: Daniel Povey)

# Apache 2.0
import numpy as np
from utils.core_config import CoreConfig  # import waldo.core_config


def validate_config(c, train_image_size=None):
    """
    This function validates that 'c' is a valid configuration object of
    type CoreConfig.
    """
    assert isinstance(c, CoreConfig)
    c.validate(train_image_size)


def validate_image_with_mask(x, c):
    """This function validates an object x that is supposed to represent an image
    with the corresponding object mask.  c is the config object as validated
    by 'validate_config'.  This function returns no value; on failure
    it raises an exception.  Specifically it is checking that:
      x['img'] is a numpy array of shape (height, width, num_colors),
            num_colors is c.num_colors.
      x['mask'] is an integer numpy array of shape (height,width) containing
             integer object-ids from 0 ... num-objects - 1.
      x['object_class'] is a list indexed by object-id giving the class of each object;
            object classes should be in the range 0 .. num_classes - 1, where
            num_classes is c.num_classes."""
    validate_config(c)
    if type(x) != dict:
        raise ValueError('dict type input required.')

    if 'img' not in x or 'mask' not in x or 'object_class' not in x:
        raise ValueError(
            'img, mask and object_class required in the dict input.')

    if not isinstance(x['img'], np.ndarray):
        raise ValueError('ndarray type img object required.')
    if not isinstance(x['mask'], np.ndarray):
        raise ValueError('ndarray type mask object required.')
    if not isinstance(x['object_class'], (list,)):
        raise ValueError('list type object_class required.')

    n_classes, n_colors = c.num_classes, c.num_colors
    im = x['img']
    dims = im.shape
    if n_colors == 1:
        if len(dims) != 2:
            raise ValueError('2 dimensional image required.')
    else:
        if len(dims) != 3:
            raise ValueError('3 dimensional image required.')

    if n_colors == 1:
        if len(dims) != 2:
            raise ValueError('2 dimensional image required.')
    else:
        if len(dims) != 3:
            raise ValueError('3 dimensional image required.')

    x_mask = x['mask']
    dims_mask = x_mask.shape

    if len(dims_mask) != 2 or dims_mask[0] != dims[0] or dims_mask[1] != dims[1]:
        raise ValueError('same mask shape and image shape required.')

    mask_unique_val = np.unique(x_mask)
    if not issubclass(mask_unique_val.dtype.type, np.integer):
        raise ValueError('int type mask value required.')

    object_class_list = x['object_class']
    if set(object_class_list) > set(range(0, n_classes)):
        raise ValueError('object classes between 0 and num_classes required')

    return


def validate_combined_image(x, c):
    """This function validates a 'combined image'.  A 'combined image' is a numpy
    array that contains both input and output information, ready for further
    preprocessing and eventually neural network training (although we'll split it
    up before we actually train the network.

    A combined image should be a numpy array with shape (num_channels, height, width),
    where 'num_channels' equals num_colors + num_classes + num_offsets
    where num_colors, num_classes and num_offsets are derived from the
    configuration object 'c'.

    The meaning of the combined image is as follows:
      x[0:num_colors,...] is the input image
      x[num_colors:,...] is the 'positive labels' for
          each class or offset, which will be 1 if it's that class or if
          it's the same object at that offset, and 0 otherwise.
    """
    validate_config(c)

    if not isinstance(x, np.ndarray):
        raise ValueError('x of numpy array type required.')

    dims = x.shape
    if len(dims) != 3:
        raise ValueError('3 dimensional image required.')

    n_colors = c.num_colors
    n_classes = c.num_classes
    n_offsets = len(c.offsets)

    dim = n_colors + n_classes + n_offsets
    if dims[0] != dim:
        raise ValueError(
            'first dimension of np.array should match with num_colors + num_classes + num_offsets)')

    # random check
    k = np.random.randint(n_colors, dims[0])
    i = np.random.randint(0, dims[1])
    j = np.random.randint(0, dims[2])
    if not (x[k, i, j] == 0 or x[k, i, j] == 1):
        raise ValueError('unique values 0, 1 expected)')
    return
