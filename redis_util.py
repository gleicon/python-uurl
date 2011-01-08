import base62
from datetime import datetime
import time

# auxiliary funcs
UNIQUE_COUNTER = 'URL:UUID'
URL_MASK = 'URL:%s'
ENCODED_URL_REF_LIST = 'URL:UID:REFERERS:%s'
ENCODED_URL_VIS_LIST = 'URL:UID:VISITORS:%s'
ENCODED_URL_DICT = 'URL:UID:DATA:%s'
ENCODED_URL_STATS_DICT = 'URL:UID:STATS:%s'
ENCODED_URL_MASK = 'URL:UID:MASK:%s'

def _update_url_data(redis_cli, url):
    k = URL_MASK % url
    u = redis_cli.get(k)
    if u == None: 
        id = _get_uuid(redis_cli)
        uid = base62.base62_encode(id)
        redis_cli.set(k, uid)
        redis_cli.set(ENCODED_URL_MASK % uid, url)
        t = int(time.time())
        k = ENCODED_URL_DICT % uid
        redis_cli.hset(k, 'date_creation', t)
        redis_cli.hset(k, 'url', url)
        return uid
    return u

def _get_uuid(redis_cli):
    return redis_cli.incr(UNIQUE_COUNTER)

def _get_url_by_uid(redis_cli, uid):
    return redis_cli.get(ENCODED_URL_MASK % uid)

def _update_encoded_url_data(redis_cli, uid, ip=None, ref=None):
    # being optimistic to save a 
    # roundtrip check for existing key
    k = ENCODED_URL_DICT % uid
    redis_cli.hincrby(k, 'clicks', 1)
    
    dt = datetime.now()
    dk = '%s.%s.%s.%s' % (dt.year, dt.month, dt.day, dt.hour)
    ks = ENCODED_URL_STATS_DICT % uid
   
    redis_cli.hincrby(ks, dk, 1)
    if ref != None: redis_cli.lpush(ENCODED_URL_REF_LIST % uid, ref)
    if ip != None: redis_cli.lpush(ENCODED_URL_VIS_LIST % uid, vis)

def _get_url_stats_by_uid(redis_cli, uid):
    st = redis_cli.hgetall(ENCODED_URL_DICT % uid)
    if st == None: return None
    
    ss = redis_cli.hgetall(ENCODED_URL_STATS_DICT % uid)

    st['referers'] = redis_cli.lrange(ENCODED_URL_REF_LIST % uid, 0, -1)
    st['visitors'] = redis_cli.lrange(ENCODED_URL_VIS_LIST % uid, 0, -1)
    st['cph'] = ss

    return st

