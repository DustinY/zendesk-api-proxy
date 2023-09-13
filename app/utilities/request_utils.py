from typing import Any
import requests
from app.utilities.encoding_utils import EncodingUtils

class RequestUtils:

    @staticmethod
    def get(**kwargs: Any) -> requests.Response:
        return requests.get(**kwargs)

    @staticmethod
    def get_basic_auth_credential(credential):
        return 'Basic ' + EncodingUtils.base64_encode(credential)