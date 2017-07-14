#!/usr/bin/python

import sys
from signal import signal, SIGINT
from socket import gethostname;

from pymouse import PyMouse

while True:


    try:
        from pymouse import PyMouseEvent


        class event(PyMouseEvent):
            def __init__(self):
                super(event, self).__init__()
                FORMAT = '%(asctime)-15s ' + gethostname() + ' touchlogger %(levelname)s %(message)s'

            def move(self, x, y):
                pass

            def click(self, x, y, button, press):
                if press:
                    print('{ "event": "click", "type": "press", "x": "' + str(x) + '", "y": "' + str(y) + '"}')
                else:
                    print('{ "event": "click", "type": "release", "x": "' + str(x) + '", "y": "' + str(y) + '"}')


        e = event()
        e.capture = False
        e.daemon = False
        e.start()

    except ImportError:
        print('{ "event": "exception", "type": "ImportError", "value": "Mouse events unsupported"}')
        sys.exit()

    m = PyMouse()
    try:
        size = m.screen_size()
        print('{ "event": "start", "type": "size", "value": "' + str(size) + '"}')
    except:
        print('{ "event": "exception", "type": "size", "value": "undetermined problem"}')
        sys.exit()

    try:
        e.join()
    except KeyboardInterrupt:
        e.stop()
        sys.exit()
