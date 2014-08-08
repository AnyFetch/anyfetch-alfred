#!/usr/bin/env python
# encoding: utf-8

import sys

from workflow import Workflow

def main(wf):
    key = wf.args[0]
    value = wf.args[1]

    title = 'Set new {0} to {1}'.format(key, value)
    arg = '{0} {1}'.format(key, value)
    wf.add_item(title=title,
                subtitle='Press ENTER to validate',
                arg=arg,
                valid=True,
                icon='icons/settings.png')

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
