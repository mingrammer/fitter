from flask import jsonify
from flask import redirect

from fitter import fitter
from fitter.cachestore.decorators import cache
from fitter.cachestore.decorators import from_cache_store
from fitter.engine.image import transform
from fitter.storage.decorators import from_store_storage


@from_cache_store('show')
@from_store_storage('show')
@cache()
def show_view(hashed, param_set):
    # TODO: Run it on async background. Supports async job
    if fitter.source_storage.exists(param_set.path):
        original_image = fitter.source_storage.get(param_set.path)
        transformed_image = transform(param_set.mode, original_image, param_set)
        fitter.store_storage.save(hashed, transformed_image)

        return jsonify(
            url=fitter.store_storage.generate_url(hashed),
        )
    return jsonify(
        errors='The filepath {} is not found on your source storage'.format(param_set.path)
    )


@from_cache_store('get')
@from_store_storage('get')
@cache()
def get_view(hashed, param_set):
    if fitter.source_storage.exists(param_set.path):
        original_image = fitter.source_storage.get(param_set.path)
        transformed_image = transform(param_set.mode, original_image, param_set)
        fitter.store_storage.save(hashed, transformed_image)

        return jsonify(
            filename=hashed,
            path=fitter.store_storage.get_path(hashed),
            url=fitter.store_storage.generate_url(hashed),
        )
    return jsonify(
        errors='The filepath {} is not found on your source storage'.format(param_set.path)
    )


@from_cache_store('redirect')
@from_store_storage('redirect')
@cache()
def redirect_view(hashed, param_set):
    if fitter.source_storage.exists(param_set.path):
        original_image = fitter.source_storage.get(param_set.path)
        transformed_image = transform(param_set.mode, original_image, param_set)
        fitter.store_storage.save(hashed, transformed_image)

        # Add header for image format
        return redirect(fitter.store_storage.generate_url(hashed), code=302)
    return jsonify(
        errors='The filepath {} is not found on your source storage'.format(param_set.path)
    )
