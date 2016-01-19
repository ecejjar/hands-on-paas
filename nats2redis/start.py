from time import sleep
import json
import pynats
import redis

accutemp = []
curhour = None
redis_client = None

def handle ( tempdata ):
    global curhour, accutemp
    parsedtempdata = json.loads(tempdata)
    nxthour = int(parsedtempdata["time"].split(':'))
    if curhour is None:
        curhour = nxthour
    elif nxthour > curhour:
        redis_client.hset(
            "aggregatedtempdata", curhour, sum(accutemp)/len(accutemp))
        accutemp = []
        curhour = nxthour
    accutemp.append(int(parsedtempdata["temp"]))

if __name__ == "__main__":
    nats_client = pynats.Connection(url=os.environ['NATS_URI'], verbose=True)
    nats_client.connect()
    nats_client.subscribe("tempdata", handle)
    redis_client = redis.Redis.from_url(os.environ['REDIS_URI'])
    while True:
        sleep(1)
