from django.conf import settings

from pymongo import Connection

connection = Connection(settings.get('MONGODB_STRING', ''))

db = connection.hit_counter

hits = db.hits
single_hits = db.single_hits


def insert_hit(content_type, id, ip):
    h = hits.find({
        'contentType': content_type,
        'objId': id,
        'ip': ip
    })

    print h.count()
    print

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
