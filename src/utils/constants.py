from environs import Env
import os

env = Env()
env.read_env()

PRODUCER_INTERVAL = env.int('PRODUCER_INTERVAL', default=5)
SITES_FILE_PATH = os.path.join(os.path.dirname(__file__), '../../conf/sites.txt')

AIVEN_TOKEN = env.str('AIVEN_TOKEN', default=None)
AIVEN_PROJECT = env.str('AIVEN_PROJECT', default='sites-availability')
AIVEN_API_URL = env.str('AIVEN_API_URL', default=None)
AIVEN_KAFKA_NAME = env.str('AIVEN_KAFKA_NAME', default=None)
AIVEN_PG_NAME = env.str('AIVEN_PG_NAME', default=None)
