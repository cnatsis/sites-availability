from environs import Env

env = Env()
env.read_env()

PORT = env.int('PORT', default=8500)
SERVICE_NAME = env.str('SERVICE_NAME', default='python-shell')
FLASK_DEBUG = env.bool('FLASK_DEBUG', default='false')
CONSUL_HOST = env.str('CONSUL_HOST', default='localhost')
CONSUL_PORT = env.int('CONSUL_PORT', default=8500)
SYSLOG_HOST = env.str('SYSLOG_HOST', default='localhost')
SYSLOG_UDP_PORT = env.int('SYSLOG_UDP_PORT', default=514)
LOGSTASH_HOST = env.str('LOGSTASH_HOST', default='localhost')
LOGSTASH_PORT = env.int('LOGSTASH_PORT', default=5000)
HOST_NAME = env.str('HOST_NAME', default=None)

DB_HOST = env.str('DB_HOST', default='<ENTER_HOST>')
DB_PORT = env.int('DB_PORT', default=1521)
DB_SCHEMA = env.str('DB_SCHEMA', default='<ENTER_SCHEMA>')
DB_USER = env.str('DB_USER', default='<ENTER_USER>')
DB_PASS = env.str('DB_PASS', default='<ENTER_PASSWORD>')

KAFKA_BROKER = env.str('KAFKA_BROKER', default='localhost')
KAFKA_PORT = env.int('KAFKA_PORT', default=9092)
KAFKA_AUTO_OFFSET_RESET = env.str('KAFKA_AUTO_OFFSET_RESET', default='latest')
KAFKA_KEY = env.str('KAFKA_KEY', default='python-shell')
KAFKA_BATCH_SIZE = env.int('KAFKA_BATCH_SIZE', default=100000)
KAFKA_MAX_REQUEST_SIZE = env.int('KAFKA_MAX_REQUEST_SIZE', default=2000000)

EXTRA_LOGS = env.bool('EXTRA_LOGS', default='false')
PREPEND_LOG = env.str('PREPEND_LOG', default='')
