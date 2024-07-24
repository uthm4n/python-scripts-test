import sys
sys.path.append('/usr/lib/python3/dist-packages')

import requests
import urllib3
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# logging config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

INSTANCE_ID = morpheus['instance']['id']
INSTANCE_IP = morpheus['instance']['container']['internalIp']

APPLIANCE_URL = morpheus['morpheus']['applianceUrl']
API_ACCESS_TOKEN = morpheus['morpheus']['apiAccessToken']

def isValidAccessToken(token):
    GET_WIKI_PAGE = f"{APPLIANCE_URL}/api/instances/{INSTANCE_ID}/wiki"
    VALIDATION_RESPONSE = requests.get(GET_WIKI_PAGE, headers={"Authorization": f"{token}"}, verify=False)
    if VALIDATION_RESPONSE.status_code == 404:
        logger.error("Instance not found! Please double-check the Wiki page URL and ensure that you have a valid API Token set")
        return False
    else:
        return True


# Determine the access token to be used - i.e. use the one that returns a 200 response from GET_WIKI_PAGE
if isValidAccessToken(API_ACCESS_TOKEN):
    TOKEN = API_ACCESS_TOKEN
else:
    TOKEN = sys.argv[1]

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

UPDATE_WIKI_PAGE = f"{APPLIANCE_URL}/api/instances/{INSTANCE_ID}/wiki"  								
PAYLOAD = {"page": {"content": f"# Usage Information\r\n***\r\n\r\nOracle Linux Server for personal usage - this is a basic setup only. You can logon at `{INSTANCE_IP}` via SSH with user `test`.\r\n\r\n## Console\r\n***\r\n\r\nYou can access the **Console** from [here](https:\/\/ueqbal-morph-appliance.localdomain\/provisioning\/instances\/{INSTANCE_ID}#!console-tab), or by clicking the appropriate Tab to the left of the current Tab.\r\n\r\n(C)2024 Uthman Test"}}

try:
    logger.debug("Starting the script...")
    logger.debug(f"[VARIABLES:\r\nINSTANCE_ID: {INSTANCE_ID}\r\nINSTANCE_IP: {INSTANCE_IP}\r\nAPPLIANCE_URL: {APPLIANCE_URL}\r\nTOKEN: {TOKEN}]")
	
    # API request to update the Wiki page
    response = requests.put(UPDATE_WIKI_PAGE, headers=HEADERS, json=PAYLOAD, verify=False)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

    logger.debug("Request successful, processing response...")
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.text}")

    print('Successfully updated Wiki page')

except requests.exceptions.RequestException as e:
    logger.error(f"Request error: {e}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")

logger.debug("Script finished.")
