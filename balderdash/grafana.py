# coding=utf-8
# Constants for the various options go here...


class YAxisFormat:
    NoFormat = 'none'
    Short = 'short'
    Bytes = 'bytes'
    Bits = 'bits'
    BitsPerSecond = 'bps'
    Seconds = 's'
    Milliseconds = 'ms'
    Microseconds = 'µs'
    Nanoseconds = 'ns'
    Percent = 'percent'


class StackStyle:
    Stacked = True
    Unstacked = False


class FillStyle:
    Filled = 10
    Unfilled = 0


class Metric:
    def __init__(self, target):
        self.target = target

    def build(self):
        return {
            "target": self.target
        }


class Panel:
    def __init__(self, title, y_axis_format=YAxisFormat.NoFormat, filled=FillStyle.Unfilled, stacked=StackStyle.Unstacked):
        self.y_axis_format = y_axis_format
        self.title = title
        self.metrics = []
        self.filled = filled
        self.stacked = stacked

    def with_metric(self, metric):
        self.metrics.append(metric.build())
        return self

    def with_metrics(self, metrics):
        self.metrics += metrics
        return self

    def build(self, panel_id, span=12):
        return {
            "title": self.title,
            "error": False,
            "span": span,
            "editable": True,
            "type": "graph",
            "id": panel_id,
            "datasource": None,
            "renderer": "flot",
            "x-axis": True,
            "y-axis": True,
            "y_formats": [
                self.y_axis_format,
                "none"
            ],
            "grid": {
                "leftMax": None,
                "rightMax": None,
                "leftMin": None,
                "rightMin": None,
                "threshold1": None,
                "threshold2": None,
                "threshold1Color": "rgba(216, 200, 27, 0.27)",
                "threshold2Color": "rgba(234, 112, 112, 0.22)"
            },
            "lines": True,
            "fill": self.filled,
            "linewidth": 1,
            "points": False,
            "pointradius": 5,
            "bars": False,
            "stack": self.stacked,
            "percentage": False,
            "legend": {
                "show": True,
                "values": False,
                "min": False,
                "max": False,
                "current": False,
                "total": False,
                "avg": False
            },
            "NonePointMode": "connected",
            "steppedLine": False,
            "tooltip": {
                "value_type": "cumulative",
                "shared": False
            },
            "targets": self.metrics,
            "aliasColors": {},
            "seriesOverrides": [],
            "links": []
        }


class Row:
    def __init__(self):
        self.panels = []

    def with_panel(self, panel):
        self.panels.append(panel)
        return self

    def with_panels(self, panels):
        self.panels += panels
        return self

    def build(self, row_id):
        def to_panel(panel_builder):
            return panel_builder.build(self.panels.index(panel_builder), 12 / len(self.panels))

        return {
            "title": "Row %d" % row_id,
            "height": "250px",
            "editable": True,
            "collapse": False,
            "panels": map(to_panel, self.panels)
        }


class Dashboard:
    def __init__(self, title):
        self.title = title
        self.rows = []

    def with_row(self, row):
        self.rows.append(row.build(len(self.rows)))
        return self

    def with_rows(self, rows):
        self.rows += rows
        return self

    def build(self):
        return {
            "title": self.title,
            "originalTitle": self.title,
            "tags": [],
            "style": "dark",
            "timezone": "browser",
            "editable": True,
            "hideControls": False,
            "sharedCrosshair": False,
            "rows": self.rows,
            "nav": [
                {
                    "type": "timepicker",
                    "enable": True,
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
                    "now": True,
                    "collapse": False,
                    "notice": False
                }
            ],
            "time": {
                "from": "now-15m",
                "to": "now"
            },
            "templating": {
                "list": []
            },
            "annotations": {
                "list": [],
                "enable": False
            },
            "refresh": "10s",
            "version": 6,
            "hideAllLegends": False
        }
