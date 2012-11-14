from django.http import HttpResponse
from datetime import datetime, timedelta, date
from django.db import models
import json


def _unix_timestamp(d):
    return int(time.mktime(d.timetuple()))


def _model2dict(item, fields=[]):
    d = {}
    for field in fields:
        f = item.__dict__[field]
        if type(f) in [datetime, date]:
            d[field] = _unix_timestamp(f)
        else:
            d[field] = f
    
    return d


def _response_json(data, fields=[]):
    if (issubclass(data.__class__, models.Model)):
        data = _model2dict(data, fields)
    elif (issubclass(data.__class__, models.query.QuerySet)):
        d = []
        for item in data:
            d.append(_model2dict(item, fields))
        data = d
    
    return HttpResponse(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False), mimetype='application/json')
    
def _calculate_percent(num, percent):
    return round(num + (( num * percent ) / 100), 2)
    
def _calculate_price(num, percent):
    
    pass
    


