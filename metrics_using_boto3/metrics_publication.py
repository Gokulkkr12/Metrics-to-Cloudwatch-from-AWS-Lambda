"""Metrics Publication to AWS Cloudwatch using Boto3"""
import boto3
from lambda_logging import logger

class MetricsPublication:
    """Common class to publish metrics into cloud watch"""

    METRICS_NAME = "DEFAULT_ERROR_NAME"
    METRICS_NAMESPACE = "DEFAULT_NAMESPACE"

    def __init__(self, input_data):
        """Expecting dictionary to get required parameters to publish metrics into cloudwatch"""

        self.metric_name = input_data.get("metric_name", self.METRICS_NAME)
        self.namespace = input_data.get("namespace", self.METRICS_NAMESPACE)
        self.dimensions = input_data["dimensions"]
        self.unit = input_data.get("unit", "None")
        self.value = input_data.get("value", 1)
        self.input_data = input_data

    def validate_dimensions(self):
        """Validates input_data dimension list."""

        logger.info(f"Validating given dimensions: {self.dimensions}")

        if isinstance(self.dimensions, list):
            for dimension in self.dimensions:
                name = dimension.get("Name", "")
                value = dimension.get("Value", "")

                if any([not isinstance(name, str),
                        name == "", not isinstance(value, str),
                        value == ""]):
                    return False

            logger.info("Dimensions are valid!")

            return True

        return False

    def validate_metric_params(self):
        """Validation of request params, additional required param checks can be added here."""

        if all([isinstance(self.metric_name, str), isinstance(self.namespace, str),
                self.validate_dimensions()]):
            return True

        return False

    def metric_data_preparation(self):
        """Metric Data Preparation: Additional data which needs to be sent can be prepared here."""

        metrics_dict = dict(
            MetricName=self.metric_name,
            Dimensions=self.dimensions,
            Unit=self.unit,
            Value=self.value
        )

        return [metrics_dict]

    def publish_metrics_to_cloudwatch(self):
        """Core Logic to Publish Metrics into Cloudwatch."""

        try:
            logger.info(f"Metrics Input Data: {self.input_data}")

            if not self.validate_metric_params():
                raise ValueError("Metrics Params validation failed!")

            metric_info_list = self.metric_data_preparation()
            cloudwatch_connector = boto3.client("cloudwatch")

            response = cloudwatch_connector.put_metric_data(
                MetricData=metric_info_list,
                Namespace=self.namespace
            )

        except Exception as err: # pylint: disable=broad-except
            response = f"Error occurred while publishing metrics as: {str(err)}"
            logger.error(response)

        return response


class MetricsAssigner: # pylint: disable=too-few-public-methods
    """Helper class to assign metrics parameters to MetricsPublication class."""

    def __init__(self, dimensions):
        self.dimensions = dimensions

    def post_metrics(self):
        """Prepares metrics params and calls MetricsPublication class."""

        metrics_data = {"dimensions": self.dimensions}
        post_metrics = MetricsPublication(metrics_data)
        metrics_response = post_metrics.publish_metrics_to_cloudwatch()

        return metrics_response
