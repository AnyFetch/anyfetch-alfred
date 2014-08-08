#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import os
import requests

from workflow import Workflow, ICON_ERROR, ICON_ACCOUNT

FILTER_KEYWORDS = {
    'mail': '5252ce4ce4cfcd16f55cfa3f',
    'email': '5252ce4ce4cfcd16f55cfa3f',
    'PDF': '5252ce4ce4cfcd16f55cfa3c',
    'pdf': '5252ce4ce4cfcd16f55cfa3c',
    'image': '5252ce4ce4cfcd16f55cfa3d',
    'picture': '5252ce4ce4cfcd16f55cfa3d',
    'contact': '5252ce4ce4cfcd16f55cfa3a',
    'event': '5252ce4ce4cfcd16f55cfa40',
    'file': '5252ce4ce4cfcd16f55cfa3b'
}


def get_documents(query, filter):
    """
    Retrieve documents from api.anyfetch.com

    Returns a list of document dictionaries.

    """

    env = os.getenv('ANYFETCH_ENV', 'api')
    token = os.getenv('ANYFETCH_TOKEN')

    if token is None:
        return None

    url = 'https://{0}.anyfetch.com/documents'.format(env)
    params = {
        'search': query,
        'render_templates': 1
    }
    headers = {
        'Authorization': 'token {0}'.format(token)
    }


    if filter is not None:
        query = query[len(filter):]
        params['document_type'] = FILTER_KEYWORDS[filter]


    r = requests.get(url, headers=headers, params=params)

    if r.status_code != 200:
        return None

    return r.json()


def html_escape(string):
    return re.sub('<(?:"[^"]*"[\'"]*|\'[^\']*\'[\'"]*|[^\'">])+>', '', string)


def main(wf):
    args = wf.args
    query = args[0]

    words = query.split(' ')
    wf.logger.debug(words)
    wf.logger.debug(FILTER_KEYWORDS.keys())
    filter = [x for x in words if x in FILTER_KEYWORDS.keys()]
    filter = filter[0] if len(filter) else None
    wf.logger.debug(filter)

    json = wf.cached_data(query, lambda: get_documents(query, filter), max_age=600)

    if json is None:
        wf.add_item(title='Invalid token',
                    subtitle='Edit workflow to provide a valid token',
                    arg=None,
                    valid=True,
                    icon=ICON_ERROR)

        # Send output to Alfred
        wf.send_feedback()

    else:
        documents = json['data']

        # Add items to Alfred feedback
        if len(documents) == 0:
            title = 'No results'
            subtitle = 'Could not fetch any document for \'{0}\''.format(query)
            wf.add_item(title, subtitle, valid=False)
        else:
            for document in documents:
                type = document['document_type']['name']
                provider = document['provider']['client']['name']

                title = document.get('rendered_title')
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

        wf.add_item(title='Contact us',
                    subtitle='Send an email to contact@anyfetch.com',
                    arg='mailto:contact@anyfetch.com',
                    valid=True,
                    icon=ICON_ACCOUNT)

        # Send output to Alfred
        wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
