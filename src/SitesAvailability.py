import re
from datetime import datetime

import requests

from src import utils
from src.connectors import KafkaClient, PostgreSQLConnector


class SitesAvailability:
    """
    A class that fetches metrics from various sites & produces records to Apache Kafka.
    Also, it consumes produced records from Kafka and sinks them to a PostgreSQL database

    Usage:
    sites_availability = SitesAvailability()
    """

    def __init__(self):
        """
        Initialize site availability operations.
        """
        super().__init__()
        self.kafka = KafkaClient()
        self.sites = utils.read_file_to_list(utils.constants.SITES_FILE_PATH)
        self.kafka.create_topic(
            "success_requests",
            partitions=3
        )
        self.kafka.create_topic(
            "error_requests",
            partitions=3
        )

    @staticmethod
    def get_site_metrics(site):
        """
        Fetches site metrics
        :param site: Site to check
        :return: Metrics dict for both successful and unsuccessful requests
        """
        now = datetime.now()

        request_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print("request_time={}".format(request_time))
        try:
            b = requests.get(site)
            b.raise_for_status()

            # Fetch request metrics for a successful request
            http_response_time = b.elapsed.total_seconds()
            status_code = b.status_code

            # Search for title tag in HTML. Leave empty string if title not found.
            search_text = re.search("<title>(.*?)</title>", b.text)

            grouped_text = ''
            if search_text:
                grouped_text = search_text.group(1)

            b.close()

            return {
                "request_time": request_time,
                "type": "SUCCESS",
                "site_url": site,
                "response_time_sec": http_response_time,
                "status_code": status_code,
                "regex_search": grouped_text
            }
        except requests.exceptions.RequestException as e:
            return {
                "request_time": request_time,
                "type": "ERROR",
                "site_url": site,
                "exception_type": type(e).__name__
            }

    def produce_metrics_to_kafka(self):
        """
        Polled fetching of metrics for each site in list.
        """
        for site in self.sites:
            print('-----------------------------------')
            print(site)
            metrics = self.get_site_metrics(site)
            if metrics['type'] == 'SUCCESS':
                self.kafka.produce("success_requests", metrics['site_url'], metrics)
            else:
                self.kafka.produce("error_requests", metrics['site_url'], metrics)

    def consume_metrics_sink_postgres(self, topics, group_id, auto_offset_reset, pg_table):
        """
        Consume data process that stores received records to PostgreSQL table
        :param topics: Kafka topics to subscribe
        :param group_id: Kafka consumer group ID
        :param auto_offset_reset: Read from start or end of stream. Valid values 'earliest' or 'latest'.
        :param pg_table: PostgreSQL target table
        """
        consumer = self.kafka.create_consumer(group_id, auto_offset_reset)
        print(f"Consuming Kafka Topic '{topics}'. Press Ctrl+C to exit")
        consumer.subscribe(topics)

        con = PostgreSQLConnector()

        try:
            for msg in consumer:
                print(f"Topic: {msg.topic}, Offset: {msg.offset}, Key: {msg.key}, Value: {msg.value}")
                con.insert(pg_table, msg.value)
            con.close()
        except KeyboardInterrupt:
            consumer.commit()
            consumer.close()
            con.close()
