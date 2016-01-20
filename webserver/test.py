import urllib2
import BaseHTTPServer
from threading import Timer
import unittest
import start

class RedisMock ( object ):
    def __init__ ( self, name ):
        self.name = name
        self.aggregatedtempdata = {
            0: 20,
            1: 21
        }

    def hgetall ( self, name ):
        if name == self.name:
            return self.aggregatedtempdata
    
    def hget ( self, name, key ):
        if name == self.name:
            return self.aggregatedtempdata[key]


class TestRequestHandler ( unittest.TestCase ):

    def setUp ( self ):
        start.redis_client = RedisMock("aggregatedtempdata")

    def testGetList ( self ):
        def testFunc():
            try:
                f = urllib2.urlopen("http://127.0.0.1:8000/temp/list")
                html = f.read()
                self.assertIn("<tr><td>0</td><td>20</td>", html)
                self.assertIn("<tr><td>1</td><td>21</td>", html)
            finally:
                server.shutdown()

        Timer(1, testFunc).start()
        server.serve_forever()        

    def testGetValue ( self ):
        def testFunc():
            try:
                f = urllib2.urlopen("http://127.0.0.1:8000/temp?time=1")
                html = f.read()
                self.assertIn("1 hours: 21", html)
            finally:
                server.shutdown()

        Timer(1, testFunc).start()
        server.serve_forever()


if __name__ == "__main__":    
    server = BaseHTTPServer.HTTPServer(
        ("127.0.0.1", start.PORT), start.TempRequestHandler)
    unittest.main()
