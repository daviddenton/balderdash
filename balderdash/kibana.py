# coding=utf-8
# Constants for the various options go here...

class FilterMode:
    Include = 'must'
    Exclude = 'mustNot'


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

    def with_field(self, field, value, filter_mode=FilterMode.Include):
        next_index = len(self.filters)
        self.filters[str(next_index)] = {
            "type": "field",
            "field": field,
            "query": "\"" + value + "\"",
            "mandate": filter_mode,
            "active": True,
            "alias": "",
            "id": next_index
        }
        return self

    def build(self):
        return {
            "list": self.filters,
            "ids": list(range(0, len(self.filters)))
        }


class Dashboard:
    def __init__(self, title):
        self.title = title
        self.filter = Filter()
        self.query = ""
        self.fields = []

    def with_filter(self, new_filter):
        self.filter = new_filter
        return self

    def with_query(self, value):
        self.query = value
        return self

    def with_fields(self, fields):
        self.fields = fields
        return self

    def build(self):
        return {
            "title": self.title,
            "services": {
                "query": {
                    "list": {
                        "0": {
                            "query": self.query,
                            "alias": "",
                            "color": "#7EB26D",
                            "id": 0,
                            "pin": False,
                            "type": "lucene",
                            "enable": True
                        }
                    },
                    "ids": [0]
                },
                "filter": self.filter.build()
            },
            "rows": [
                {
                    "title": "Graph",
                    "height": "350px",
                    "editable": True,
                    "collapse": False,
                    "collapsable": True,
                    "panels": [
                        {
                            "span": 12,
                            "editable": True,
                            "group": ["default"],
                            "type": "histogram",
                            "mode": "count",
                            "time_field": "@timestamp",
                            "value_field": None,
                            "auto_int": True,
                            "resolution": 100,
                            "interval": "30s",
                            "fill": 3,
                            "linewidth": 3,
                            "timezone": "browser",
                            "spyable": True,
                            "zoomlinks": True,
                            "bars": True,
                            "stack": True,
                            "points": False,
                            "lines": False,
                            "legend": True,
                            "x-axis": True,
                            "y-axis": True,
                            "percentage": False,
                            "interactive": True,
                            "queries": {
                                "mode": "all",
                                "ids": [0]
                            },
                            "title": "Events over time",
                            "intervals": [
                                "auto",
                                "1s",
                                "1m",
                                "5m",
                                "10m",
                                "30m",
                                "1h",
                                "3h",
                                "12h",
                                "1d",
                                "1w",
                                "1M",
                                "1y"
                            ],
                            "options": True,
                            "tooltip": {
                                "value_type": "cumulative",
                                "query_as_alias": True
                            },
                            "scale": 1,
                            "y_format": "none",
                            "grid": {
                                "max": None,
                                "min": 0
                            },
                            "annotate": {
                                "enable": False,
                                "query": "*",
                                "size": 20,
                                "field": "_type",
                                "sort": [
                                    "_score",
                                    "desc"
                                ]
                            },
                            "pointradius": 5,
                            "show_query": True,
                            "legend_counts": True,
                            "zerofill": True,
                            "derivative": False
                        }
                    ],
                    "notice": False
                },
                {
                    "notice": False,
                    "panels": [
                        {
                            "status": "Stable",
                            "header": True,
                            "trimFactor": 300,
                            "spyable": True,
                            "field_list": True,
                            "size": 100,
                            "all_fields": False,
                            "style": {
                                "font-size": "9pt"
                            },
                            "span": 12,
                            "title": "All events",
                            "normTimes": True,
                            "type": "table",
                            "sort": [
                                "@timestamp",
                                "desc"
                            ],
                            "error": False,
                            "editable": True,
                            "offset": 0,
                            "group": [
                                "default"
                            ],
                            "overflow": "min-height",
                            "pages": 5,
                            "localTime": True,
                            "sortable": True,
                            "fields": self.fields,
                            "paging": True,
                            "queries": {
                                "mode": "all",
                                "ids": [
                                    0
                                ]
                            },
                            "timeField": "@timestamp",
                            "highlight": []
                        }
                    ],
                    "collapse": False,
                    "title": "Events",
                    "editable": True,
                    "height": "350px",
                    "collapsable": True
                }
            ],
            "editable": True,
            "failover": False,
            "index": {
                "interval": "day",
                "pattern": "[logstash-]YYYY.MM.DD",
                "default": "NO_TIME_FILTER_OR_INDEX_PATTERN_NOT_MATCHED",
                "warm_fields": True
            },
            "style": "dark",
            "panel_hints": True,
            "pulldowns": [
                {
                    "type": "query",
                    "collapse": False,
                    "notice": False,
                    "query": "*",
                    "pinned": True,
                    "history": [
                    ],
                    "remember": 10,
                    "enable": True
                },
                {
                    "type": "filtering",
                    "collapse": False,
                    "notice": True,
                    "enable": True
                }
            ],
            "nav": [
                {
                    "type": "timepicker",
                    "collapse": False,
                    "notice": False,
                    "status": "Stable",
                    "time_options": [
                        "5m",
                        "15m",
                        "1h",
                        "6h",
                        "12h",
                        "24h",
                        "2d",
                        "7d",
                        "30d"
                    ],
                    "refresh_intervals": [
                        "5s",
                        "10s",
                        "30s",
                        "1m",
                        "5m",
                        "15m",
                        "30m",
                        "1h",
                        "2h",
                        "1d"
                    ],
                    "timefield": "@timestamp",
                    "now": True,
                    "filter_id": 0,
                    "enable": True
                }
            ],
            "loader": {
                "save_gist": False,
                "save_elasticsearch": True,
                "save_local": True,
                "save_default": True,
                "save_temp": True,
                "save_temp_ttl_enable": True,
                "save_temp_ttl": "30d",
                "load_gist": True,
                "load_elasticsearch": True,
                "load_elasticsearch_size": 20,
                "load_local": True,
                "hide": False
            },
            "refresh": "30s"
        }

