#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import requests

from workflow import Workflow, ICON_ERROR, ICON_CONTACT

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

    env = get_env('api')
    token = get_token()

    if token is None:
        return None

    url = 'https://{0}.anyfetch.com/documents'.format(env)
    params = {
        'search': query,
        'render_templates': 1
    }
    headers = {
        'Authorization': 'Bearer {0}'.format(token)
    }

    if filter is not None:
        params['search'] = query[len(filter):]
        params['document_type'] = [FILTER_KEYWORDS[filter]]

    r = requests.get(url, headers=headers, params=params)

    if r.status_code != 200:
        return None

    return r.json()


def html_escape(string):
    return re.sub('<(?:"[^"]*"[\'"]*|\'[^\']*\'[\'"]*|[^\'">])+>', '', string)


def get_token():
    return wf.settings.get('token')


def get_env(default):
    env = wf.settings.get('env')
    return env if env is not None else default


def send_invalid_token(wf):
    wf.add_item(title='Invalid token',
                subtitle='Edit workflow to provide a valid token',
                arg=None,
                valid=True,
                icon=ICON_ERROR)

    # Send output to Alfred
    wf.send_feedback()


def send_documents(wf, query, documents):
    # Add items to Alfred feedback
    if len(documents) == 0:
        title = 'No results'
        subtitle = 'Could not fetch any document for \'{0}\''.format(query)
        wf.add_item(title, subtitle, valid=False, icon='icons/icon.png')
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
                icon=ICON_CONTACT)

    # Send output to Alfred
    wf.send_feedback()


def main(wf):
    args = wf.args
    query = args[0]

    words = query.split(' ')
    filter = [x for x in words if x in FILTER_KEYWORDS.keys()]
    filter = filter[0] if len(filter) else None

    cacheKey = '{0}:{1}'.format(query, filter)
    fetcher = lambda: get_documents(query, filter)
    json = wf.cached_data(cacheKey, fetcher, max_age=600)

    if json is None:
        send_invalid_token(wf)
    else:
        documents = json['data']
        send_documents(wf, query, documents)


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
