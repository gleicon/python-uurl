from bottle import route, redirect, run, debug, send_file, abort, request, ServerAdapter, template
import redis
import json
from redis_util import _get_url_stats_by_uid, _update_encoded_url_data, _update_url_data, _get_url_by_uid
import os
if len(os.path.dirname(__file__)) > 1: os.chdir(os.path.dirname(__file__))

BASE_URL = "http://7co.cc/"

redis_cli = redis.Redis()

@route('/:uurl!')
def uurl_stats(uurl):
    return template('stats', uurl = uurl)

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
    if jc != None: return "%s(%s)"% (jc, json.dumps(stats))
    return json.dumps(stats)

@route('/url', method='POST')
def post_url():
    url = request.POST['url']
    if url != None and len(url) > 1:
        if url.find(BASE_URL) > -1: abort(404, 'invalid url')
        uurl = _update_url_data(redis_cli, url)
        if uurl == None: abort(404, 'empty request')
        return template('resp', uurl=uurl, base_url=BASE_URL)
    else:
        redirect('/')

@route('/')
@route('/:filename#.*#')
def static_file(filename='index.html'):
    send_file(filename, root='static/')

class GEventServerAdapter(ServerAdapter):
    def run(self, handler):
        from gevent import monkey
        monkey.patch_socket()
        from gevent.wsgi import WSGIServer
        WSGIServer((self.host, self.port), handler).serve_forever()

debug(True)

run(host='localhost', port=10000, server=GEventServerAdapter)
