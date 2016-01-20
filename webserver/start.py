import BaseHTTPServer
from urlparse import urlparse
from functools import reduce
from operator import add
import redis

PORT = 8000
redis_client = None

class TempRequestHandler ( BaseHTTPServer.BaseHTTPRequestHandler ):
    def do_GET ( self ):
        parsedreq = urlparse(self.path)
        xformedpath = parsedreq.path.replace('/', '_')
        try:
            html = TempRequestHandler.__dict__[xformedpath](parsedreq.query)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
        except KeyError:
            self.send_error(404, "Endpoint '%s' not found" % xformedpath)
        except Exception as e:
            self.send_error(500, "Exception: %s" % e)

    def _temp_list ( query ):
        timestamps = redis_client.hgetall("aggregatedtempdata")
        html = "<html><h1>Today's average temperatures</h1>" + (
            "<table>%s</table></html>" % reduce(
                add,
                map(lambda ts_tr: "<tr><td>%d</td><td>%d</td></tr>" % ts_tr,
                    timestamps.items()),
                ""
            )
        )
        return(html)

    def _temp ( query ):
        assert(query)
        time = int(query.split('=')[-1])
        temp = redis_client.hget("aggregatedtempdata", time)
        html = "<html><h1>Average temperature at %d hours: %d</h1></html>" \
            % (time, temp)
        return(html)
    
if __name__ == "__main__":
    redis_client = redis.Redis.from_url(os.environ['REDIS_URI'])
    httpd = BaseHTTPServer.HTTPServer(("", PORT), TempRequestHandler)
    print("Serving temperature readings at port %d" % int(PORT))
    httpd.serve_forever()
