from bottle import route, redirect, run, debug, send_file, abort, request, ServerAdapter, template, response
from time import gmtime, strftime
import redis
import json
import logging
from redis_util import _get_url_stats_by_uid, _update_encoded_url_data, _update_url_data, _get_url_by_uid
import os
if len(os.path.dirname(__file__)) > 1: os.chdir(os.path.dirname(__file__))

logger = logging.getLogger('uurl')
hdlr = logging.FileHandler('/var/log/uurl_%d.log' % os.getpid())
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

BASE_URL = "http://chu.pe/"
STATIC_ROOT_PATH = "static/"
MAX_REQ_PER_MIN = 10

p = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_cli = redis.Redis(connection_pool = p)

if BASE_URL[-1] is not '/': BASE_URL = BASE_URL + '/'

def throttle(route, addr): # enable if your proxy can pass the right client ip ADDR
    if route is None or addr is None: return False
    t = strftime("%d:%m:%Y:%H:%M:", gmtime())
    k = "%s:%s:%s" % (t, route, addr)
    c = redis_cli.incr(k)
    if c > MAX_REQ_PER_MIN:
        return False
    return True

@route('/')
@route('/index.html')
@route('/static/:filename#.*[\.css|\.html|\.js|\.png]#')
def static_file(filename='index.html'):
    send_file(filename, root=STATIC_ROOT_PATH)

@route('/:uurl!')
def uurl_stats(uurl):
    return template('stats', uurl = uurl, base_url=BASE_URL)

@route('/:uid')
@route('/u')
@route('/u/:uid')
def url(uid = None):
    if uid == None: abort(404, 'No uid')
    url = _get_url_by_uid(redis_cli, uid)
    if url == None: abort(404, 'No url')
    try:
        ip = request['REMOTE_ADDR']
        ref = request['REFERER']
    except Exception, e:
        logger.error("Exception: %s" % e)
        ip = ref = None
    _update_encoded_url_data(redis_cli, uid, ip, ref)
    logger.info("Request: uid: %s ip: %s ref: %s url: %s" % (uid, ip, ref, url))
    redirect(url)

@route('/s/:uid')
def stats(uid):
    try:
        jc = request.GET['jsoncallback']
    except Exception, e:
        jc = None
    stats = _get_url_stats_by_uid(redis_cli, uid)
    response.content_type="application/json"
    if stats is None:
        abort(404, 'No url')
    else:
        if jc != None: 
            return "%s(%s)"% (jc, json.dumps(stats))
        else:
            return json.dumps(stats)
        
def shorten(url, custom_url):
    if url != None and len(url) > 1:
        if url.find(BASE_URL) > -1: return None
        if url.find('http') < 0: url = "http://%s" % url
        uurl = _update_url_data(redis_cli, url, custom_url)
        return uurl
    else:
        return None

@route('/url')
def quick_link():
    #if throttle('url', request.environ.get('REMOTE_ADDR')) is False: abort(401, "Not allowed - try again later")
    try:
        url = request.GET['url']
    except:
        abort(404, "No url given")
    uurl = shorten(url, None)
    if not uurl: 
        abort(500, "empty or invalid url")
    else: 
        # two options here: render the status page or redirect to it. You might
        # want to redirect to somewhere else passing the new uurl as parameter,
        # etc. Dont forget that the full url == BASE_URL + uurl (+ '!' if you
        # want the status page

        #return template('stats', uurl = uurl, base_url = BASE_URL, url = url)
        redirect(BASE_URL + uurl+"!")

@route('/url', method='POST')
def post_url():
    #if throttle('url', request.environ.get('REMOTE_ADDR')) is False: abort(401, "Not allowed - try again later")
    url = request.POST['url']
    try:
        custom_url = request.POST['custom_url']
    except Exception, e:
        custom_url = None
    if custom_url == "": custom_url = None
    if url != None and len(url) > 1:
        uurl = shorten(url, custom_url)
        response.content_type = "application/json"
        return '{"uurl":"%s", "url": "%s", "base_url": "%s"}' % (uurl, url, BASE_URL)
    else:
        abort(500, "empty url parameter")

class GEventServerAdapter(ServerAdapter):
    def run(self, handler):
        from gevent import monkey
        monkey.patch_socket()
        from gevent.wsgi import WSGIServer
        WSGIServer((self.host, self.port), handler).serve_forever()

# uncomment for nice error 500 and stacktrace messages
#debug(True)
run(host='localhost', port=14000, server=GEventServerAdapter)
