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


class Thresholds:
    def __init__(self, lower, mid, upper):
        self.lower = lower
        self.mid = mid
        self.upper = upper

    def toCsv(self):
        return ",".join([str(self.lower), str(self.mid), str(self.upper)])


class EvaluatorType:
    GreaterThan = 'gt'
    LessThan = 'lt'
    Outside = 'outside_range'
    Within = 'within_range'
    NoValue = 'no_value'


class OperatorType:
    And = 'and'
    Or = 'or'


class Reducer:
    Average = 'avg'
    Count = 'count'
    Last = 'last'
    Median = 'median'
    Max = 'max'
    Min = 'min'
    Sum = 'sum'


class NoDataState:
    Alerting = 'alerting'
    KeepState = 'keep_state'
    NoData = 'no_data'
    Ok = 'ok'


class ExecutionErrorState:
    Alerting = 'alerting'
    KeepState = 'keep_state'


class VariableRefresh:
    Never = 0
    OnDashboardLoad = 1
    OnTimeRangeChange = 2

class VariableSort:
    Disabled = 0
    AlphaAsc = 1
    AlphaDesc = 2
    NumericalAsc = 3
    NumericalDesc = 4
    AlphaCaseInsensitiveAsc = 5
    AlphaCaseInsensitiveDesc = 6


class Notification:
    def __init__(self, notification_id):
        self.notification_id = notification_id

    def build(self):
        return {
            'id': self.notification_id
        }


class Condition:
    def __init__(self, metric, evaluator_type, value, operator_type=OperatorType.And, reducer=Reducer.Last):
        self.metric = metric
        self.evaluator_type = evaluator_type
        self.value = value
        self.operator_type = operator_type
        self.reducer = reducer

    def build(self, panel_metrics):
        filtered = filter(lambda possible_metric: possible_metric['target'] == self.metric.target, panel_metrics)
        matching_metric = list(filtered).pop(0)
        return {
            "evaluator": {
                "params": [self.value],
                "type": self.evaluator_type
            },
            "operator": {
                "type": self.operator_type
            },
            "query": {
                "datasourceId": 1,
                "model": {
                    "refId": matching_metric['refId'],
                    "target": matching_metric['target']
                },
                "params": [matching_metric['refId'], "5m", "now"]
            },
            "reducer": {
                "params": [],
                "type": self.reducer
            },
            "type": "query"
        }


class Metric:
    def __init__(self, target, right_y_axis_metric_name=None, hide=False):
        self.target = target
        self.right_y_axis_metric_name = right_y_axis_metric_name
        self.hide = hide

    def build(self, ref_id):
        json = {
            "refId": ref_id,
            "target": self.target
        }
        if self.hide:
            json['hide'] = True
        return json


class Alert:
    def __init__(self, name, frequency, message=None, no_data_state=NoDataState.NoData, execution_error_state=ExecutionErrorState.Alerting):
        self.name = name
        self.frequency = frequency
        self.message = message
        self.conditions = []
        self.notifications = []
        self.no_data_state = no_data_state
        self.execution_error_state = execution_error_state

    def with_notification(self, notification):
        self.notifications.append(notification)
        return self

    def with_condition(self, condition):
        self.conditions.append(condition)
        return self

    def build(self, panel_metrics):
        alert = {
            "conditions": list(map(lambda condition: condition.build(panel_metrics), self.conditions)),
            "executionErrorState": self.execution_error_state,
            "frequency": "%ds" % self.frequency,
            "handler": 1,
            "name": self.name,
            "noDataState": self.no_data_state,
            "notifications": list(map(lambda notification: notification.build(), self.notifications))
        }
        if self.message:
            alert['message'] = self.message
        return alert


class Panel:
    def __init__(self, title, y_axis_format=YAxisFormat.NoFormat, filled=FillStyle.Unfilled,
                 stacked=StackStyle.Unstacked, minimum=YAxisMinimum.Auto, alias_colors=None,
                 span=None, maximum=None, datasource=None, lines=True, bars=False, points=False):
        self.y_axis_format = y_axis_format
        self.title = title
        self.metrics = []
        self.alert = None
        self.filled = filled
        self.stacked = stacked
        self.minimum = minimum
        self.maximum = maximum
        self.series_overrides = []
        self.alias_colors = alias_colors
        self.span = span
        self.datasource = datasource
        self.lines = lines
        self.bars = bars
        self.points = points

        self.available_ref_ids = list(map(chr, range(65, 91)))

    def with_metric(self, metric):
        self.metrics.append(metric.build(self.available_ref_ids.pop(0)))
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

    def with_alert(self, alert):
        self.alert = alert
        return self

    def build(self, panel_id, span=12):
        panel = {
            "title": self.title,
            "error": False,
            "span": self.span or span,
            "editable": True,
            "type": "graph",
            "id": panel_id,
            "datasource": self.datasource,
            "renderer": "flot",
            "x-axis": True,
            "y-axis": True,
            "y_formats": [
                self.y_axis_format,
                self.y_axis_format
            ],
            "grid": {
                "leftMax": self.maximum,
                "rightMax": None,
                "leftMin": self.minimum,
                "rightMin": None,
                "threshold1": None,
                "threshold2": None,
                "threshold1Color": "rgba(216, 200, 27, 0.27)",
                "threshold2Color": "rgba(234, 112, 112, 0.22)"
            },
            "lines": self.lines,
            "fill": self.filled,
            "linewidth": 1,
            "points": self.points,
            "pointradius": 5,
            "bars": self.bars,
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
            "aliasColors": ({} if self.alias_colors is None else self.alias_colors),
            "seriesOverrides": self.series_overrides,
            "links": []
        }
        if self.alert:
            panel['alert'] = self.alert.build(self.metrics)
        return panel


