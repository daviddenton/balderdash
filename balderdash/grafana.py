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


class YAxis:
    Left = 1
    Right = 2


class YAxisMinimum:
    Zero = 0
    Auto = None


class StackStyle:
    Stacked = True
    Unstacked = False


class FillStyle:
    Filled = 10
    Unfilled = 0


class Metric:
    def __init__(self, target, right_y_axis_metric_name=None):
        self.target = target
        self.right_y_axis_metric_name = right_y_axis_metric_name

    def build(self):
        return {
            "target": self.target
        }


class Panel:
    def __init__(self, title, y_axis_format=YAxisFormat.NoFormat, filled=FillStyle.Unfilled,
                 stacked=StackStyle.Unstacked, minimum=YAxisMinimum.Auto):
        self.y_axis_format = y_axis_format
        self.title = title
        self.metrics = []
        self.filled = filled
        self.stacked = stacked
        self.minimum = minimum
        self.series_overrides = []

    def with_metric(self, metric):
        self.metrics.append(metric.build())
        if metric.right_y_axis_metric_name is not None:
            self.series_overrides.append({
                "alias": metric.right_y_axis_metric_name,
                "yaxis": 2
            })
        return self

    def with_metrics(self, metrics):
        for metric in metrics:
            self.with_metric(metric)
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
                self.y_axis_format
            ],
            "grid": {
                "leftMax": None,
                "rightMax": None,
                "leftMin": self.minimum,
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
            "nullPointMode": "connected",
            "steppedLine": False,
            "tooltip": {
                "value_type": "cumulative",
                "shared": False
            },
            "targets": self.metrics,
            "aliasColors": {},
            "seriesOverrides": self.series_overrides,
            "links": []
        }


class SingleStatPanel:
    def __init__(self, title, prefix, postfix):
        self.title = title
        self.prefix = prefix
        self.postfix = postfix
        self.metrics = []

    def with_metric(self, metric):
        self.metrics.append(metric.build())
        return self

    def with_metrics(self, metrics):
        for metric in metrics:
            self.with_metric(metric)
        return self

    def build(self, panel_id, span=12):
        return {
            "title": self.title,
            "error": False,
            "span": span,
            "editable": True,
            "type": "singlestat",
            "id": panel_id,
            "links": [],
            "maxDataPoints": 100,
            "interval": None,
            "targets": self.metrics,
            "cacheTimeout": None,
            "format": "none",
            "prefix": self.prefix,
            "postfix": self.postfix,
            "valueName": "current",
            "prefixFontSize": "100%",
            "valueFontSize": "120%",
            "postfixFontSize": "100%",
            "thresholds": "0,50,200",
            "colorBackground": True,
            "colorValue": False,
            "colors": [
                "rgba(225, 40, 40, 0.59)",
                "rgba(245, 150, 40, 0.73)",
                "rgba(71, 212, 59, 0.4)"
            ],
            "sparkline": {
                "show": True,
                "full": False,
                "lineColor": "rgb(71, 248, 35)",
                "fillColor": "rgba(130, 189, 31, 0.18)"
            }
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
            return panel_builder.build((row_id * 10) + (self.panels.index(panel_builder) + 1), 12 / len(self.panels))

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
        self.rows.append(row.build(len(self.rows) + 1))
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
