import io

from wand.image import Image


def _thumbnail(image_obj, width, height, **options):
    img_format = options['format']
    quality = options['quality']

    img_file = io.BytesIO()

    img = Image(file=image_obj)
    original_width, original_height = img.size
    new_width, new_height = width, height
    # Preserves the aspect ratio fit to new height
    if width == 0:
        new_width = int(original_width * (new_height / original_height))
    # Preserves the aspect ratio fit to new width
    if height == 0:
        new_height = int(original_height * (new_width / original_width))
    # If desired width and/or height is larger than original ones, shrinks it
    # If not, enlarges it
    if (new_width > original_width) or (new_height > original_height):
        img.transform(str(new_width) + 'x' + str(new_height) + '<')
    else:
        img.transform(str(new_width) + 'x' + str(new_height) + '>')
    img.format = img_format
    img.compression_quality = quality
    img.save(file=img_file)
    img_file.seek(0)
    return img_file


def _resize(image_obj, width, height, **options):
    img_format = options['format']
    upscale = options['upscale']
    quality = options['quality']

    img_file = io.BytesIO()

    img = Image(file=image_obj)
    original_width, original_height = img.size
    new_width, new_height = width, height
    # Stretchs or fits the width with desired width
    if width < original_width or upscale:
        new_width = width
    # Stretchs or fits the height with desired height
    if (height < original_height) or upscale:
        new_height = height
    # Preserves the aspect ratio fit to new height
    if width == 0:
        new_width = int(original_width * (new_height / original_height))
    # Preserves the aspect ratio fit to new width
    if height == 0:
        new_height = int(original_height * (new_width / original_width))
    img.resize(new_width, new_height)
    img.format = img_format
    img.compression_quality = quality
    img.save(file=img_file)
    img_file.seek(0)
    return img_file


def _flip(image_obj, direction, **options):
    img_format = options['format']
    quality = options['quality']

    img_file = io.BytesIO()

    img = Image(file=image_obj)
    if direction == 'v':
        img.flip()
    if direction == 'h':
        img.flop()
    img.format = img_format
    img.compression_quality = quality
    img.save(file=img_file)
    img_file.seek(0)
    return img_file


def _rotate(image_obj, degree, **options):
    img_format = options['format']
    quality = options['quality']

    img_file = io.BytesIO()

    img = Image(file=image_obj)
    img.rotate(degree)
    img.format = img_format
    img.compression_quality = quality
    img.save(file=img_file)
    img_file.seek(0)
    return img_file


def transform(mode, image_obj, param_set):
    if mode == 'thumbnail':
        return _thumbnail(image_obj, param_set.width, param_set.height, **param_set.options)
    if mode == 'resize':
        return _resize(image_obj, param_set.width, param_set.height, **param_set.options)
    if mode == 'flip':
        return _flip(image_obj, param_set.direction, **param_set.options)
    if mode == 'rotate':
        return _roate(image_obj, param_set.degree, **param_set.options)
