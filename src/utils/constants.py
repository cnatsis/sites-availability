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
AIVEN_KAFKA_CLOUD = env.str('AIVEN_KAFKA_CLOUD', default='do-fra')
AIVEN_KAFKA_PLAN = env.str('AIVEN_KAFKA_PLAN', default='business-4')

AIVEN_PG_NAME = env.str('AIVEN_PG_NAME', default=None)
AIVEN_PG_CLOUD = env.str('AIVEN_PG_CLOUD', default='do-fra')
AIVEN_PG_PLAN = env.str('AIVEN_PG_PLAN', default='startup-4')

config = {
    "api_url": AIVEN_API_URL,
    "project": AIVEN_PROJECT,
    "token": AIVEN_TOKEN,
    "kafka_name": AIVEN_KAFKA_NAME,
    "kafka_cloud": AIVEN_KAFKA_CLOUD,
    "kafka_plan": AIVEN_KAFKA_PLAN,
    "pg_name": AIVEN_PG_NAME,
    "pg_cloud": AIVEN_PG_CLOUD,
    "pg_plan": AIVEN_PG_PLAN
}
