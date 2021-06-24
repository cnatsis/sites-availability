import utils
from connectors import PostgreSQLConnector, KafkaClient

from multiprocessing import Process

if __name__ == '__main__':
    failed_sites = []

    con = PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")

    kafka = KafkaClient()
    sites = utils.read_file('conf/sites.txt')
    for site in sites:
        print('-----------------------------------')
        metrics = utils.get_site_metrics(site)
        if metrics['type'] == 'SUCCESS':
            kafka.produce("success_topic", metrics['site_url'], metrics)
        else:
            kafka.produce("error_topic", metrics['site_url'], metrics)

    # Why Process and not threading.Thread
    t1 = Process(target=kafka.consume, args=("success_topic", "test_topic_group", "earliest", "success_requests"))
    t2 = Process(target=kafka.consume, args=("error_topic", "test_topic_group", "earliest", "error_requests"))
    t1.start()
    t2.start()

    # http://jessenoller.com/blog/2009/01/08/multiprocessingpool-and-keyboardinterrupt
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        t1.terminate()
        t1.join()
        t2.terminate()
        t2.join()

    # kafka.consume(("success_topic", "error_topic"), "test_topic_group", "earliest")
