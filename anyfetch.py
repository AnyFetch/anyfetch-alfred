#!/usr/bin/env python
# encoding: utf-8

import sys

from workflow import Workflow, web
import requests

def get_documents():
    """Retrieve documents from api.anyfetch.com

    Returns a list of document dictionaries.

    """
    url = 'https://api.anyfetch.com/documents'
    r = requests.get('https://api.anyfetch.com/documents', auth=('tanguyhelesbeux@gmail.com', 'bitecouille'))

    # Parse the JSON returned by pinboard and extract the posts
    result = r.json()
    documents = result['data']
    return documents

def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`
    # Your imports here if you want to catch import errors
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`
    # import somemodule
    # import anothermodule
    # Get args from Workflow, already in normalised Unicode
    args = wf.args

    documents = get_documents();

    # Add items to Alfred feedback
    for document in documents:
        wf.add_item(document['id'], u'Item subtitle')


    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
