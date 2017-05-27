from functools import wraps

from flask import g
from flask import jsonify
from flask import request

from fitter import fitter
from fitter.server.paramset import ParamSet
from fitter.utils.file import generate_hash
from fitter.views.action import get_view
from fitter.views.action import redirect_view
from fitter.views.action import show_view


def validate_params(api):
    """A decorator for validating the parameters like a middleware

    get:
        parameters:
            mode:
                description: The operation type
                :type: string
                options:
                    - thumbnail: Generates an image for thumbnails (resized and cropped)
                    - resize: Resizes the image with desired size
                    - flip: Flips the image with given direction
                    - rotate: Rotates the image with desired degree
                required
            path:
                description: The path of image which is on source storage
                :type: string
            format:
                description: The desired format of the image
                :type; string
                options:
                    - png
                    - jpg
                    - jpeg
                default: png
            width (w):
                description: The desired width of the image
                :type: int
            height (h):
                description: The desired height of the image
                :type: int
            upscale:
                :description: Whether if upscale the image has size smaller than desired size
                :type: boolean
                default: true
            quality:
                description: The desired quality of image
                type: int
                default: 100
            direction:
                description: The desired direction to flip the image
                :type: string
                options:
                    - h (horizontal)
                    - v (vertical)
            degree:
                description: The desired degree to rotate the image
                :type: float
    """

    @wraps(api)
    def validate_params_decorator(*args, **kwargs):
        param_fetcher = request.args.get

        mode = param_fetcher('mode')
        path = param_fetcher('path')
        img_fotmat = param_fetcher('format', 'png')
        width = param_fetcher('width')
        height = param_fetcher('height')
        upscale = param_fetcher('upscale', 'true')
        quality = param_fetcher('quality', '100')
        direction = param_fetcher('direction')
        degree = param_fetcher('degree')

        param_set = ParamSet(
            mode=mode,
            path=path,
            img_format=img_fotmat,
            width=width,
            height=height,
            upscale=upscale,
            quality=quality,
            direction=direction,
            degree=degree,
        )

        if param_set.validate():
            g.param_set = param_set
            return api(*args, **kwargs)
        return jsonify(errors=param_set.errors)
    return validate_params_decorator


@validate_params
def upload():
    """Upload an image and generate an image with given conditions

    If width or height value is 0, the image aspect raio will be preserved

    post:
        parameters:
            image:
                description: The image to generate resized one. needed only if 'action' is 'upload'
                type: file object
    """
    pass


@fitter.route('/show', methods=['GET'])
@validate_params
def generate_and_show():
    """Get the generated image information asynchronously

    It is Useful when use in <img> tag
    """
    param_set = g.param_set
    hashed = generate_hash(param_set)
    return show_view(hashed, param_set)


@fitter.route('/get', methods=['GET'])
@validate_params
def generate_and_get():
    """Get the generated image information"""
    param_set = g.param_set
    hashed = generate_hash(param_set)
    return get_view(hashed, param_set)


@fitter.route('/redirect', methods=['GET'])
@validate_params
def generate_and_redirect():
    """Redirect to generated image url"""

    param_set = g.param_set
    hashed = generate_hash(param_set)
    return redirect_view(hashed, param_set)
