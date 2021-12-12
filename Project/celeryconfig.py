import dotenv
import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

os.environ.setdefault('C_FORCE_ROOT', 'true')
broker_url = config('REDIS_URL')
result_backend = config('REDIS_URL')
accept_content = ["pickle", "json", "msgpack", "yaml"]
task_ignore_result = False

