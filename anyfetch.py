#!/usr/bin/env python
# encoding: utf-8

import sys

from workflow import Workflow, web
from requests import Requests


def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`
    # Your imports here if you want to catch import errors
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`
    # import somemodule
    # import anothermodule
    # Get args from Workflow, already in normalised Unicode
    args = wf.args

    # Do stuff here ...

    json = web.get('https://localhost:3000/app/documents?data=%7B%22sessionId%22%3A%22fake_session_id%22%2C%22salesFetchURL%22%3A%22https%3A%2F%2Flocalhost%3A3000%22%2C%22instanceURL%22%3A%22https%3A%2F%2Feu0.salesforce.com%22%2C%22context%22%3A%7B%22templatedDisplay%22%3A%22Matthieu%20Bacconnier%22%2C%22templatedQuery%22%3A%22Matthieu%20Bacconnier%22%2C%22recordId%22%3A%220032000001DoV22AAF%22%2C%22recordType%22%3A%22Contact%22%7D%2C%22user%22%3A%7B%22id%22%3A%2200520000003RnlGAAS%22%2C%22name%22%3A%22mehdi%40anyfetch.com%22%2C%22email%22%3A%22tanguy.helesbeux%40insa-lyon.fr%22%7D%2C%22organization%22%3A%7B%22id%22%3A%2200D20000000lJVPEA2%22%2C%22name%22%3A%22AnyFetch%22%7D%2C%22hash%22%3A%22ZS5ZybJaJPiPAvPms9DNw4Nd2y0%3D%22%7D').json()

    documents = json['documents']['data']

    # Add an item to Alfred feedback
    for document in documents:
        wf.add_item(document['id'], u'Item subtitle')

    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
