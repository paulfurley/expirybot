import io
import json
from os.path import abspath, dirname, join as pjoin

with io.open(abspath(pjoin(dirname(__file__), '..', 'config.json'))) as f:
    config_json = json.load(f)
    KEYSERVER = config_json['keyserver']
    MAILGUN_API_KEY = config_json['mailgun_api_key']

DATA_DIR = abspath(pjoin(dirname(__file__), '..', 'data'))

FINGERPRINT_CSV_HEADER = [
    'fingerprint',
    'uids',
    'created_date',
    'expiry_date',
]
