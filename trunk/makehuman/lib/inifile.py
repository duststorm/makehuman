
import json

def _u2s(value):
    if isinstance(value, unicode):
        return str(value)
    elif isinstance(value, dict):
        return dict([(str(key), _u2s(val)) for key, val in value.iteritems()])
    elif isinstance(value, list):
        return [_u2s(val) for val in value]
    else:
        return value

def parseINI(s, replace = []):
    try:
        result = json.loads(s)
    except ValueError:
        for src, dst in replace + [("'",'"'), (": True",": true"), (": False",": false"), (": None",": null")]:
            s = s.replace(src, dst)
        result = json.loads(s)
    return _u2s(result)

def formatINI(d):
    return json.dumps(d, indent=4, ensure_ascii=True, encoding='iso-8859-1') + '\n'
