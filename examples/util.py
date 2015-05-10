import json

def prettyPrintAsJson(obj):
    print json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
