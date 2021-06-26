from multiprocessing import Process

from SitesAvailability import SitesAvailability
from utils import PeriodicThread

if __name__ == '__main__':
    # Used env_file. Could have used argParser

    sites_availability = SitesAvailability()

    # Why multiprocessing Process and not threading.Thread

    # Producer thread
    # producer_thread = Process(target=sites_availability.produce_metrics_to_kafka)
    # producer_thread = Process(target=PeriodicThread(callback=sites_availability.produce_metrics_to_kafka).run())
    producer_thread = PeriodicThread(callback=sites_availability.produce_metrics_to_kafka, period=5)
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
        producer_thread.cancel()
        producer_thread.join()

        success_topic_thread.terminate()
        success_topic_thread.join()

        error_topic_thread.terminate()
        error_topic_thread.join()
