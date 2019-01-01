import sys

sys.path.append('../balderdash')

import unittest
import random
import balderdash

bd = balderdash.grafana

teamname = "teamname"
appname = "appname"
envname = "envname"


def random_metric():
    name = str(random.random())
    return bd.Metric(name, right_y_axis_metric_name=name)


def random_panel():
    return bd.Panel(str(random.random()), str(random.random()), str(random.random()), str(random.random()), ) \
        .with_metric(random_metric()) \
        .with_metric(random_metric())


def random_singlestat_panel():
    return bd.SingleStatPanel(str(random.random()), str(random.random()), str(random.random())) \
        .with_metric(random_metric()) \
        .with_metric(random_metric())


def random_row():
    return bd.Row() \
        .with_panel(random_panel()) \
        .with_panel(random_singlestat_panel())


class GrafanaDashboardTest(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(GrafanaDashboardTest, self).__init__(methodName)
        self.title = str(random.random())
        self.panelId = random.randint(1, 999)
        self.span = random.randint(1, 100)

    def test_metric_renders(self):
        target = 'target'
        expected = {
            "refId": 'A',
            "target": target
        }
        self.assertEqual(expected, bd.Metric(target).build('A'))

    def test_panel_renders(self):
        yaxis = random.choice([bd.YAxisFormat.Bits, bd.YAxisFormat.BitsPerSecond, bd.YAxisFormat.Bytes])
        filled = random.choice([[bd.FillStyle.Filled, bd.FillStyle.Unfilled]])
        stacked = random.choice([[bd.StackStyle.Stacked, bd.StackStyle.Stacked]])
        minimum = 5

        metric1 = random_metric()
        metric2 = random_metric()

        expected = {
            "title": self.title,
            "error": False,
            "span": self.span,
            "editable": True,
            "type": "graph",
            "id": self.panelId,
            "datasource": None,
            "renderer": "flot",
            "x-axis": True,
            "y-axis": True,
            "y_formats": [
                yaxis,
                yaxis
            ],
            "grid": {
                "leftMax": None,
                "rightMax": None,
                "leftMin": minimum,
                "rightMin": None,
                "threshold1": None,
                "threshold2": None,
                "threshold1Color": "rgba(216, 200, 27, 0.27)",
                "threshold2Color": "rgba(234, 112, 112, 0.22)"
            },
            "lines": True,
            "fill": filled,
            "linewidth": 1,
            "points": False,
            "pointradius": 5,
            "bars": False,
            "stack": stacked,
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
            "targets": [metric1.build('A'), metric2.build('B')],
            "aliasColors": {},
            "seriesOverrides": [{
                "alias": metric1.right_y_axis_metric_name,
                "yaxis": 2
            }, {
                "alias": metric2.right_y_axis_metric_name,
                "yaxis": 2
            }],
            "links": []
        }

        self.assertEqual(expected, bd.Panel(self.title, yaxis, filled, stacked, minimum)
                         .with_metric(metric1)
                         .with_metric(metric2)
                         .build(self.panelId, self.span))

    def test_panel_renders_with_specific_maximum(self):
        yaxis = random.choice([bd.YAxisFormat.Bits, bd.YAxisFormat.BitsPerSecond, bd.YAxisFormat.Bytes])
        filled = random.choice([[bd.FillStyle.Filled, bd.FillStyle.Unfilled]])
        stacked = random.choice([[bd.StackStyle.Stacked, bd.StackStyle.Stacked]])
        minimum = 5
        maximum = 15

        expected_grid = {
            "leftMax": 15,
            "rightMax": None,
            "leftMin": minimum,
            "rightMin": None,
            "threshold1": None,
            "threshold2": None,
            "threshold1Color": "rgba(216, 200, 27, 0.27)",
            "threshold2Color": "rgba(234, 112, 112, 0.22)"
        }

        self.assertEqual(expected_grid, bd.Panel(self.title, yaxis, filled, stacked, minimum, maximum=maximum)
                         .with_metric(random_metric())
                         .with_metric(random_metric())
                         .build(self.panelId, self.span)['grid'])

    def test_panel_renders_with_datasource(self):
        expected = "a-datasource"

        actual = bd.Panel(self.title, datasource=expected).build(self.panelId, self.span)

        self.assertEqual(expected, actual.get("datasource"))

    def test_panel_renders_with_alias_colors(self):
        expected = {
            "metric1": "#color1",
            "metric2": "#color2"
        }

        actual = bd.Panel(self.title, alias_colors=expected).build(self.panelId, self.span)

        self.assertEqual(expected, actual.get("aliasColors"))

    def test_panel_renders_with_target_refids(self):
        metric1 = random_metric()
        metric2 = random_metric()

        expected = [
            {
                "refId": "A",
                "target": metric1.target
            },
            {
                "refId": "B",
                "target": metric2.target
            }
        ]
        actual = bd.Panel(self.title, alias_colors=expected) \
            .with_metric(metric1) \
            .with_metric(metric2) \
            .build(self.panelId, self.span)

        self.assertEqual(expected, actual.get("targets"))

    def test_panel_renders_an_alert(self):
        metric1 = random_metric()
        metric2 = random_metric()

        expected = {
            "conditions": [
                {
                    "evaluator": {
                        "params": [0],
                        "type": "gt"
                    },
                    "operator": {
                        "type": "and"
                    },
                    "query": {
                        "datasourceId": 1,
                        "model": {
                            "refId": "A",
                            "target": metric1.target
                        },
                        "params": ["A", "5m", "now"]
                    },
                    "reducer": {
                        "params": [],
                        "type": "last"
                    },
                    "type": "query"
                },
                {
                    "evaluator": {
                        "params": [3],
                        "type": "lt"
                    },
                    "operator": {
                        "type": "or"
                    },
                    "query": {
                        "datasourceId": 1,
                        "model": {
                            "refId": "B",
                            "target": metric2.target
                        },
                        "params": ["B", "5m", "now"]
                    },
                    "reducer": {
                        "params": [],
                        "type": "last"
                    },
                    "type": "query"
                }
            ],
            "executionErrorState": "alerting",
            "frequency": "55s",
            "handler": 1,
            "name": "a test alert",
            "noDataState": "no_data",
            "notifications": []
        }

        actual = bd.Panel(self.title) \
            .with_metric(metric1) \
            .with_metric(metric2) \
            .with_alert(bd.Alert('a test alert', 55)
                        .with_condition(bd.Condition(metric1, bd.EvaluatorType.GreaterThan, 0))
                        .with_condition(bd.Condition(metric2, bd.EvaluatorType.LessThan, 3, bd.OperatorType.Or))) \
            .build(self.panelId, self.span)

        self.assertEqual(expected, actual.get("alert"))

    def test_panel_renders_an_alert_with_a_reducer(self):
        metric1 = random_metric()
        metric2 = random_metric()

        expected_conditions = [
                {
                    "evaluator": {
                        "params": [0],
                        "type": "gt"
                    },
                    "operator": {
                        "type": "and"
                    },
                    "query": {
                        "datasourceId": 1,
                        "model": {
                            "refId": "A",
                            "target": metric1.target
                        },
                        "params": ["A", "5m", "now"]
                    },
                    "reducer": {
                        "params": [],
                        "type": "avg"
                    },
                    "type": "query"
                },
                {
                    "evaluator": {
                        "params": [3],
                        "type": "lt"
                    },
                    "operator": {
                        "type": "or"
                    },
                    "query": {
                        "datasourceId": 1,
                        "model": {
                            "refId": "B",
                            "target": metric2.target
                        },
                        "params": ["B", "5m", "now"]
                    },
                    "reducer": {
                        "params": [],
                        "type": "min"
                    },
                    "type": "query"
                }
            ]

        actual = bd.Panel(self.title) \
            .with_metric(metric1) \
            .with_metric(metric2) \
            .with_alert(bd.Alert('a test alert', 55)
                        .with_condition(bd.Condition(metric1, bd.EvaluatorType.GreaterThan, 0, reducer=bd.Reducer.Average))
                        .with_condition(bd.Condition(metric2, bd.EvaluatorType.LessThan, 3, bd.OperatorType.Or, reducer=bd.Reducer.Min))) \
            .build(self.panelId, self.span)

        self.assertEqual(expected_conditions, actual['alert']['conditions'])

    def test_panel_renders_an_alert_with_a_notification(self):
        metric1 = random_metric()
        metric2 = random_metric()

        expected = [
            {
                "id": 1
            },
            {
                "id": 2
            }
        ]

        actual = bd.Panel(self.title) \
            .with_metric(metric1) \
            .with_metric(metric2) \
            .with_alert(bd.Alert('a test alert', 55)
                        .with_condition(bd.Condition(metric1, bd.EvaluatorType.GreaterThan, 5))
                        .with_notification(bd.Notification(1))
                        .with_notification(bd.Notification(2))) \
            .build(self.panelId, self.span)

        self.assertEqual(expected, actual['alert']['notifications'])

    def test_panel_renders_an_alert_with_a_message(self):
        metric1 = random_metric()
        metric2 = random_metric()

        actual = bd.Panel(self.title) \
            .with_metric(metric1) \
            .with_metric(metric2) \
            .with_alert(bd.Alert('a test alert', 55, message='An alert message')
                        .with_condition(bd.Condition(metric1, bd.EvaluatorType.GreaterThan, 5))
                        .with_notification(bd.Notification(1)))\
            .build(self.panelId, self.span)

        self.assertEqual('An alert message', actual['alert']['message'])

    def test_singlestat_panel_renders(self):
        prefix = "some prefix"
        postfix = "some postfix"
        threshold_lower = 111
        threshold_mid = 222
        threshold_upper = 333
        metric1 = random_metric()
        metric2 = random_metric()

        expected = {
            "title": self.title,
            "error": False,
            "span": self.span,
            "editable": True,
            "type": "singlestat",
            "id": self.panelId,
            "links": [],
            "maxDataPoints": 100,
            "interval": None,
            "targets": [metric1.build('A'), metric2.build('B')],
            "cacheTimeout": None,
            "format": "none",
            "prefix": prefix,
            "postfix": postfix,
            "valueName": "current",
            "prefixFontSize": "100%",
            "valueFontSize": "120%",
            "postfixFontSize": "100%",
            "thresholds": str(threshold_lower) + "," + str(threshold_mid) + "," + str(threshold_upper),
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

        single_stat_panel = bd.SingleStatPanel(self.title, prefix=prefix, postfix=postfix,
                                               thresholds=bd.Thresholds(threshold_lower, threshold_mid,
                                                                        threshold_upper),
                                               invert_threshold_order=False)
        actual = single_stat_panel \
            .with_metric(metric1) \
            .with_metric(metric2) \
            .build(self.panelId, self.span)

        self.assertEqual(expected, actual)

    def test_singlestat_panel_renders_with_inverted_thresholds(self):
        single_stat_panel = bd.SingleStatPanel(self.title, invert_threshold_order=True)

        expected = [
            "rgba(71, 212, 59, 0.4)",
            "rgba(245, 150, 40, 0.73)",
            "rgba(225, 40, 40, 0.59)",
        ]

        actual = single_stat_panel.build(self.panelId, self.span)

        self.assertEqual(actual.get("colors"), expected)

    def test_row_can_be_collapsed(self):
        panel1 = random_panel()
        panel2 = random_panel()
        expected = {
            "title": "Row %d" % 1,
            "height": "250px",
            "editable": True,
            "collapse": True,
            "showTitle": False,
            "panels": [panel1.build(11, 6), panel2.build(12, 6)]
        }
        self.assertEqual(expected, bd.Row(collapse=True)
                         .with_panel(panel1)
                         .with_panel(panel2)
                         .build(1))

    def test_row_title_can_be_shown(self):
        panel1 = random_panel()
        panel2 = random_panel()
        expected = {
            "title": "Row %d" % 1,
            "height": "250px",
            "editable": True,
            "collapse": False,
            "showTitle": True,
            "panels": [panel1.build(11, 6), panel2.build(12, 6)]
        }
        self.assertEqual(expected, bd.Row(show_title=True)
                         .with_panel(panel1)
                         .with_panel(panel2)
                         .build(1))

    def test_row_splits_panels_evenly(self):
        panel1 = random_panel()
        panel2 = random_panel()
        expected = {
            "title": "Row %d" % 1,
            "height": "250px",
            "editable": True,
            "collapse": False,
            "showTitle": False,
            "panels": [panel1.build(11, 6), panel2.build(12, 6)]
        }
        self.assertEqual(expected, bd.Row()
                         .with_panel(panel1)
                         .with_panel(panel2)
                         .build(1))

    def test_row_respects_specific_panel_span(self):
        def random_panel_with_span(span):
            return bd.Panel(str(random.random()), str(random.random()), str(random.random()), str(random.random()),
                            span=span) \
                .with_metric(random_metric()) \
                .with_metric(random_metric())

        panel1 = random_panel_with_span(3)
        panel2 = random_panel()
        expected = {
            "title": "Row %d" % 1,
            "height": "250px",
            "editable": True,
            "collapse": False,
            "showTitle": False,
            "panels": [panel1.build(11, 3), panel2.build(12, 6)]
        }
        self.assertEqual(expected, bd.Row()
                         .with_panel(panel1)
                         .with_panel(panel2)
                         .build(1))

    def test_row_can_be_named(self):
        panel1 = random_panel()
        panel2 = random_panel()
        expected = {
            "title": "Row of magical nameliness",
            "height": "250px",
            "editable": True,
            "collapse": False,
            "showTitle": False,
            "panels": [panel1.build(11, 6), panel2.build(12, 6)]
        }
        self.assertEqual(expected, bd.Row(title='Row of magical nameliness')
                         .with_panel(panel1)
                         .with_panel(panel2)
                         .build(1))

    def test_row_height(self):
        expected = {
            "title": "Row %d" % 1,
            "height": "123px",
            "editable": True,
            "collapse": False,
            "showTitle": False,
            "panels": []
        }
        self.assertEqual(expected, bd.Row(height="123px")
                         .build(1))

    def test_dashboard_renders(self):
        row1 = random_row()
        row2 = random_row()
        expected = {
            "title": self.title,
            "originalTitle": self.title,
            "tags": [],
            "style": "dark",
            "timezone": "browser",
            "editable": True,
            "hideControls": False,
            "sharedCrosshair": False,
            "rows": [row1.build(1), row2.build(2)],
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

        actual = bd.Dashboard(self.title) \
            .with_row(row1) \
            .with_row(row2) \
            .build()

        self.assertEqual(expected, actual)

    def test_dashboard_with_customised_time_range(self):
        expected = {
            "from": "now-2d",
            "to": "now-1h"
        }

        actual = bd.Dashboard(self.title) \
            .with_time_range("now-2d", "now-1h") \
            .build()

        self.assertEqual(expected, actual["time"])

    def test_dashboard_with_customised_nav_time_options(self):
        expected = ["1h", "12h", "7d"]

        actual = bd.Dashboard(self.title) \
            .with_nav_time_options(["1h", "12h", "7d"]) \
            .build()

        self.assertEqual(expected, actual["nav"][0]["time_options"])

    def test_dashboard_with_customised_nav_refresh_intervals(self):
        expected = ["1m", "1h", "1d"]

        actual = bd.Dashboard(self.title) \
            .with_nav_refresh_intervals(["1m", "1h", "1d"]) \
            .build()

        self.assertEqual(expected, actual["nav"][0]["refresh_intervals"])

    def test_dashboard_write_request_renders(self):
        dashboard = bd.Dashboard(self.title)
        actual = bd.DashboardWriteRequest(dashboard) \
            .build()

        self.assertEqual(dashboard.build(), actual["dashboard"])
        self.assertEqual(True, actual["overwrite"])


if __name__ == "__main__":
    unittest.main()
