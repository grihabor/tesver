import logging
import socket

logging.basicConfig(level=logging.INFO)

import os

from flask import Flask, request, jsonify, render_template
from flask_bootstrap import Bootstrap

from models import Repository
from tester.script import run_bash_script
from utils import (
    DIR_SRC, 
    safe_get_repository,
    process_details,
    UnifiedResponse
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder='../app/templates')
Bootstrap(app)

ARG_URL = 'url'
ARG_IDENTITY_FILE = 'identity_file'
ARG_REPOSITORY_ID = 'repository_id'
ARG_USER_ID = 'user_id'

DIR_TESTER = os.path.join(DIR_SRC, 'tester')
FILE_CLONE_SH = os.path.join(DIR_TESTER, 'clone.sh')
FILE_TEST_SH = os.path.join(DIR_TESTER, 'test.sh')


@app.route('/')
def index():
    return 'Internal tester service'



def routes():
    routes = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            routes[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return routes





def missing(arg):
    return 'Missing argument: {}'.format(arg)


def _clone_repo():
    if ARG_URL not in request.args:
        return UnifiedResponse(
            details=missing(ARG_URL), 
            result='fail'
        )
    if ARG_IDENTITY_FILE not in request.args:
        return UnifiedResponse(
            details=missing(ARG_IDENTITY_FILE), 
            result='fail'
        )

    url = request.args[ARG_URL]
    parsed = parse_repo_url(url)
    identity_file = request.args[ARG_IDENTITY_FILE]

    if parsed is None:
        return UnifiedResponse(
            result='fail', 
            details='URL parsing error'
        )

    result = run_bash_script(
        FILE_CLONE_SH,
        identity_file=identity_file,
        git=Git(**parsed)
    )
    
    return result


@app.route('/clone_repo', methods=['GET'])
def clone_repo():
    return jsonify(dict(_clone_repo()))



def main():
    logger.info('Starting tester...')
    app.run('0.0.0.0', 6000, debug=True)


if '__main__' == __name__:
    main()
