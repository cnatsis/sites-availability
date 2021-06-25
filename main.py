from multiprocessing import Process

from SitesAvailability import SitesAvailability
from connectors import PostgreSQLConnector, KafkaClient

if __name__ == '__main__':
    # Used env_file. Could have used argParser

    con = PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")

    # kafka = KafkaClient()
    sites_availability = SitesAvailability()

    # sites = utils.read_file('conf/sites.txt')
    # for site in sites:
    #     print('-----------------------------------')
    #     # Create poller
    #     metrics = utils.get_site_metrics(site)
    #     if metrics['type'] == 'SUCCESS':
    #         kafka.produce("success_topic", metrics['site_url'], metrics)
    #     else:
    #         kafka.produce("error_topic", metrics['site_url'], metrics)

    # Why multiprocessing Process and not threading.Thread

    # Producer thread
    producer_thread = Process(target=sites_availability.produce_metrics_to_kafka)
    producer_thread.start()

    # Consumer threads
    # Two (2) threads, one (1) for each use case and Kafka topic
    success_topic_thread = Process(target=sites_availability.consume_metrics_sink_postgres,
                                   args=("success_topic", "test_topic_group", "earliest", "success_requests"))
    error_topic_thread = Process(target=sites_availability.consume_metrics_sink_postgres,
                                 args=("error_topic", "test_topic_group", "earliest", "error_requests"))

    success_topic_thread.start()
    error_topic_thread.start()

    # Terminate and kill all active threads
    # http://jessenoller.com/blog/2009/01/08/multiprocessingpool-and-keyboardinterrupt
    try:
        producer_thread.join()
        success_topic_thread.join()
        error_topic_thread.join()
    except KeyboardInterrupt:
        producer_thread.terminate()
        producer_thread.join()

        success_topic_thread.terminate()
        success_topic_thread.join()

        error_topic_thread.terminate()
        error_topic_thread.join()

    # kafka.consume(("success_topic", "error_topic"), "test_topic_group", "earliest")
