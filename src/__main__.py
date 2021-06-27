import time
from multiprocessing import Process

from src import SitesAvailability, connectors
from src.connectors import AivenConnector, KafkaClient, PostgreSQLConnector
from src.utils import PeriodicThread, constants


if __name__ == '__main__':

    # Initialize Aiven connector
    aiven = AivenConnector(constants.config)

    # Create/Check Kafka service status
    aiven.create_service(
        constants.config['project'],
        'kafka',
        constants.config['kafka_name'],
        constants.config['kafka_cloud'],
        constants.config['kafka_plan']
    )

    # Create/Check PostgreSQL service status
    aiven.create_service(
        constants.config['project'],
        'pg',
        constants.config['pg_name'],
        constants.config['pg_cloud'],
        constants.config['pg_plan']
    )

    # Wait for services to be in RUNNING state
    # aiven.wait_to_run(constants.config['project'], constants.config['kafka_name'])
    aiven.wait_to_run(constants.config['project'], constants.config['pg_name'])

    # Create tables if not exist
    p = PostgreSQLConnector()
    p.run_from_file('sql/success_requests.sql')
    p.run_from_file('sql/error_requests.sql')

    # Initialize site availability operations
    sites_availability = SitesAvailability()

    # Producer thread
    producer_thread = PeriodicThread(callback=sites_availability.produce_metrics_to_kafka,
                                     period=constants.PRODUCER_INTERVAL)
    producer_thread.start()

    # Consumer threads
    # Two (2) threads, one (1) for each use case and Kafka topic
    success_topic_thread = Process(target=sites_availability.consume_metrics_sink_postgres,
                                   args=("success_requests", "topic_group", "earliest", "success_requests"))
    error_topic_thread = Process(target=sites_availability.consume_metrics_sink_postgres,
                                 args=("error_requests", "topic_group", "earliest", "error_requests"))
    success_topic_thread.start()
    error_topic_thread.start()

    # Terminate and kill all active threads
    # http://jessenoller.com/blog/2009/01/08/multiprocessingpool-and-keyboardinterrupt
    try:
        producer_thread.join()
        success_topic_thread.join()
        error_topic_thread.join()
    except KeyboardInterrupt:
        producer_thread.cancel()
        producer_thread.join()

        success_topic_thread.terminate()
        success_topic_thread.join()

        error_topic_thread.terminate()
        error_topic_thread.join()
