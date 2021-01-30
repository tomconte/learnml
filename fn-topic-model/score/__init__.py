import json
import logging
import os
import sys

import azure.functions as func

from . import score


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('launching score in ' + os.getcwd())
    score.init()
    req_body = req.get_json()
    return json.dumps(score.run(json.dumps(req_body)))