class SingleStatPanel:
    def __init__(self, title, prefix="", postfix="", thresholds=Thresholds(0,50,200), invert_threshold_order=False):
        self.title = title
        self.prefix = prefix
        self.postfix = postfix
        self.thresholds = thresholds
        self.invert_threshold_order = invert_threshold_order
        self.metrics = []

        self.available_ref_ids = list(map(chr, range(65, 91)))

    def with_metric(self, metric):
        self.metrics.append(metric.build(self.available_ref_ids.pop(0)))
        return self

    def with_metrics(self, metrics):
        for metric in metrics:
            self.with_metric(metric)
        return self

    def build(self, panel_id, span=12):
        colors = ["rgba(225, 40, 40, 0.59)", "rgba(245, 150, 40, 0.73)", "rgba(71, 212, 59, 0.4)"]
        if self.invert_threshold_order:
            colors.reverse()

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
            "thresholds": self.thresholds.toCsv(),
            "colorBackground": True,
            "colorValue": False,
            "colors": colors,
            "sparkline": {
                "show": True,
                "full": False,
                "lineColor": "rgb(71, 248, 35)",
                "fillColor": "rgba(130, 189, 31, 0.18)"
            }
        }


class QueryVariable:
    def __init__(self, name, label, datasource, query, 
                 include_all=False,
                 multi=False,
                 sort=VariableSort.Disabled,
                 refresh=VariableRefresh.OnDashboardLoad):
        self.name = name
        self.label = label
        self.datasource = datasource
        self.query = query
        self.include_all = include_all
        self.multi = multi
        self.sort = sort
        self.refresh = refresh

    def build(self):
        return {
            "allValue": None,
            "datasource": self.datasource,
            "definition": self.query,
            "hide": 0,
            "includeAll": self.include_all,
            "label": self.label,
            "multi": self.multi,
            "name": self.name,
            "query": self.query,
            "refresh": self.refresh,
            "regex": "",
            "skipUrlSync": False,
            "sort": self.sort,
            "tagValuesQuery": "",
            "tags": [],
            "tagsQuery": "",
            "type": "query",
            "useTags": False
        }

class CustomVariable:
    def __init__(self, name, label, default_value, *other_values):
        self.name = name
        self.label = label
        self.default_value = default_value
        self.other_values = other_values

    def _as_option(self, value, selected=False):
        return {
                "selected": selected,
                "text": value,
                "value": value
            }

    def build(self):
        options = [self._as_option(self.default_value, selected=True)] + \
            [self._as_option(value) for value in self.other_values]

        return {
            "allValue": None,
            "current": {
                "tags": [],
                "text": self.default_value,
                "value": self.default_value
            },
            "hide": 0,
            "includeAll": False,
            "label": self.label,
            "multi": False,
            "name": self.name,
            "options": options,
            "query": ",".join([self.default_value] + list(self.other_values)),
            "skipUrlSync": False,
            "type": "custom"
      }

class Row:
    def __init__(self, height="250px", title=None, show_title=False, collapse=False):
        self.panels = []
        self.height = height
        self.title = title
        self.show_title=show_title
        self.collapse=collapse

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
            "title": self.title or "Row %d" % row_id,
            "height": self.height,
            "editable": True,
            "collapse": self.collapse,
            "showTitle": self.show_title,
            "panels": list(map(to_panel, self.panels))
        }


class Dashboard:
    def __init__(self, title):
        self.title = title
        self.rows = []
        self.time = {
            "from": "now-15m",
            "to": "now"
        }
        self.time_options = ["5m", "15m", "1h", "6h", "12h", "24h", "2d", "7d", "30d"]
        self.refresh_intervals = ["5s", "10s", "30s", "1m", "5m", "15m", "30m", "1h", "2h", "1d"]
        self.variables = []

    def with_row(self, row):
        self.rows.append(row.build(len(self.rows) + 1))
        return self

    def with_rows(self, rows):
        self.rows += rows
        return self

    def with_time_range(self, start, end):
        self.time["from"] = start
        self.time["to"] = end
        return self

    def with_nav_time_options(self, options):
        self.time_options = options
        return self

    def with_nav_refresh_intervals(self, options):
        self.refresh_intervals = options
        return self

    def with_variable(self, variable):
        self.variables += [variable]
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
                    "time_options": self.time_options,
                    "refresh_intervals": self.refresh_intervals,
                    "now": True,
                    "collapse": False,
                    "notice": False
                }
            ],
            "time": self.time,
            "templating": {
                "list": [variable.build() for variable in self.variables]
            },
            "annotations": {
                "list": [],
                "enable": False
            },
            "refresh": "10s",
            "version": 6,
            "hideAllLegends": False
        }

# This wraps the dashboard json to make it suitable for POSTing to /api/dashboards/db -- see http://docs.grafana.org/reference/http_api/
class DashboardWriteRequest:
    def __init__(self, dashboard, overwrite=True):
        self.dashboard = dashboard
        self.overwrite = overwrite

    def build(self):
        return {
            "dashboard": self.dashboard.build(),
            "overwrite": self.overwrite
        }
