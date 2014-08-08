#!/usr/bin/env python
# encoding: utf-8

import sys

from workflow import Workflow

def main(wf):
	key = wf.args[0]
	value = wf.args[1]
	wf.settings[key] = value
	wf.logger.debug(wf.settings)
	wf.clear_cache()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
