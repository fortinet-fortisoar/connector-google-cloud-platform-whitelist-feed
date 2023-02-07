""" Copyright start
  Copyright (C) 2008 - 2023 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

from requests import request, exceptions as req_exceptions
from connectors.core.connector import get_logger, ConnectorError
from .constants import *


logger = get_logger("google-cloud-platform-whitelist-feed")


class GoogleCloudPlatformWhitelistFeed:
    def __init__(self, config, *args, **kwargs):
        server_url = config.get("server_url")
        if not server_url.startswith('https://') and not server_url.startswith('http://'):
            server_url = "https://" + server_url
        self.url = server_url
        self.verify_ssl = config.get("verify_ssl")

    def api_request(self, method, endpoint):
        try:
            endpoint = self.url + endpoint
            response = request(method, endpoint, verify=self.verify_ssl)

            if response.status_code in [200, 201, 204]:
                if response.text != "":
                    return response.json()
                else:
                    return True
            else:
                if response.text != "":
                    err_resp = response.json()
                    failure_msg = err_resp['error']['message']
                    error_msg = 'Response [{0}:{1} Details: {2}]'.format(response.status_code, response.reason,
                                                                         failure_msg if failure_msg else '')
                else:
                    error_msg = 'Response [{0}:{1}]'.format(response.status_code, response.reason)
                logger.error(error_msg)
                raise ConnectorError(error_msg)
        except req_exceptions.SSLError:
            logger.error('An SSL error occurred')
            raise ConnectorError('An SSL error occurred')
        except req_exceptions.ConnectionError:
            logger.error('A connection error occurred')
            raise ConnectorError('A connection error occurred')
        except req_exceptions.Timeout:
            logger.error('The request timed out')
            raise ConnectorError('The request timed out')
        except req_exceptions.RequestException:
            logger.error('There was an error while handling the request')
            raise ConnectorError('There was an error while handling the request')
        except Exception as err:
            raise ConnectorError(str(err))


def ip_ranges(config, params):
    ob = GoogleCloudPlatformWhitelistFeed(config)
    res1 = ob.api_request(Method.GET, "goog.json")
    prefixes1 = res1.get("prefixes", [])
    res2 = ob.api_request(Method.GET, "cloud.json")
    prefixes2 = res2.get("prefixes", [])
    all_prefixes = (prefixes2 + prefixes1)[0:5]
    res2["prefixes"] = all_prefixes
    return res2


def check_health_ex(config):
    ip_ranges(config, None)
    return True


operations = {
    "ip_ranges": ip_ranges,
}
