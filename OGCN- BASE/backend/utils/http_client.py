import requests
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    def get(self, url, **kwargs):
        try:
            # Bypass SSL verification for development purposes
            response = requests.get(url, verify=False, **kwargs)
            response.raise_for_status()
            logger.debug(f"Response content: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP GET request failed: {e}")
            return None

    def post(self, url, **kwargs):
        try:
            # Bypass SSL verification for development purposes
            response = requests.post(url, verify=False, **kwargs)
            response.raise_for_status()
            logger.debug(f"Response content: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP POST request failed: {e}")
            return None

    def put(self, url, **kwargs):
        try:
            response = requests.put(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP PUT request failed: {e}")
            return None

    def delete(self, url, **kwargs):
        try:
            response = requests.delete(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP DELETE request failed: {e}")
            return None