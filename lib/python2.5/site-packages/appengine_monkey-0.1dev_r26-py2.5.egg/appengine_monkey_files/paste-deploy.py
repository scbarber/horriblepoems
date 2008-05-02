#!/usr/bin/env python

CONF_FILE = 'development.ini'

import sys
import os
import site
import wsgiref.handlers

try:
    here = os.path.dirname(__file__)
    site_packages = os.path.join(here, 'lib', 'python2.5', 'site-packages')
    site.addsitedir(site_packages)
    import appengine_monkey
    CONF_FILE = 'config:' + os.path.join(here, CONF_FILE)
    from paste.deploy import loadapp
    app = loadapp(CONF_FILE)
except:
    import traceback
    print 'Content-type: text/plain'
    print
    print 'Error loading application:'
    traceback.print_exc(file=sys.stdout)
    exc_value = sys.exc_info()[1]
    if isinstance(exc_value, ImportError):
        print
        print 'sys.path:'
        for path in sys.path:
            print ' ', path
else:
    def main():
        ## FIXME: set multiprocess based on whether this is the dev/SDK server
        wsgiref.handlers.BaseCGIHandler(sys.stdin, sys.stdout, sys.stderr, os.environ,
                                        multithread=False, multiprocess=False).run(app)

    if __name__ == '__main__':
        main()
