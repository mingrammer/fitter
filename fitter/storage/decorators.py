from functools import wraps

from flask import jsonify
from flask import redirect

from fitter import fitter


def from_store_storage(action):
    def from_store_storage_decorator(func):
        @wraps(func)
        def func_wrapper(hashed, param_set):
            if fitter.store_storage.exists(key=hashed):
                if action == 'show':
                    return jsonify(
                        url=fitter.store_storage.generate_url(hashed)
                    )
                if action == 'get':
                    return jsonify(
                        filename=hashed,
                        path=fitter.store_storage.get_path(hashed),
                        url=fitter.store_storage.generate_url(hashed),
                    )
                if action == 'redirect':
                    return redirect(fitter.store_storage.generate_url(hashed), code=302)
            return func(hashed, param_set)
        return func_wrapper
    return from_store_storage_decorator
