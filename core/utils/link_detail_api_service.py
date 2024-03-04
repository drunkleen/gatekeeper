import json
import requests

from core.models import Subscription, PanelConnection


def byte_to_gigabytes(byte_data):
    gigabytes = byte_data / (1024 ** 3)
    megabytes = byte_data / (1024 ** 2)
    kilobytes = byte_data / 1024

    if gigabytes >= 1:
        return f"{gigabytes:.2f} GB"
    elif megabytes >= 1:
        return f"{megabytes:.2f} MB"
    else:
        return f"{kilobytes:.2f} KB"


headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
PATH_API_alireza = "/xui/API/inbounds/"
PATH_API_MHSANAEI = "/panel/api/inbounds/"

PATH_GET_TRAFFIC = 'getClientTraffics/'


def get_user_info(link: Subscription):
    session = requests.Session()

    if link.panel_connection.panel_name == PanelConnection.panel_marzban:
        response = requests.get(link.subscription_link)
        if response.status_code == 200:
            response = response.headers['subscription-userinfo'].split("; ")
            data = {}

            for pair in response:
                key, value = pair.split("=")
                data[key] = int(value) if value.isdigit() else value

            data['download'] = str(byte_to_gigabytes(data.get('download')))
            data['upload'] = str(byte_to_gigabytes(data.get('upload')))
            data['total'] = str(byte_to_gigabytes(data.get('total')))
            return data
        else:
            return None

    body = {"username": link.panel_connection.panel_user, "password": link.panel_connection.panel_password}
    session.post(f"{link.panel_connection.panel_url}/login", data=json.dumps(body), headers=headers)

    if link.panel_connection.panel_name == PanelConnection.panel_alireza:
        response = session.get(
            f"{link.panel_connection.panel_url}{PATH_API_alireza}{PATH_GET_TRAFFIC}{link.user_email_in_xui_panel}",
            headers=headers
        )
    elif link.panel_connection.panel_name == PanelConnection.panel_sanaei:
        response = session.get(
            f"{link.panel_connection.panel_url}{PATH_API_MHSANAEI}{PATH_GET_TRAFFIC}{link.user_email_in_xui_panel}",
            headers=headers
        )
    else:
        return None

    if response.status_code == 200 and response.json()['success']:
        return {
            'upload': byte_to_gigabytes(json.loads(response.text)['obj']['up']),
            'download': byte_to_gigabytes(json.loads(response.text)['obj']['down']),
            'total': byte_to_gigabytes(json.loads(response.text)['obj']['total']),
            'expire': json.loads(response.text)['obj']['expiryTime'],
        }
    else:
        return None


def connection_test(username, password, panel_url):
    body = {"username": username, "password": password}
    try:
        response = requests.post(f"{panel_url}/login", data=json.dumps(body), headers=headers)
        return response.status_code == 200 and response.json()['success']
    except:
        return False
