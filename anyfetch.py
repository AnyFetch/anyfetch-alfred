#!/usr/bin/env python
# encoding: utf-8

import sys

from workflow import Workflow
import requests

def get_documents(search):
    """Retrieve documents from api.anyfetch.com

    Returns a list of document dictionaries.

    """
    url = 'https://api.anyfetch.com/documents'
    r = requests.get('https://api.anyfetch.com/documents?search='+search, auth=('tanguyhelesbeux@gmail.com', 'bitecouille'))

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
    query = args[0]

    documents = get_documents(query);



    # Add items to Alfred feedback
    if len(documents) == 0:
        wf.add_item('No results', 'We could not fetch any document for \'' + query + '\'')
    else:
        for document in documents:
            type = document['document_type']['name'].capitalize()
            provider = document['provider']['client']['name']
            wf.add_item(title=document['_type'],
                             subtitle= type + ' from ' + provider,
                             arg=document['identifier'],
                             valid=True,
                             icon='./icon.png')


    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
