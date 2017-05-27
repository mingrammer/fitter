from fitter import fitter
from fitter.server.api import upload

if __name__ == '__main__':
    if fitter.config['OPTIONS']['ENABLE_UPLOAD']:
        fitter.add_url_rule('/upload', view_func=upload, methods=['POST'])
    fitter.run('0.0.0.0', port=fitter.config['PORT'])
