#!/usr/bin/env python
# encoding: utf-8

import sys, re, os, requests

from workflow import Workflow


def get_documents(query):
    """
    Retrieve documents from api.anyfetch.com

    Returns a list of document dictionaries.

    """

    env = os.getenv('ANYFETCH_ENV', 'api')
    token = os.getenv('ANYFETCH_TOKEN')

    r = requests.get('https://{0}.anyfetch.com/documents?search={1}'.format(env, query),
                      headers={'Authorization': 'token {0}'.format(token)})

    return r.json()

def html_escape(string):
    return re.sub('<(?:"[^"]*"[\'"]*|\'[^\']*\'[\'"]*|[^\'">])+>', '', string)


def main(wf):
    args = wf.args
    query = args[0]

    json = wf.cached_data(query, lambda: get_documents(query), max_age=600)

    documents = json['data']

    # Add items to Alfred feedback
    if len(documents) == 0:
        title = 'No results'
        subtitle = 'We could not fetch any document for \'{0}\''.format(query)
        wf.add_item(title, subtitle)
    else:
        for document in documents:
            type = document['document_type']['name']
            provider = document['provider']['client']['name']

            # TODO: rendered_title
            title = 'Unknown'
            if document['data'].get('title') is not None:
                title = document['data']['title']
            elif document['data'].get('subject') is not None:
                title = document['data']['subject']
            elif document['data'].get('name') is not None:
                title = document['data']['name']

            title = html_escape(title)

            action = None
            if document['actions'].get('show') is not None:
                action = document['actions']['show']
            elif document['actions'].get('reply') is not None:
                action = document['actions']['reply']
            elif document['actions'].get('download') is not None:
                action = document['actions']['download']

            subtitle = '{0} from {1}'.format(type.capitalize(), provider)

            wf.add_item(title=title,
                        subtitle=subtitle,
                        arg=action,
                        valid=True,
                        icon='./icons/{0}.png'.format(type))

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
