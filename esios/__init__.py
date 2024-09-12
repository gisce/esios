from __future__ import absolute_import    

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution(__name__).version
except Exception as e:
    VERSION = 'unknown'

from libsaas.executors import requests_executor
requests_executor.use()
from .service import Esios
