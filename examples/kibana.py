import balderdash.kibana as bd
import util

filter = bd.Filter() \
    .with_field("application_name", "my app") \
    .with_field("environment", "production")

fields = ['timestamp', 'http_code', 'response_time', 'path', 'host']

dashboard = bd.Dashboard("My app Kibana dashboard").with_fields(fields).with_filter(filter).build()

util.prettyPrintAsJson(dashboard)
