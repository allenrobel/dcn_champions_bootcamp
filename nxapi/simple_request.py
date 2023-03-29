#!/usr/bin/env python
"""
Simple demonstration for using the python requests library to both 
send configuration to an NX-OS switch and to retrieve the output
of show commands.
"""
import requests
import json
import urllib3
import sys

urllib3.warnings.filterwarnings("ignore", module="urllib3")

def send_request_json(params):
    """
    params dictionary
        "ip4": str()      # address of NXAPI endpoint
        "username": str() # username of NXAPI endpoint
        "password": str() # password of NXAPI endpoint
        "timeout": int()  # request timeout in seconds
        "proxies": dict() # proxy servers 
        "cookies": dict()
        "payload": dict()

    Example params dictionary

    {
        "ip4": "10.1.1.1"
        "username": "admin"
        "password": "mypassword"
        "timeout": 10
        "proxies": {
            "scheme": "http"
            "url" : "http://myproxy.foo.com:8080"
        }
        "cookies": {
        }
        "payload": {
            "ins_api": {
                "version": "1.0",
                "type": "cli_show",
                "chunk": "0", 
                "sid": "1",
                "input": "show interface Eth1/1",
                "output_format": "json",
            }        
        }
    }
    """
    headers = {}
    headers["content-type"] = "application/json"
    url = f"https://{params['ip4']}:443/ins"
    try:
        response = session.post(
            url,
            auth = (
                params["username"],
                params["password"]
            ),
            data = json.dumps(params["payload"]),
            proxies = params["proxies"],
            headers = headers,
            timeout = params["timeout"],
            verify = False,
            cookies = params["cookies"]
        )

    except Exception as err:
        print(f"Exiting. GenericException -> unable to connect to {params['ip4']}.")
        print(f"Exception detail: {err}")
        sys.exit(1)

    if response.status_code != 200:
        print(f"{response.url} request failed.")
        print(f"Code {response.status_code} ({response.content.decode('utf-8')})")
        sys.exit(1)
    return response

def print_response_info(response):
    try:
        response_json = response.json()
    except Exception as err:
        print(f"Got exception while converting response to JSON. Exception: {err}")
        sys.exit(1)
    print(f"response.url: {response.url}")
    print(f"response.status_code: {response.status_code}")
    print(f"response.reason: {response.reason}")
    print(f"len(response.text): {len(response.text)}")
    print(f"response.json(): {json.dumps(response_json, indent=4, sort_keys=True)}")
    print(f"response.headers: {response.headers}")

def get_cookies(params, response):
    if len(response.cookies) == 0:
        print("old cookies are fresh")
    else:
        print("cookies refreshed by DUT")
        print(f"  old cookies {params['cookies']}")
        print(f"  new cookies {response.cookies}")
    return response.cookies

def get_common_mandatory_keys():
    keys = set()
    keys.add("username")
    keys.add("password")
    keys.add("ip4")
    keys.add("timeout")
    keys.add("proxies")
    keys.add("cookies")
    return keys

def cli_show(d):
    """
    Send NXAPI request using cli_show request method
    """
    if not isinstance(d, dict):
        print(f"Exiting. Missing params. Example: show(params_dictionary)")
        sys.exit(1)
    mandatory_keys = get_common_mandatory_keys()
    mandatory_keys.add("command")
    if not mandatory_keys.issubset(d.keys()):
        print(f"missing mandatory key.")
        print(f"Expected keys: {','.join(list(sorted(mandatory_keys)))}")
        print(f"Got keys: {','.join(list(sorted(d.keys())))}")
        sys.exit(1)
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",  # do not chunk results
            "sid": "1",    # session ID
            "input": d['command'],
            "output_format": "json",
        }
    }
    d["payload"] = payload
    return send_request_json(d)


def cli_conf(d):
    """
    Send NXAPI request using cli_conf request method
    """
    if not isinstance(d, dict):
        print(f"Exiting. Missing params. Example: show(params_dictionary)")
        sys.exit(1)
    mandatory_keys = get_common_mandatory_keys()
    mandatory_keys.add("config")
    if not mandatory_keys.issubset(d.keys()):
        print(f"missing mandatory key.")
        print(f"Expected keys: {','.join(list(sorted(mandatory_keys)))}")
        print(f"Got keys: {','.join(list(sorted(d.keys())))}")
        sys.exit(1)
    payload = {
        "ins_api": {
            "version": "1.0",
            "type": "cli_conf",
            "chunk": "0",  # do not chunk results
            "sid": "1",    # session ID
            "input": " ; ".join(d['config']),
            "output_format": "json",
        }
    }
    d["payload"] = payload
    return send_request_json(d)

# These will be in all 'show CLI' responses
def get_output(response):
    try:
        response_json = response.json()['ins_api']['outputs']['output']
    except Exception as err:
        print(f"unable to retrieve response output")
        print(f"Exeption detail: {err}")
        sys.exit(1)
    if response_json["code"] != "200":
        print(f'Bad response {response_json["code"]} {response_json["msg"]}')
        sys.exit(1)
    return response_json
def get_body(response):
    return get_output(response)["body"]

# These are specific to 'show interface'
def get_table_interface(response):
    return get_body(response)["TABLE_interface"]
def get_row_interface(response):
    return get_table_interface(response)['ROW_interface']

def get_interface_name(response):
    return get_row_interface(response)['interface']
def get_interface_state(response):
    return get_row_interface(response)['state']
def get_interface_description(response):
    return get_row_interface(response)['desc']
def get_interface_eth_outrate1_bits(response):
    return get_row_interface(response)['eth_outrate1_bits']

def print_interface_info(response):
    print(f"Interface {get_interface_name(response)}")
    print(f"  state: {get_interface_state(response)}")
    print(f"  description: {get_interface_description(response)}")
    print(f"  eth_outrate1_bits: {get_interface_eth_outrate1_bits(response)}")

def get_hostname(response):
    return get_body(response)["hostname"]
def print_hostname(response):
    print(f"hostname {get_hostname(response)}")


session = requests.Session()

params = {}
params["username"] = "admin"
params["password"] = "mypassword"
params["ip4"] = "10.1.1.1"
params["timeout"] = 10
params["proxies"] = {}
params["cookies"] = {}
params["config"] = []
params["config"].append('interface Eth1/11')
params["config"].append('description aaa')

response = cli_conf(params)
params["cookies"] = get_cookies(params, response)
#print_response_info(response)

params["command"] = "show hostname"
response = cli_show(params)
params["cookies"] = get_cookies(params, response)
print_hostname(response)

params["command"] = "show interface Eth1/11"
response = cli_show(params)
params["cookies"] = get_cookies(params, response)
print_interface_info(response)
