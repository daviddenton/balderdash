class Filter:
    def __init__(self):
        self.filters = {
            "0": {
                "type": "time",
                "field": "@timestamp",
                "from": "now-1h",
                "to": "now",
                "mandate": "must",
                "active": True,
                "alias": "",
                "id": 0
            }
        }

    def with_field(self, field, value):
        next_index = len(self.filters)
        self.filters[str(next_index)] = {
            "type": "field",
            "field": field,
            "query": "\"" + value + "\"",
            "mandate": "must",
            "active": True,
            "alias": "",
            "id": next_index
        }
        return self

    def build(self):
        return {
            "list": self.filters,
            "ids": range(0, len(self.filters))
        }


class Dashboard:
    def with_filter(self):
        return self

    def build(self):
        return {

        }
