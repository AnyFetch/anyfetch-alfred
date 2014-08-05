#!/usr/bin/env python
# encoding: utf-8

import sys
import requests

from workflow import Workflow

def get_documents(query):
    """

    Retrieve documents from api.anyfetch.com

    Returns a list of document dictionaries.

    """

    r = requests.get('https://api.anyfetch.com/documents?search=' + query,
        auth=('tanguyhelesbeux@gmail.com', 'bitecouille'))

    # Parse the JSON returned by pinboard and extract the posts
    return r.json()

def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`
    # Your imports here if you want to catch import errors
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`
    # import somemodule
    # import anothermodule
    # Get args from Workflow, already in normalised Unicode
    args = wf.args
    query = args[0]

    json = wf.cached_data(query, lambda: get_documents(query), max_age=600)

    documents = json['data']

    # Add items to Alfred feedback
    if len(documents) == 0:
        wf.add_item('No results', 'We could not fetch any document for \'' + query + '\'')
    else:
        for document in documents:
            type = document['document_type']['name'].capitalize()
            provider = document['provider']['client']['name']

            # TODO: rendered_title
            title = 'Unknown'
            if document['data'].get('title') is not None:
                title = document['data']['title']
            elif document['data'].get('subject'):
                title = document['data']['subject']
            elif document['data'].get('name'):
                title = document['data']['name']

            wf.add_item(title=title,
                        subtitle=type+' from '+provider,
                        arg=document['identifier'],
                        valid=True,
                        icon='./icon.png')

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
