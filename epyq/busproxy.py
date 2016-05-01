#!/usr/bin/env python3.4

# TODO: get some docstrings in here!

import can
import threading
import time

from epyq.canneo import QtCanListener

# See file COPYING in this source tree
__copyright__ = 'Copyright 2016, EPC Power Corp.'
__license__ = 'GPLv2+'


class BusProxy:
    # This has very limited thread safety.  Only recv may be called
    # from another thread.
    def __init__(self, bus=None):
        self.bus = bus

        self.lock = threading.Lock()

        try:
            self._notifier = self.bus.notifier()
        except AttributeError:
            self._notifier = NotifierProxy(bus=self)

    def notifier(self):
        return self._notifier

    def recv(self, timeout=None):
        # This is called from the Notifier thread so it has to be protected

        self.lock.acquire()

        result = None

        bus_is_none = self.bus is None

        if not bus_is_none:
            result = self.bus.recv(timeout=timeout)

        self.lock.release()

        if bus_is_none and timeout is not None:
            time.sleep(timeout)

        return result

    def send(self, msg):
        if self.bus is not None:
            # TODO: I would use message=message (or msg=msg) but:
            #       https://bitbucket.org/hardbyte/python-can/issues/52/inconsistent-send-signatures
            return self.bus.send(msg)

    def shutdown(self):
        pass

    def flash(self):
        if self.bus is not None:
            return self.bus.flash()

    def set_bus(self, bus=None):
        self.lock.acquire()

        if self.bus is not None:
            self.bus.shutdown()
        self.bus = bus

        self.lock.release()


class NotifierProxy(QtCanListener):
    def __init__(self, bus, listeners=[], parent=None):
        QtCanListener.__init__(self, receiver=self.message_received, parent=parent)

        self.bus = bus
        self.listeners = set(listeners)

        self.notifier = can.Notifier(self.bus, [self], timeout=0.1)

    def message_received(self, message):
        for listener in self.listeners:
            listener.message_received_signal.emit(message)

    def add(self, listener):
        self.listeners.add(listener)

    def discard(self, listener):
        self.listeners.discard(listener)

    def remove(self, listener):
        self.listeners.remove(listener)


if __name__ == '__main__':
    import sys

    print('No script functionality here')
    sys.exit(1)     # non-zero is a failure
