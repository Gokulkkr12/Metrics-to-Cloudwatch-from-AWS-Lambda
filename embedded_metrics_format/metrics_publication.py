"""Uses Embedded Metrics Json Format to Ship metrics to Cloud watch."""
from aws_embedded_metrics import metric_scope

class MetricPublication:
    """Publication of Embedded metrics using aws_embedded_metrics module."""
    def __init__(self, metrics_data):
        self.namespace = metrics_data.get("namespace", "Health_Check")
        self.dimensions = metrics_data["dimensions"]
        self.metrics_name = metrics_data["metrics_name"]
        self.metric_unit = metrics_data.get("metric_unit", "Count")
        self.metric_value = metrics_data.get("metric_value", 1)

    @metric_scope
    def publish_metrics(self, metrics):
        """
        set_namespace() expects parameter of String[1-255 chars]
        set_dimensions() expects dict[key[str], value[str]]
        put_metric() expects parameters
            1. metrics_name of String[1-255 chars]
            2. metrics_value of Double[-2^360 to 2^360]
            3. metrics_unit [Seconds, Microseconds, Percent, Count...etc]
        """
        metrics.set_namespace(self.namespace)
        metrics.set_dimensions(self.dimensions)
        metrics.put_metric(self.metrics_name, self.metric_value, self.metric_unit)

        return {"status": "metrics is published!"}
