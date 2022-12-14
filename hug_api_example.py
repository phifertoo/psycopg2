"""A basic (single function) API written using Hug."""
import hug

import redis
"""
Make sure you have redis installed via pip and redis-cli can connect
example add data first: http://127.0.0.1:8000/redis_add?ape=123456&rname=phrase
example call http://127.0.0.1:8000/redis_call?ape=123456&rname=phrase
"""

r = redis.StrictRedis(host='127.0.0.1', port=6379)


@hug.get('/happy_birthday')
def happy_birthday(name, age: hug.types.number = 1):
    """Says happy birthday to a user."""
    return "Happy {age} Birthday {name}!".format(**locals())


@hug.get('/redis_call')
def a_redis_call(rname, ape=1):
    """Simple redis call."""
    if ape == 1:
        return "no valid api key specified, nice try though".format(**locals())
    if r.sismember('ape', ape) != 1:
        return "no valid api key specified, nice try though".format(**locals())
    else:
        coolness = r.get(rname).decode('utf8')
        r.decr(ape)
        numleft = r.get(str(ape))
        print(numleft)
        return "Authenticated w {ape}. You have {numleft} queries left. This\
             is the {rname} value you requested: {coolness}".format(**locals())


@hug.get('/redis_add')
def add_redis(rname, ape=1):
    """Add to redis int."""
    r.sadd('ape', int(ape))
    r.set(ape, 1000)
    r.set(rname, 'a nice value here')
    return "added successfully".format(**locals())
