"""Lambda main file for sending defined metrics using AWS Embedded Metrics Json Format."""

import sys
import os
from lambda_logging import logger
from metrics_publication import MetricPublication

def lambda_handler(event, context):
    """Handler function for the Lambda Invocations."""
    try:
        logger.info(f"Event : {event}")
        logger.info(f"Context : {context}")

        logger.info("Publishing metrics!")

        # only dimensions & metrics we are passing here, it will use default namespace.
        # if needed other params we can pass it along with dimensions.

        metrics_data = {
            "dimensions": {
                "Module": "XBOX_PING_SVC",
                "Error_Name": "SYNC_FAIL_ERROR"
            },
            "metrics_name": "ErrorCount"
        }

        metrics_response = MetricPublication(metrics_data).publish_metrics()  # pylint: disable = no-value-for-parameter
        logger.info(f"status of published metrics: {metrics_response}")
        response_body = 'Metrics Publication is success.'

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
