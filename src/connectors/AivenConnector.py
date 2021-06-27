import time
from aiven.client.client import AivenClient, Error


# https://github.com/aiven/aiven-examples/blob/master/kafka/python/connector/debezium_pg.py
def timeout(stop_after=200.0):
    """decorated function should return 1 when done and 0 when it should run again"""

    def wrap(func):
        def inner(self, *args, **kwargs):
            start_time = time.monotonic()
            timeout_t = stop_after + start_time
            while time.monotonic() < timeout_t:
                if func(self, *args, **kwargs):
                    return
                time.sleep(3.0)
            print("This is taking too long. Request timed out.")

        return inner

    return wrap


class AivenConnector:
    """
    Connect to Aiven services using AivenClient
    """

    def __init__(self, config):
        self.config = config
        self.client = AivenClient(self.config["api_url"])
        self.login(self.config['token'])

    def login(self, token=None):
        """
        Login to Aiven using auth token
        :param token: auth token
        """
        self.client.set_auth_token(token)

    def create_service(self, project, service_type, service_name, cloud, plan, service_config=None):
        """
        Create Aiven service
        :param project: Aiven project
        :param service_name: Service name
        :param cloud: Cloud provider (aws-<region>, google-<region>, azure-<region>, do-<region>, upcloud-<region>)
        :param plan: Service plan
        :param service_type: Service type. Example: 'kafka', 'pg', etc.
        :param service_config: Kafka services settings. Example: service_config = {"kafka_connect": True}
        :return:
        """
        try:
            aiven_service = self.client.get_service(project, service_name)
            print(f"Service '{aiven_service}' already exists!")
        except Error:
            print(f"Creating service '{service_name}...'")
            aiven_service = self.client.create_service(
                project,
                service_name,
                service_type,
                plan,
                cloud,
                user_config=service_config
            )
            print(f"Service '{aiven_service}' created!")

    def get_service(self, project, service_name):
        try:
            return self.client.get_service(project, service_name)
        except Error:
            print(f"No service '{service_name}' found!")
            return None

    # def update_service(self, project, service_name, service_config=None):
    #     """
    #
    #     :param project: Aiven project
    #     :param service_name: Service name
    #     :param service_config: Aiven service settings. Example: service_config = {"kafka_connect": True}
    #     :return:
    #     """
    #     if service_config is None:
    #         service_config = {}
    #     try:
    #         aiven_service = self.client.get_service(project, service_name)
    #         for key in service_config.keys():
    #
    #             if not aiven_service["user_config"][key]:
    #                 print(f"Enabling '{key}' for {service_name}...")
    #                 self.kafka = self.client.update_service(
    #                     project, service_name, user_config=service_config
    #                 )
    #             else:
    #                 print(f"Kafka Connect is already enabled on {self.config['kafka_name']}!")
    #     except Error:
    #         print(f"No service '{self.config['kafka_name']}' found!")

    def is_service_running(self, project, service_name):
        """
        Checks if Aiven service is in RUNNING state
        :param project: Aiven project
        :param service_name: Service name
        :return: 1 if RUNNING, else 0
        """
        aiven_service = self.client.get_service(project, service_name)
        print(f"Status of {service_name}: {aiven_service['state']}")
        if aiven_service['state'] == "RUNNING":
            print(f"{service_name} is RUNNING!")
            return 1
        return 0

    @timeout(300)
    def wait_to_run(self, project, service_name):
        """
        Method that is executed until service is in RUNNING state.
        :param project: Aiven project
        :param service_name: Service name
        :return: Service state
        """
        print(f'Checking if {service_name} is RUNNING...')
        return self.is_service_running(project, service_name)
