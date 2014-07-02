# -*- coding: utf-8 -*-

"""TCP Server Sample"""

import gevent
from gevent.server import StreamServer
from endpoint import EndPoint


class Observer(EndPoint):
    def on_connection_closed(self):
        print("Observer {0} closed the connecton".format(id(self)))

    def on_connection_lost(self):
        print("Observer {0} lost".format(id(self)))

    def on_data(self, data):
        pass


class ObserverManager(gevent.Greenlet):
    def __init__(self, port):
        self.port = port
        gevent.Greenlet.__init__(self)

    def _connection_handler(self, client, address):
        print("New Connection From {0}".format(address))
        observer = Observer(client)
        observer.start()

    def _run(self):
        print("TCP Observer Listen at port {0}".format(self.port))
        server = StreamServer(('0.0.0.0', self.port), self._connection_handler)
        server.serve_forever()


if __name__ == "__main__":
    ob = ObserverManager(7000) # 这个是通过协程执行的,所以下面需要一个协程join等待
    ob.start()
    print "....."
    def loop():
        while True:
            gevent.sleep(600)
    lp = gevent.spawn(loop)
    lp.join()