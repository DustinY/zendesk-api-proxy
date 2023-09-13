from enum import Enum
from app.config import Config
from app.utilities.request_utils import RequestUtils


class ZendeskDictConstants(dict, Enum):
    api_header = {
        "Content-Type": "application/json",
        "Authorization": RequestUtils.get_basic_auth_credential("{0}/token:{1}".format(Config.ZAP_API_USER, Config.ZAP_API_TOKEN))
    }


class ZendeskStrConstants(str, Enum):
    list_tickets_url = "https://{}.zendesk.com/api/v2/tickets.json".format(Config.ZENDESK_DOMAIN)

