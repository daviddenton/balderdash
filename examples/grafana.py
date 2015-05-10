import balderdash.grafana as bd
import util

memory_panel = bd.Panel("Memory", bd.YAxisFormat.Bytes, bd.FillStyle.Filled) \
    .with_metric(bd.Metric("aliasByNode(my.app.*.memory.total, 2)")) \
    .with_metric(bd.Metric("aliasByNode(my.app.*.memory.used, 2)"))

uptime_panel = bd.Panel("Uptime", bd.YAxisFormat.Seconds, bd.FillStyle.Unfilled) \
    .with_metric(bd.Metric("aliasByNode(my.app.*.uptime.seconds, 2)"))

response_time_panel = bd.Panel("Response Time", bd.YAxisFormat.Milliseconds, bd.FillStyle.Unfilled) \
    .with_metric(bd.Metric("aliasByNode(my.app.*.graphite.response.time.999thPercentile, 2)"))

row_with_2_panels = bd.Row() \
    .with_panel(memory_panel) \
    .with_panel(uptime_panel)

row_with_1_panel = bd.Row().with_panel(response_time_panel)

dashboard = bd.Dashboard("My app Grafana dashboard").with_row(row_with_2_panels).with_row(row_with_1_panel).build()

util.prettyPrintAsJson(dashboard)
