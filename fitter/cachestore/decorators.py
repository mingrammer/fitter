from functools import wraps

from flask import jsonify
from flask import redirect

from fitter import fitter


def from_cache_store(action):
    def from_cache_store_decorator(func):
        @wraps(func)
        def func_wrapper(hashed, param_set):
            if fitter.cache_store is not None:
                cached = fitter.cache_store.get(fitter.store_storage.get_path(hashed))
                if cached is not None:
                    if action == 'show':
                        return jsonify(
                            url=cached['url'],
                        )
                    if action == 'get':
                        return jsonify(
                            filename=cached['filename'],
                            path=cached['path'],
                            url=cached['url'],
                        )
                    if action == 'redirect':
                        return redirect(cached['url'], code=302)
            return func(hashed, param_set)
        return func_wrapper
    return from_cache_store_decorator


def cache():
    def cache_decorator(func):
        @wraps(func)
        def func_wrapper(hashed, param_set):
            result = func(hashed, param_set)
            if fitter.cache_store is not None:
                fitter.cache_store.set(hashed, {
                    'filename': hashed,
                    'path': fitter.store_storage.get_path(hashed),
                    'url': fitter.store_storage.generate_url(hashed),
                })
            return result
        return func_wrapper
    return cache_decorator
