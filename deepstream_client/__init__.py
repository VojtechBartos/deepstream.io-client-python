from .client import Client as DeepstreamClient
from .exceptions import DeepstreamHTTPError

__version__ = '0.1.0'
__all__ = [
    'DeepstreamClient',
    'DeepstreamHTTPError'
]
