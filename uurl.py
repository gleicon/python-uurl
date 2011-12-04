from bottle import route, redirect, run, debug, send_file, abort, request, ServerAdapter, template, response
import redis
import json
from redis_util import _get_url_stats_by_uid, _update_encoded_url_data, _update_url_data, _get_url_by_uid
import os
if len(os.path.dirname(__file__)) > 1: os.chdir(os.path.dirname(__file__))


BASE_URL = "http://chu.pe/"
STATIC_ROOT_PATH = "static/"

redis_cli = redis.Redis()
if BASE_URL[-1] is not '/': BASE_URL = BASE_URL + '/'

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
        ip = ref = None
    _update_encoded_url_data(redis_cli, uid, ip, ref)
    redirect(url)

@route('/s/:uid')
def stats(uid):
    try:
        jc = request.GET['jsoncallback']
    except Exception, e:
        jc = None
    stats = _get_url_stats_by_uid(redis_cli, uid)
    response.content_type="application/json"
    if jc != None: return "%s(%s)"% (jc, json.dumps(stats))
    return json.dumps(stats)

@route('/url', method='POST')
def post_url():
    url = request.POST['url']
    try:
        custom_url = request.POST['custom_url']
    except Exception, e:
        custom_url = None
    if custom_url == "": custom_url = None
    if url != None and len(url) > 1:
        if url.find(BASE_URL) > -1: abort(404, 'invalid url')
        if url.find('http') < 0: url = "http://%s" % url
        uurl = _update_url_data(redis_cli, url, custom_url)
        if uurl == None: abort(404, 'empty request')
        response.content_type = "application/json"
        return '{"uurl":%s, "url": "%s", "base_url": "%s"}' % (uurl, url, BASE_URL)
    else:
        abort(500, "empty url parameter")

class GEventServerAdapter(ServerAdapter):
    def run(self, handler):
        from gevent import monkey
        monkey.patch_socket()
        from gevent.wsgi import WSGIServer
        WSGIServer((self.host, self.port), handler).serve_forever()


run(host='localhost', port=14000, server=GEventServerAdapter)
