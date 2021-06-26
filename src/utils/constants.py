from environs import Env
import os

env = Env()
env.read_env()

PRODUCER_INTERVAL = env.int('PRODUCER_INTERVAL', default=5)
SITES_FILE_PATH = os.path.join(os.path.dirname(__file__), '../../conf/sites.txt')
