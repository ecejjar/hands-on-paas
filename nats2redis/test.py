import json
import random
import unittest
import start

class RedisMock ( object ):
    def __init__ ( self, name ):
        self.name = name
        self.aggregatedtempdata = {}

    def hset ( self, name, key, val ):
        if name == self.name:
            self.aggregatedtempdata[key] = val


class TestHandle ( unittest.TestCase ):

    def setUp ( self ):
        start.redis_client = RedisMock("aggregatedtempdata")
        start.accutemp = []
        start.curhour = None
        
    def test1h ( self ):
        tempreadings = random.sample(xrange(-2000, +5000), 60)
        averagetemp = sum(tempreadings)/len(tempreadings)
        timestamped_tempreadings = zip(
            map(lambda mn: "05:%d:00" % mn, range(60)), tempreadings)
        for ts_tr in timestamped_tempreadings:
            start.handle(json.dumps({ "time": ts_tr[0], "temp": ts_tr[1] }))
        start.handle(json.dumps({ "time": "06:00:00", "temp": 50000 }))
        self.assertEqual(start.redis_client.aggregatedtempdata[5], averagetemp)


if __name__ == "__main__":
    unittest.main()
