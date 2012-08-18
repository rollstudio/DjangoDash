from urlparse import urlparse

from django.conf import settings

from pymongo import Connection

mongodb_string = getattr(settings, 'MONGODB_STRING', '')
s = urlparse(mongodb_string)

connection = Connection(mongodb_string)

db = connection.hit_counter

db.authenticate(s.username, s.password)

hits = db.hits
single_hits = db.single_hits


def insert_hit(content_type, id, ip):
    h = hits.find({
        'contentType': content_type,
        'objId': id,
        'ip': ip
    })

    if h.count() == 0:
        single_hits.update({
            'contentType': content_type,
            'objId': id,
        }, {
            '$inc': {'hits': 1}
        }, True)

    hits.insert({
        'contentType': content_type,
        'objId': id,
        'ip': ip
    })
