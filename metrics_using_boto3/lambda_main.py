"""Lambda main file for sending defined metrics to cloud watch using boto3."""

import sys
import os
from metrics_publication import MetricsAssigner
from lambda_logging import logger

def lambda_handler(event, context):
    """Handler function for the Lambda Invocations."""
    try:
        logger.info(f"Event : {event}")
        logger.info(f"Context : {context}")

        logger.info("Publishing metrics!")

        # only dimensions we are passing here, it will use default namespace & metrics name.
        # if needed other params we can pass it along with dimensions.

        metrics_dimensions = [
            {
                "Name": "Error_Name",
                "Value": "[SQS] API Callback Failed.",
            }]

        metrics_response = MetricsAssigner(metrics_dimensions).post_metrics()
        logger.info(f"status of published metrics: {metrics_response}")
        response_body = 'Metrics publication is completed.'

    except Exception as err: # pylint: disable=broad-except
        exc_obj = sys.exc_info()
        exc_type = exc_obj[0]
        exc_tb = exc_obj[2]
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        exception_string = str(exc_type) + " & " + str(fname) + " & " + str(exc_tb.tb_lineno)
        logger.error(
            f"An exception occurred in lambda_handler : {exception_string} as : {str(err)}"
        )
        response_body = 'Metrics publication is failed.'

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': response_body
    }
