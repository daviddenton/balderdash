import sys

sys.path.append('../balderdash')

import unittest
import random
import balderdash

dg = balderdash.grafana

teamname = "teamname"
appname = "appname"
envname = "envname"


def random_metric():
    return dg.Metric(str(random.random()))


def random_panel():
    return dg.Panel(str(random.random()), str(random.random()), str(random.random()), str(random.random()), ) \
        .with_metric(random_metric()) \
        .with_metric(random_metric())


def random_row():
    return dg.Row() \
        .with_panel(random_panel()) \
        .with_panel(random_panel())


class GrafanaDashboardTest(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        super(GrafanaDashboardTest, self).__init__(methodName)
        self.title = str(random.random())
        self.panelId = random.randint(1, 999)
        self.rowId = random.randint(1, 999)
        self.maxDiff = 100000
        self.yaxis = random.choice([dg.YAxisFormat.Bits, dg.YAxisFormat.BitsPerSecond, dg.YAxisFormat.Bytes])
        self.filled = random.choice([[dg.FillStyle.Filled, dg.FillStyle.Unfilled]])
        self.stacked = random.choice([[dg.StackStyle.Stacked, dg.StackStyle.Stacked]])
        self.target = 'target'
        self.minimum = 5

    def test_metric_renders(self):
        expected = {
            "target": self.target
        }
        self.assertEqual(expected, dg.Metric(self.target).build())

    def test_panel_renders(self):
        metric1 = random_metric()
        metric2 = random_metric()
        width = random.randint(1, 100)
        expected = {
            "title": self.title,
            "error": False,
            "span": width,
            "editable": True,
            "type": "graph",
            "id": self.panelId,
            "datasource": None,
            "renderer": "flot",
            "x-axis": True,
            "y-axis": True,
            "y_formats": [
                self.yaxis,
                "none"
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
            "targets": [metric1.build(), metric2.build()],
            "aliasColors": {},
            "seriesOverrides": [],
            "links": []
        }

        self.assertEqual(expected, dg.Panel(self.title, self.yaxis, self.filled, self.stacked, self.minimum)
                         .with_metric(metric1)
                         .with_metric(metric2)
                         .build(self.panelId, width))

    def test_row_splits_panels_evenly(self):
        panel1 = random_panel()
        panel2 = random_panel()
        expected = {
            "title": "Row %d" % 1,
            "height": "250px",
            "editable": True,
            "collapse": False,
            "panels": [panel1.build(11, 6), panel2.build(12, 6)]
        }
        self.assertEqual(expected, dg.Row()
                         .with_panel(panel1)
                         .with_panel(panel2)
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

        self.assertEqual(expected, dg.Dashboard(self.title)
                         .with_row(row1)
                         .with_row(row2)
                         .build())


if __name__ == "__main__":
    unittest.main()